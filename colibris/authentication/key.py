import re

from colibris.authentication.exceptions import AuthenticationException
from colibris.authentication.model import ModelBackend

_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class ApiKeyException(AuthenticationException):
    pass


class ApiKeyBackend(ModelBackend):
    def extract_auth_data(self, request):
        token = None

        auth_header = request.headers.get(_AUTH_HEADER)
        if auth_header is not None:
            m = _AUTH_TOKEN_REGEX.match(auth_header)
            if not m:
                raise ApiKeyException('Invalid authorization header')

            token = m.group(1)

        if not token:
            raise ApiKeyException('Missing token')

        return token

    def authenticate(self, request):
        identity = self.extract_auth_data(request)
        account = self.lookup_account(identity)

        if account is None:
            raise ApiKeyException('Account not known')

        return account
