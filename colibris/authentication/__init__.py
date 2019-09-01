
import logging

from colibris.conf import settings

from .base import AuthenticationBackend
from .exceptions import *


REQUEST_ACCOUNT_KEY = 'account'


logger = logging.getLogger(__name__)


def require_authentication(required=True):
    def decorator(handler):
        handler.authentication_required = required

        return handler

    return decorator


def get_authentication_required(handler):
    return getattr(handler, 'authentication_required', None)


def authenticate(request):
    account = AuthenticationBackend.get_instance().authenticate(request)
    request[REQUEST_ACCOUNT_KEY] = account

    return account


def get_account(request):
    return request.get(REQUEST_ACCOUNT_KEY)


def login(request, account, persistent):
    logger.debug('logging in account "%s" (persistent=%s)', account, persistent)

    request[REQUEST_ACCOUNT_KEY] = account
    AuthenticationBackend.get_instance().login(request, persistent)


def logout(request):
    account = request.pop(REQUEST_ACCOUNT_KEY, None)
    if account:
        logger.debug('logging out account "%s"', account)
        AuthenticationBackend.get_instance().logout(request)


def process_request(request):
    return AuthenticationBackend.get_instance().process_request(request)


def process_response(request, response):
    return AuthenticationBackend.get_instance().process_response(request, response)


def setup():
    AuthenticationBackend.configure(settings.AUTHENTICATION)
