
import logging
import sys

from colibris.email.base import EmailBackend


logger = logging.getLogger(__name__)


class ConsoleBackend(EmailBackend):
    def __init__(self):
        self.stream = sys.stdout

    def send_messages(self, email_messages):
        for message in email_messages:
            prepared = message.prepare()
            data = prepared.as_bytes()
            text = data.decode()

            self.stream.write('-' * 10 + '\n')
            self.stream.write(text)

        self.stream.write('-' * 10 + '\n')
