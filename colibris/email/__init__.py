
import logging

from colibris import settings
from colibris import utils


logger = logging.getLogger(__name__)

_backend = None


def get_backend():
    global _backend

    if _backend is None:
        backend_settings = dict(settings.EMAIL)
        backend_path = backend_settings.pop('backend', 'colibris.email.base.NullBackend')
        backend_class = utils.import_member(backend_path)

        logger.debug('creating backend of class %s', backend_path)

        _backend = backend_class(**backend_settings)

    return _backend


def send(email_message):
    logger.debug('sending %s', email_message)
    return get_backend().send(email_message)
