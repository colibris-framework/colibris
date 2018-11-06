
from colibri import utils
from colibri.authorization.base import AuthorizationBackend


class ModelBackend(AuthorizationBackend):
    def __init__(self, model, account_field, resource_field, operations_field, **kwargs):
        self.model = utils.import_member(model)
        self.account_field = account_field
        self.resource_field = resource_field
        self.operations_field = operations_field

        super().__init__(**kwargs)

    def authorize(self, account, method, path, required_permissions):
        if required_permissions == '*':
            return True  # anyone authenticated is authorized

        resource, required_operations = required_permissions.split(':', 1)

        query = (getattr(self.model, self.account_field) == account and
                 getattr(self.model, self.resource_field) == resource)

        # gather all permissions from all entries for the given account and resource;
        allowed_operations = set()
        permissions = self.model.select().where(query)
        for permission in permissions:
            allowed_operations |= set(getattr(permission, self.operations_field))

        # consider the request authorized if all required operations are included in allowed operations
        required_operations = set(required_operations)
        return len(required_operations - allowed_operations) == 0
