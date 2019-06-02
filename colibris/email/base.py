
import logging

from colibris.conf.backends import BackendMixin


logger = logging.getLogger(__name__)


class EmailBackend(BackendMixin):
    def __init__(self, **kwargs):
        pass

    def send_messages(self, email_messages):
        raise NotImplementedError
