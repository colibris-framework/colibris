
from colibris.authorization import ANY_PERMISSION
from colibris.authorization.base import AuthorizationBackend


class RoleBackend(AuthorizationBackend):
    def __init__(self, role_field, **kwargs):
        self.role_field = role_field

        super().__init__(**kwargs)

    def get_role(self, account):
        return getattr(account, self.role_field)

    def authorize(self, account, method, path, required_permissions):
        if required_permissions == ANY_PERMISSION:
            return True  # anyone authenticated is authorized

        return self.get_role(account) in required_permissions
