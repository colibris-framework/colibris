
import async_timeout
import asyncio
import logging

from colibris.conf import settings

from .exceptions import *
from .base import TaskQueueBackend


DEFAULT_TIMEOUT = 300  # seconds

logger = logging.getLogger(__name__)


async def execute(func, *args, timeout=DEFAULT_TIMEOUT, **kwargs):
    try:
        with async_timeout.timeout(timeout):
            return await TaskQueueBackend.get_instance().execute(func, *args, timeout=timeout, **kwargs)

    except asyncio.TimeoutError:
        raise TimeoutException(timeout)


def add_worker_arguments(parser):
    TaskQueueBackend.get_instance().add_worker_arguments(parser)


def run_worker(options):
    TaskQueueBackend.get_instance().run_worker(options)


def setup():
    TaskQueueBackend.configure(settings.TASK_QUEUE)


def is_enabled():
    return TaskQueueBackend.is_enabled()


def is_created():
    return TaskQueueBackend.is_created()
