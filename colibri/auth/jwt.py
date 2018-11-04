
import jwt
import re

from . import AuthException, AuthenticationBackend as BaseAuthenticationBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)


class JWTException(AuthException):
    pass


class AuthenticationBackend(BaseAuthenticationBackend):
    def __init__(self, identity_claim, secret_field, **kwargs):
        self.identity_claim = identity_claim
        self.secret_field = secret_field

        super().__init__()

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
        if hasattr(account, '__getitem__'):  # dict-like account
            secret = account[self.secret_field]

        else:  # assuming regular attribute
            secret = getattr(account, self.secret_field)

        try:
            jwt.decode(auth_data, key=secret, verify=True)

        except jwt.InvalidSignatureError:
            return False

        return True
