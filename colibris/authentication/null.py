
from .base import AuthenticationBackend


class NullBackend(AuthenticationBackend):
    _DUMMY_ACCOUNT = {}

    def __init__(self, **kwargs):
        pass

    def extract_auth_data(self, request):
        return None, None

    def lookup_account(self, identity):
        return self._DUMMY_ACCOUNT

    def verify_identity(self, request, account, auth_data):
        pass

    def authenticate(self, request):
        return self._DUMMY_ACCOUNT
