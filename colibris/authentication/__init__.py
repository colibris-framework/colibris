
import logging

from colibris import settings
from colibris import utils

from .exceptions import *


REQUEST_ACCOUNT_ITEM_NAME = 'account'


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
    request[REQUEST_ACCOUNT_ITEM_NAME] = account

    return account


def get_account(request):
    return request.get(REQUEST_ACCOUNT_ITEM_NAME)


def login(request, account, persistent):
    logger.debug('logging in account "%s"', account)

    get_backend().login(request, account, persistent)
    request[REQUEST_ACCOUNT_ITEM_NAME] = account


def logout(request):
    account = request.pop(REQUEST_ACCOUNT_ITEM_NAME, None)
    if account:
        get_backend().logout(request)
        logger.debug('logged out account "%s"', account)
