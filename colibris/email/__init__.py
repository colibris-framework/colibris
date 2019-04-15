
import logging

from colibris import settings
from colibris import utils
from colibris.email.message import EmailMessage


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
    return get_backend().send_messages([email_message])


def send_many(email_messages):
    logger.debug('sending %d messages', len(email_messages))
    return get_backend().send_messages(email_messages)
