
import jwt
import re
import time

from colibris.authentication.cookie import CookieBackendMixin
from colibris.authentication.exceptions import AuthenticationException
from colibris.authentication.model import ModelBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)

DEFAULT_VALIDITY_SECONDS = 3600 * 24 * 30
JWT_ALG = 'HS256'


class JWTException(AuthenticationException):
    pass


class JWTBackend(ModelBackend, CookieBackendMixin):
    def __init__(self, identity_claim='sub', **kwargs):
        self.identity_claim = identity_claim

        super().__init__(**kwargs)

    def extract_auth_data(self, request):
        token = None

        # First look for auth header
        auth_header = request.headers.get(_AUTH_HEADER)
        if auth_header is not None:
            m = _AUTH_TOKEN_REGEX.match(auth_header)
            if not m:
                raise JWTException('invalid authorization header')

            token = m.group(1)

        # Then look in cookies
        elif self.cookie_name:
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

    def response_login(self, response, account, persistent):
        self.cookie_login(response, persistent, self.build_jwt(account))

        return response

    def response_logout(self, response):
        self.cookie_logout(response)

        return response

    def build_jwt(self, account):
        now = int(time.time())
        token_claims = {
            'sub': str(account),
            'iat': now,
            'exp': now + self.validity_seconds
        }

        return jwt.encode(algorithm=JWT_ALG, payload=token_claims, key=self.get_secret(account)).decode()
