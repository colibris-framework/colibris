
from .base import AuthorizationBackend


# A permission is defined as the role of an account.
#
# The optional ordering defines a relation between roles; this allows specifying e.g. "admin" as required permission
# and assuming that it also has "regular" and "viewonly" permissions, without explicitly requiring them.

class RoleBackend(AuthorizationBackend):
    def __init__(self, role_field, order=None, **kwargs):
        self.role_field = role_field
        self.order = order or []  # lower first, e.g. ["readonly", "regular", "admin"]

        super().__init__(**kwargs)

    def get_role(self, account):
        return getattr(account, self.role_field)

    def get_actual_permissions(self, account, method, path):
        role = self.get_role(account)
        actual_permissions = {role}

        try:
            index = self.order.index(role)

        except ValueError:
            index = 0

        actual_permissions.update(self.order[:index])

        return actual_permissions
