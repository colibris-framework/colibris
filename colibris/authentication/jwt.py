
import jwt
import re

from colibris.authentication.exceptions import AuthenticationException
from colibris.authentication.model import ModelBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class JWTException(AuthenticationException):
    pass


class JWTBackend(ModelBackend):
    def __init__(self, identity_claim='sub', **kwargs):
        self.identity_claim = identity_claim

        super().__init__(**kwargs)

    def extract_auth_data(self, request):
        auth_header = request.headers.get(_AUTH_HEADER)
        if auth_header is None:
            raise JWTException('missing authorization header')

        m = _AUTH_TOKEN_REGEX.match(auth_header)
        if not m:
            raise JWTException('invalid authorization header')

        token = m.group(1)

        try:
            jwt_decoded = jwt.decode(token, verify=False)

        except jwt.DecodeError:
            raise JWTException('invalid authorization header')

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
