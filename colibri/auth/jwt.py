
import jwt
import re

from . import AuthException, AuthenticationBackend as BaseAuthenticationBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class JWTException(AuthException):
    pass


class AuthenticationBackend(BaseAuthenticationBackend):
    def __init__(self, identity_claim, **kwargs):
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

    def verify_identity(self, secret, account, auth_data):
        try:
            jwt.decode(auth_data, key=secret, verify=True)

        except jwt.InvalidSignatureError:
            return False

        return True
