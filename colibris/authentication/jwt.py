
import jwt
import re
import time

from .cookie import CookieBackendMixin
from .exceptions import AuthenticationException
from .model import ModelBackend


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)

DEFAULT_VALIDITY_SECONDS = 3600 * 24 * 30
JWT_ALG = 'HS256'


class JWTException(AuthenticationException):
    pass


class JWTBackend(ModelBackend, CookieBackendMixin):
    def __init__(self, identity_field, secret_field, identity_claim='sub', **kwargs):
        self.identity_claim = identity_claim
        self.identity_field = identity_field
        self.secret_field = secret_field

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

        return {
            'identity': identity,
            'token': token
        }

    def get_lookup_value(self, auth_data):
        return auth_data['identity']

    def get_lookup_field(self):
        return getattr(self.model, self.identity_field)

    def verify_identity(self, request, account, auth_data):
        secret = self.get_secret(account)

        try:
            jwt.decode(auth_data['token'], key=secret, verify=True)

        except jwt.InvalidSignatureError:
            raise JWTException('invalid signature')

        if self.is_csrf_enabled():
            self.verify_csrf(request, account)

    def prepare_login_response(self, response, account, persistent):
        self.cookie_login(response, persistent, self.build_jwt(account))

        return response

    def prepare_logout_response(self, response):
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

    def process_response(self, request, response):
        response = super().process_response(request, response)

        if self.is_csrf_enabled():
            self.set_csrf(request, response)

        return response

    def get_secret(self, account):
        return getattr(account, self.secret_field)
