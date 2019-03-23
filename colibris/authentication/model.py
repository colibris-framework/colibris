
from colibris import utils
from colibris.authentication.base import AuthenticationBackend


class ModelBackend(AuthenticationBackend):
    def __init__(self, model, identity_field, secret_field, active_field=None, inactive_field=None, **kwargs):
        self.model = utils.import_member(model)
        self.identity_field = identity_field
        self.secret_field = secret_field
        self.active_field = active_field
        self.inactive_field = inactive_field

        super().__init__(**kwargs)

    def lookup_account(self, identity):
        query = self.get_identity_field() == identity
        if self.active_field:
            query = query & (self.get_active_field() == True)

        if self.inactive_field:
            query = query & (self.get_inactive_field() == False)

        try:
            return self.model.select().where(query).get()

        except self.model.DoesNotExist:
            return None

    def get_identity_field(self):
        return getattr(self.model, self.identity_field)

    def get_active_field(self):
        return getattr(self.model, self.active_field)

    def get_inactive_field(self):
        return getattr(self.model, self.inactive_field)

    def get_secret(self, account):
        return getattr(account, self.secret_field)
