
from . import ANY_PERMISSION
from .model import ModelBackend


class RightsBackend(ModelBackend):
    def __init__(self, resource_field, operations_field, **kwargs):
        self.resource_field = resource_field
        self.operations_field = operations_field

        super().__init__(**kwargs)

    def get_resource_field(self):
        return getattr(self.model, self.resource_field)

    def get_operations(self, right):
        return getattr(right, self.operations_field)

    def authorize(self, account, method, path, required_permissions):
        if required_permissions == ANY_PERMISSION:
            return True

        resource, required_operations = required_permissions.split(':', 1)

        query = (self.get_account_field() == account and
                 self.get_resource_field() == resource)

        # gather all rights from all entries for the given account and resource;
        allowed_operations = set()
        rights = self.model.select().where(query)
        for right in rights:
            allowed_operations |= set(self.get_operations(right))

        # consider the request authorized if all required operations are included in allowed operations
        required_operations = set(required_operations)
        return len(required_operations - allowed_operations) == 0
