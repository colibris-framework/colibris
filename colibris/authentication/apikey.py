
import re

from .exceptions import AuthenticationException
from .model import ModelBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class ApiKeyException(AuthenticationException):
    pass


class APIKeyBackend(ModelBackend):
    def __init__(self, key_field, **kwargs):
        self.key_field = key_field

        super().__init__(**kwargs)

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

    def get_lookup_value(self, auth_data):
        return auth_data

    def get_lookup_field(self):
        return getattr(self.model, self.key_field)
