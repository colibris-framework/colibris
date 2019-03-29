
import jwt
import re

from colibris.authentication.exceptions import AuthenticationException
from colibris.authentication.model import ModelBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class JWTException(AuthenticationException):
    pass


class JWTBackend(ModelBackend):
    def __init__(self, identity_claim='sub', cookie_name=None, **kwargs):
        self.identity_claim = identity_claim
        self.cookie_name = cookie_name

        super().__init__(**kwargs)

    def extract_auth_data(self, request):
        token = None

        auth_header = request.headers.get(_AUTH_HEADER)
        if auth_header is not None:  # First look for auth header.
            m = _AUTH_TOKEN_REGEX.match(auth_header)
            if not m:
                raise JWTException('invalid authorization header')

            token = m.group(1)

        elif self.cookie_name:  # Then look in cookies.
            token = request.cookies.get(self.cookie_name)

        if not token:
            raise JWTException('missing token')

        try:
            jwt_decoded = jwt.decode(token, verify=False)

        except jwt.DecodeError:
            raise JWTException('invalid token')

        identity = jwt_decoded.get(self.identity_claim)
        if identity is None:
            raise JWTException('missing identity claim')

        return identity, token

    def verify_identity(self, account, auth_data):
        secret = self.get_secret(account)

        try:
            jwt.decode(auth_data, key=secret, verify=True)

        except jwt.InvalidSignatureError:
            return False

        return True
