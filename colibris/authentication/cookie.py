
import hashlib
import hmac

from http.cookies import Morsel

from colibris.conf import settings
from colibris.api.exceptions import BaseJSONException

from . import get_account
from .exceptions import AuthenticationException


DEFAULT_VALIDITY_SECONDS = 3600 * 24 * 30
SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS', 'TRACE'}

_REQUEST_CSRF_TOKEN_ITEM_NAME = 'csrf_token'
_SECRET_KEY = settings.SECRET_KEY.encode() if settings.SECRET_KEY else b''


class CookieException(AuthenticationException):
    pass


class CSRFValidationException(BaseJSONException):
    def __init__(self):
        super().__init__(code='forbidden', message='CSRF token is either invalid or missing.', status=403)


class CookieBackendMixin:
    def __init__(self, cookie_name=None, cookie_domain=None, validity_seconds=DEFAULT_VALIDITY_SECONDS,
                 csrf_token_cookie_name=None, csrf_token_header_name=None, **kwargs):

        self.cookie_name = cookie_name
        self.cookie_domain = cookie_domain
        self.validity_seconds = validity_seconds
        self.csrf_token_cookie_name = csrf_token_cookie_name
        self.csrf_token_header_name = csrf_token_header_name

    def is_csrf_enabled(self):
        return bool(self.csrf_token_cookie_name and self.csrf_token_header_name)

    def cookie_login(self, response, persistent, token):
        if not self.cookie_name:
            raise CookieException('login attempt without a configured cookie name')

        cookie = Morsel()
        cookie.set(self.cookie_name, token, token)
        cookie['httponly'] = True
        cookie['secure'] = not settings.DEBUG
        cookie['path'] = '/'
        if self.cookie_domain:
            cookie['domain'] = self.cookie_domain

        if persistent:
            cookie['expires'] = self.validity_seconds

        response.cookies[self.cookie_name] = cookie

    def cookie_logout(self, response):
        if not self.cookie_name:
            raise CookieException('logout attempt without a configured cookie name')

        self.clear_cookie(response, self.cookie_name)
        if self.csrf_token_cookie_name:
            self.clear_cookie(response, self.csrf_token_cookie_name)

    def clear_cookie(self, response, name):
        cookie = Morsel()
        cookie.set(name, 'invalid', 'invalid')
        cookie['httponly'] = True
        cookie['secure'] = not settings.DEBUG
        cookie['path'] = '/'
        cookie['expires'] = 0
        if self.cookie_domain:
            cookie['domain'] = self.cookie_domain

        response.cookies[name] = cookie

    def verify_csrf(self, request, account):
        # Skip verification for safe methods
        if request.method in SAFE_METHODS:
            return

        try:
            incoming_csrf_token = request.headers[self.csrf_token_header_name]

        except KeyError:
            raise CSRFValidationException()

        expected_csrf_token = self.get_csrf_token(request, account)

        if incoming_csrf_token != expected_csrf_token:
            raise CSRFValidationException()

    def set_csrf(self, request, response):
        token = self.get_csrf_token(request)
        if not token:
            return

        cookie = Morsel()
        cookie.set(self.csrf_token_cookie_name, token, token)
        cookie['secure'] = not settings.DEBUG
        cookie['path'] = '/'
        if self.cookie_domain:
            cookie['domain'] = self.cookie_domain

        response.cookies['csrf_token'] = cookie

    @staticmethod
    def get_csrf_token(request, account=None):
        token = request.get(_REQUEST_CSRF_TOKEN_ITEM_NAME)
        if token:
            return token

        account = account or get_account(request)
        if account is None:
            return

        account_id = str(account).encode()
        token = hmac.new(_SECRET_KEY, account_id, hashlib.sha256).hexdigest()

        request[_REQUEST_CSRF_TOKEN_ITEM_NAME] = token

        return token
