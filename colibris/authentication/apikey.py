import re

from colibris.authentication.exceptions import AuthenticationException
from colibris.authentication.model import ModelBackend

_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class ApiKeyException(AuthenticationException):
    pass


class APIKeyBackend(ModelBackend):
    def extract_auth_data(self, request):
        token = None

        auth_header = request.headers.get(_AUTH_HEADER)
        if auth_header is not None:
            m = _AUTH_TOKEN_REGEX.match(auth_header)
            if not m:
                raise ApiKeyException('invalid authorization header')

            token = m.group(1)

        if not token:
            raise ApiKeyException('missing token')

        return token

    def get_identity_value(self, auth_data):
        return auth_data
