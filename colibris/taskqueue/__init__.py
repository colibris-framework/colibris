
import async_timeout
import asyncio
import logging

from colibris import settings
from colibris import utils

from .exceptions import *


DEFAULT_TIMEOUT = 300  # seconds

logger = logging.getLogger(__name__)

_backend = None


def get_backend():
    global _backend

    if _backend is None:
        backend_settings = dict(settings.TASK_QUEUE)
        backend_path = backend_settings.pop('backend', None)
        if backend_path is None:
            raise TaskQueueNotConfigured()

        backend_class = utils.import_member(backend_path)
        _backend = backend_class(**backend_settings)

        logger.debug('backend of class %s created', backend_path)

    return _backend


async def execute(func, *args, timeout=DEFAULT_TIMEOUT, **kwargs):
    try:
        with async_timeout.timeout(timeout):
            return await get_backend().execute(func, *args, timeout=timeout, **kwargs)

    except asyncio.TimeoutError:
        raise TimeoutException(timeout)


def add_worker_arguments(parser):
    get_backend().add_worker_arguments(parser)


def run_worker(options):
    get_backend().run_worker(options)
