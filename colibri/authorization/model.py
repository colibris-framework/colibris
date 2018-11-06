
from colibri import utils
from colibri.authorization.base import AuthorizationBackend


class ModelBackend(AuthorizationBackend):
    def __init__(self, model, account_field, permissions_field, **kwargs):
        self.model = utils.import_member(model)
        self.account_field = account_field
        self.permissions_field = permissions_field

        super().__init__(**kwargs)

    def authorize(self, account, permissions):
        query = getattr(self.model, self.account_field) == account

        if permissions != '*':
            # permissions are given as a set of letters
            query = query and getattr(self.model, self.permissions_field) == permissions

        return len(self.model.select().where(query)) > 0
