
from colibris import utils

from .base import AuthenticationBackend


class ModelBackend(AuthenticationBackend):
    def __init__(self, model, active_field=None, inactive_field=None, **kwargs):
        self.model = utils.import_member(model)
        self.active_field = active_field
        self.inactive_field = inactive_field

        super().__init__(**kwargs)

    def lookup_account(self, auth_data):
        value = self.get_lookup_value(auth_data)
        field = self.get_lookup_field()
        query = (field == value)

        if self.active_field:
            query = query & (self.get_active_field() == True)  # noqa: E712

        if self.inactive_field:
            query = query & (self.get_inactive_field() == False)  # noqa: E712

        try:
            return self.model.select().where(query).get()

        except self.model.DoesNotExist:
            return None

    def get_lookup_field(self):
        raise NotImplementedError

    def get_lookup_value(self, auth_data):
        raise NotImplementedError

    def get_active_field(self):
        return getattr(self.model, self.active_field)

    def get_inactive_field(self):
        return getattr(self.model, self.inactive_field)
