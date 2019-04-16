
import logging


logger = logging.getLogger(__name__)


class EmailBackend:
    def __init__(self, **kwargs):
        pass

    def send_messages(self, email_messages):
        raise NotImplementedError


class NullBackend(EmailBackend):
    def send_messages(self, email_messages):
        logger.debug('null backend: send_messages() called')
