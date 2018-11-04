
from . import AuthenticationBackend as BaseAuthenticationBackend


class AuthenticationBackend(BaseAuthenticationBackend):
    _DUMMY_ACCOUNT = {}

    def extract_auth_data(self, request):
        return None, None

    def lookup_account(self, identity):
        return self._DUMMY_ACCOUNT

    def verify_identity(self, account, identity, auth_data):
        return True
