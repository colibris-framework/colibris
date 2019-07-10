
from .model import ModelBackend


# The model is assumed to have the following fields:
#  * account
#  * resource
#  * operation
#
#
# A permission is defined as the right to perform an operation on a resource.
# The format used is "{resource}:{operation}", e.g. "users:r".

class RightsBackend(ModelBackend):
    def __init__(self, resource_field, operation_field, **kwargs):
        self.resource_field = resource_field
        self.operation_field = operation_field

        super().__init__(**kwargs)

    def get_resource_field(self):
        return getattr(self.model, self.resource_field)

    def get_operation(self, right):
        return getattr(right, self.operation_field)

    def authorize(self, account, method, path, required_permissions):
        resource, required_operations = required_permissions.split(':', 1)

        query = (self.get_account_field() == account and
                 self.get_resource_field() == resource)

        # Gather all rights from all entries for the given account and resource;
        allowed_operations = set()
        rights = self.model.select().where(query)
        for right in rights:
            allowed_operations |= set(self.get_operation(right))

        # Consider the request authorized if all required operations are included in allowed operations
        required_operations = set(required_operations)
        return len(required_operations - allowed_operations) == 0
