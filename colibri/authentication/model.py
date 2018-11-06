
from colibri import utils
from colibri.authentication.base import AuthenticationBackend


class ModelBackend(AuthenticationBackend):
    def __init__(self, model, identity_field, secret_field, **kwargs):
        self.model = utils.import_member(model)
        self.identity_field = identity_field
        self.secret_field = secret_field

        super().__init__(**kwargs)

    def lookup_account(self, identity):
        query = getattr(self.model, self.identity_field) == identity
        try:
            return self.model.select().where(query).get()

        except self.model.DoesNotExist:
            return None

    def extract_secret(self, account):
        return getattr(account, self.secret_field)
