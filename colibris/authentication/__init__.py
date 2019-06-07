
import logging

from colibris.conf import settings

from .base import AuthenticationBackend
from .exceptions import *


_REQUEST_ACCOUNT_ITEM_NAME = 'account'


logger = logging.getLogger(__name__)


def authenticate(request):
    account = AuthenticationBackend.get_instance().authenticate(request)
    request[_REQUEST_ACCOUNT_ITEM_NAME] = account

    return account


def get_account(request):
    return request.get(_REQUEST_ACCOUNT_ITEM_NAME)


def login(request, account, persistent):
    logger.debug('logging in account "%s" (persistent=%s)', account, persistent)

    request[_REQUEST_ACCOUNT_ITEM_NAME] = account
    AuthenticationBackend.get_instance().login(request, persistent)


def logout(request):
    account = request.pop(_REQUEST_ACCOUNT_ITEM_NAME, None)
    if account:
        logger.debug('logging out account "%s"', account)
        AuthenticationBackend.get_instance().logout(request)


def process_request(request):
    return AuthenticationBackend.get_instance().process_request(request)


def process_response(request, response):
    return AuthenticationBackend.get_instance().process_response(request, response)


def setup():
    AuthenticationBackend.configure(settings.AUTHENTICATION)
