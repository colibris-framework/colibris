
import logging

from colibris.conf import settings

from .base import AuthorizationBackend


ANY_PERMISSION = '*'

logger = logging.getLogger(__name__)


def authorize(account, method, path, authorization_info):
    return AuthorizationBackend.get_instance().authorize(account, method, path, authorization_info)


def setup():
    AuthorizationBackend.configure(settings.AUTHORIZATION)
