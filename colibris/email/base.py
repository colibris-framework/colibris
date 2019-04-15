
import logging


logger = logging.getLogger(__name__)


class EmailBackend:
    def send(self, email_message):
        raise NotImplementedError


class NullBackend(EmailBackend):
    def __init__(self, **kwargs):
        pass

    def send(self, email_message):
        logger.debug('null backend: send() called')
