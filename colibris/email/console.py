
import logging
import sys

from .base import EmailBackend


logger = logging.getLogger(__name__)


class ConsoleBackend(EmailBackend):
    def __init__(self, **kwargs):
        self.stream = sys.stdout

        super().__init__(**kwargs)

    def send_messages(self, email_messages):
        for message in email_messages:
            prepared = message.prepare()
            data = prepared.as_bytes()
            text = data.decode()

            self.stream.write('-' * 10 + '\n')
            self.stream.write(text)

        self.stream.write('-' * 10 + '\n')
