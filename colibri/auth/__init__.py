
from colibri import settings
from colibri import utils


class AuthException(Exception):
    pass


class NoSuchAccount(AuthException):
    pass


class IdentityVerificationFailed(AuthException):
    pass


class AuthenticationBackend:
    _ACCOUNT_MODEL = None
    if settings.AUTHENTICATION.get('model'):
        _ACCOUNT_MODEL = utils.import_member(settings.AUTHENTICATION['model'])

    def extract_auth_data(self, request):
        raise NotImplementedError

    def lookup_account(self, identity):
        if self._ACCOUNT_MODEL:
            query = {settings.AUTHENTICATION['identity_field']: identity}
            try:
                return self._ACCOUNT_MODEL.select().where(**query).get()

            except self._ACCOUNT_MODEL.DoesNotExist:
                return None

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
