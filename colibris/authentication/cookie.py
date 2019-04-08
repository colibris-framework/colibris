
from http.cookies import Morsel

from colibris import settings
from colibris.authentication.exceptions import AuthenticationException

DEFAULT_VALIDITY_SECONDS = 3600 * 24 * 30


class CookieException(AuthenticationException):
    pass


class CookieBackendMixin:
    def __init__(self, cookie_name=None, validity_seconds=DEFAULT_VALIDITY_SECONDS, **kwargs):
        self.cookie_name = cookie_name
        self.validity_seconds = validity_seconds

    def cookie_login(self, response, persistent, token):
        if not self.cookie_name:
            raise CookieException('login attempt without a configured cookie name')

        cookie = Morsel()
        cookie.set(self.cookie_name, token, token)
        cookie['httponly'] = True
        cookie['secure'] = not settings.DEBUG
        #cookie['domain'] = settings.ROOT_DOMAIN  # TODO define me
        cookie['path'] = '/'

        if persistent:
            cookie['expires'] = self.validity_seconds

        response.cookies[self.cookie_name] = cookie

    def cookie_logout(self, response):
        if not self.cookie_name:
            raise CookieException('logout attempt without a configured cookie name')

        cookie = Morsel()
        cookie.set(self.cookie_name, 'invalid', 'invalid')
        cookie['httponly'] = True
        cookie['secure'] = not settings.DEBUG
        #cookie['domain'] = settings.ROOT_DOMAIN  # TODO define me
        cookie['path'] = '/'
        cookie['expires'] = 0

        response.cookies[self.cookie_name] = cookie
