
from http.cookies import Morsel

from colibris.authentication.exceptions import AuthenticationException
from colibris import settings


DEFAULT_VALIDITY_SECONDS = 3600 * 24 * 30
DEFAULT_COOKIE_NAME = 'auth_token'


class JWTException(AuthenticationException):
    pass


class CookieBackendMixin:
    def __init__(self, cookie_name=DEFAULT_COOKIE_NAME, validity_seconds=DEFAULT_VALIDITY_SECONDS, **kwargs):
        self.cookie_name = cookie_name
        self.validity_seconds = validity_seconds

    def cookie_login(self, request, persistent, token):
        cookie = Morsel()
        cookie.set(self.cookie_name, token, token)
        cookie['httponly'] = True
        cookie['secure'] = not settings.DEBUG
        #cookie['domain'] = settings.ROOT_DOMAIN  # TODO define me
        cookie['path'] = '/'

        if persistent:
            cookie['expires'] = self.validity_seconds

        request.cookies[self.cookie_name] = cookie

    def cookie_logout(self, request):
        cookie = Morsel()
        cookie.set(self.cookie_name, 'invalid', 'invalid')
        cookie['httponly'] = True
        cookie['secure'] = not settings.DEBUG
        #cookie['domain'] = settings.ROOT_DOMAIN  # TODO define me
        cookie['path'] = '/'
        cookie['expires'] = 0

        request.cookies[self.cookie_name] = cookie
