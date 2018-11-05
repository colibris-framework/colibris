
from colibri import utils


class AuthException(Exception):
    pass


class NoSuchAccount(AuthException):
    pass


class IdentityVerificationFailed(AuthException):
    pass


class AuthenticationBackend:
    def __init__(self, model=None, identity_field=None, secret_field=None):
        self.model = None
        if model:
            self.model = utils.import_member(model)

        self.identity_field = identity_field
        self.secret_field = secret_field

    def extract_auth_data(self, request):
        raise NotImplementedError

    def lookup_account(self, identity):
        if self.model:
            query = {self.identity_field: identity}
            try:
                return self.model.select().where(**query).get()

            except self.model.DoesNotExist:
                return None

    def verify_identity(self, secret, account, auth_data):
        raise NotImplementedError

    def authenticate(self, request):
        identity, auth_data = self.extract_auth_data(request)
        account = self.lookup_account(identity)
        if account is None:
            raise NoSuchAccount()

        if hasattr(account, '__getitem__'):  # dict-like account
            secret = account[self.secret_field]

        else:  # assuming regular attribute
            secret = getattr(account, self.secret_field)

        if not self.verify_identity(secret, account, auth_data):
            raise IdentityVerificationFailed()

        return account
