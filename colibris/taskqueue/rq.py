
import asyncio
import base64
import logging
import pickle
import redis
import rq.timeouts
import traceback

from rq import Connection
from rq.worker import Worker
from rq.connections import get_current_connection
from rq.queue import get_failed_queue

from colibris.taskqueue import UnpicklableException, TimeoutException
from colibris.taskqueue.base import TaskQueueBackend


DEFAULT_POLL_RESULTS_INTERVAL = 1  # seconds

logger = logging.getLogger(__name__)


class RQBackend(TaskQueueBackend):
    def __init__(self, host='localhost', port=6379, db=0, password=None,
                 poll_results_interval=DEFAULT_POLL_RESULTS_INTERVAL):

        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._poll_results_interval = poll_results_interval

        self._pending_results = []
        self._poll_loop_started = False
        self._connection = None
        self._queue = None

    def _get_connection(self):
        if self._connection is None:
            logger.debug('initializing redis connection')

            self._connection = redis.Redis(host=self._host, port=self._port, db=self._db, password=self._password)

        return self._connection

    def _get_queue(self):
        if self._queue is None:
            logger.debug('initializing task queue')

            self._queue = rq.Queue(connection=self._get_connection())

        return self._queue

    async def _poll_results(self):
        self._poll_loop_started = True
        logger.debug('starting results polling loop ')

        loop = asyncio.get_event_loop()

        while loop.is_running():
            remaining_results = []
            for tup in self._pending_results:
                try:
                    result, timeout, future = tup
                    result.refresh()

                    if result.is_finished and not future.cancelled():
                        future.set_result(result.return_value)

                    elif result.is_failed:
                        try:
                            exc_value = base64.b64decode(result.exc_info)
                            exc_value = pickle.loads(exc_value)

                        except Exception as e:
                            logger.error('failed to decode exception: %s', e, exc_info=True)
                            exc_value = UnpicklableException(result.exc_info)

                        # treat exceptions that could not be pickled
                        if isinstance(exc_value, str):
                            exc_value = UnpicklableException(exc_value)

                        # transform rq timeouts into taskqueue timeouts
                        if isinstance(exc_value, rq.timeouts.JobTimeoutException):
                            exc_value = TimeoutException(timeout)

                        future.set_exception(exc_value)

                    else:
                        remaining_results.append(tup)

                except Exception as e:
                    logger.error('polling results failed: %s', e, exc_info=True)

            self._pending_results = remaining_results

            await asyncio.sleep(self._poll_results_interval)

    async def execute(self, func, *args, timeout, **kwargs):
        if not self._poll_loop_started:
            _ = asyncio.ensure_future(self._poll_results())

        queue = self._get_queue()

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        result = queue.enqueue(func, timeout=timeout, *args, **kwargs)

        self._pending_results.append((result, timeout, future))

        return await future

    @staticmethod
    def handle_task_exception(job, exc_type, exc_value, tb):
        try:
            pickled_exc_value = pickle.dumps(exc_value)

        except (pickle.PickleError, TypeError):
            logger.error('exception could not be pickled')
            exc_string = Worker._get_safe_exception_string(traceback.format_exception(exc_type, exc_value, tb))
            pickled_exc_value = pickle.dumps(exc_string)

        # we need to encode pickled_exc_value using base64, since pickle is not guaranteed to be ASCII
        pickled_exc_value = base64.b64encode(pickled_exc_value).decode()

        failed_queue = get_failed_queue(get_current_connection(), job.__class__)
        failed_queue.quarantine(job, exc_info=pickled_exc_value)

    def add_worker_arguments(self, parser):
        parser.add_argument('--queue-name', help='The task queue name ("default" if unspecified)',
                            type=str, default='default')

    def run_worker(self, options):
        with Connection(self._get_connection()):
            w = Worker([options.queue_name], exception_handlers=[self.handle_task_exception])
            w.work()
