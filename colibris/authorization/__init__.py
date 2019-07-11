
from colibris.conf import settings

from .base import AuthorizationBackend
from .exceptions import *
from .permissions import *


def authorize(account, method, path, handler, permissions):
    return AuthorizationBackend.get_instance().authorize(account, method, path, handler, permissions)


def setup():
    AuthorizationBackend.configure(settings.AUTHORIZATION)
