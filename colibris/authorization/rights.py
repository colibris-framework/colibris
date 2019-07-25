
from .model import ModelBackend


# The model is assumed to have the following fields:
#  * account
#  * resource
#  * operation
#
# A permission is defined as the right to perform an operation on a resource.
# The format used is "{resource}:{operation}", e.g. "users:update".

class RightsBackend(ModelBackend):
    def __init__(self, resource_field, operation_field, **kwargs):
        self.resource_field = resource_field
        self.operation_field = operation_field

        super().__init__(**kwargs)

    def get_resource(self, right):
        return getattr(right, self.resource_field)

    def get_operation(self, right):
        return getattr(right, self.operation_field)

    def get_actual_permissions(self, account, method, path):
        # Gather all rights from all entries for the given account
        rights = self.model.select().where(self.get_account_field() == account)

        return {'{}:{}'.format(self.get_resource(r), self.get_operation(r)) for r in rights}
