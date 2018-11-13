
from colibris import utils
from colibris.authentication.base import AuthenticationBackend


class ModelBackend(AuthenticationBackend):
    def __init__(self, model, identity_field, secret_field, **kwargs):
        self.model = utils.import_member(model)
        self.identity_field = identity_field
        self.secret_field = secret_field

        super().__init__(**kwargs)

    def lookup_account(self, identity):
        query = self.get_identity_field() == identity
        try:
            return self.model.select().where(query).get()

        except self.model.DoesNotExist:
            return None

    def get_identity_field(self):
        return getattr(self.model, self.identity_field)

    def get_secret(self, account):
        return getattr(account, self.secret_field)
