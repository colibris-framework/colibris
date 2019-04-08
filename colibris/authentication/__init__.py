
import logging

from colibris import settings
from colibris import utils

from .exceptions import *


_REQUEST_ACCOUNT_ITEM_NAME = 'account'
_REQUEST_ACCOUNT_PERSISTENT_ITEM_NAME = 'account_persistent'


logger = logging.getLogger(__name__)

_backend = None


def get_backend():
    global _backend

    if _backend is None:
        backend_settings = dict(settings.AUTHENTICATION)
        backend_path = backend_settings.pop('backend', 'colibris.authentication.base.NullBackend')
        backend_class = utils.import_member(backend_path)

        logger.debug('creating backend of class %s', backend_path)

        _backend = backend_class(**backend_settings)

    return _backend


def authenticate(request):
    account = get_backend().authenticate(request)
    request[_REQUEST_ACCOUNT_ITEM_NAME] = account

    return account


def get_account(request):
    return request.get(_REQUEST_ACCOUNT_ITEM_NAME)


def is_persistent_account(request):
    return request.get(_REQUEST_ACCOUNT_PERSISTENT_ITEM_NAME)


def login(request, account, persistent):
    logger.debug('logging in account "%s" (persistent=%s)', account, persistent)

    request[_REQUEST_ACCOUNT_ITEM_NAME] = account
    request[_REQUEST_ACCOUNT_PERSISTENT_ITEM_NAME] = persistent


def logout(request):
    account = request.pop(_REQUEST_ACCOUNT_ITEM_NAME, None)
    if account:
        logger.debug('logged out account "%s"', account)


def response_login(response, account, persistent):
    return get_backend().response_login(response, account, persistent)


def response_logout(response):
    return get_backend().response_logout(response)
