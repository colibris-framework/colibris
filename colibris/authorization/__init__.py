
import logging

from colibris.conf import settings

from .base import AuthorizationBackend
from .exceptions import *
from .permissions import require_permission, require_one_permission, require_all_permissions, require_any_permission


logger = logging.getLogger(__name__)


def authorize(account, method, path, permissions):
    return AuthorizationBackend.get_instance().authorize(account, method, path, permissions)


def setup():
    AuthorizationBackend.configure(settings.AUTHORIZATION)
