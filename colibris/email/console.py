
import logging
import sys

from colibris.email.base import EmailBackend


logger = logging.getLogger(__name__)


class ConsoleBackend(EmailBackend):
    def __init__(self):
        self.stream = sys.stdout

    def send(self, email_message):
        prepared = email_message.prepare()
        data = prepared.as_bytes()
        text = data.decode()

        self.stream.write('-' * 10 + '\n')
        self.stream.write(text)
        self.stream.write('-' * 10 + '\n')


class NullBackend(EmailBackend):
    def __init__(self, **kwargs):
        pass

    def send(self, email_message):
        logger.debug('null backend: send() called')
