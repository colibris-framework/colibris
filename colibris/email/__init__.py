
import logging

from colibris.conf import settings

from .message import EmailMessage
from .base import EmailBackend


logger = logging.getLogger(__name__)


def send(email_message):
    logger.debug('sending %s', email_message)
    return EmailBackend.get_instance().send_messages([email_message])


def send_many(email_messages):
    logger.debug('sending %d messages', len(email_messages))
    return EmailBackend.get_instance().send_messages(email_messages)


def setup():
    EmailBackend.configure(settings.EMAIL)


def is_enabled():
    return EmailBackend.is_enabled()


def is_created():
    return EmailBackend.is_created()
