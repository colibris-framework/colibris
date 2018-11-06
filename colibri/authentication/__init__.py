
from colibri import utils


class AuthenticationException(Exception):
    def __str__(self):
        message = super().__str__()
        if not message:
            message = self.__class__.__name__

        return message


class NoSuchAccount(AuthenticationException):
    pass


class IdentityVerificationFailed(AuthenticationException):
    pass


class AuthenticationBackend:
    def extract_auth_data(self, request):
        raise NotImplementedError

    def lookup_account(self, identity):
        raise NotImplementedError

    def verify_identity(self, account, auth_data):
        raise NotImplementedError

    def authenticate(self, request):
        identity, auth_data = self.extract_auth_data(request)
        account = self.lookup_account(identity)
        if account is None:
            raise NoSuchAccount()

        if not self.verify_identity(account, auth_data):
            raise IdentityVerificationFailed()

        return account


class NullBackend(AuthenticationBackend):
    _DUMMY_ACCOUNT = {}

    def extract_auth_data(self, request):
        return None, None

    def lookup_account(self, identity):
        return self._DUMMY_ACCOUNT

    def verify_identity(self, secret, account, auth_data):
        return True

    def authenticate(self, request):
        return self._DUMMY_ACCOUNT
