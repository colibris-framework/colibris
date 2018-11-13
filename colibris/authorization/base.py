
from colibris.authorization import ANY_PERMISSION


class AuthorizationBackend:
    def authorize(self, account, method, path, required_permissions):
        # by default, when "any" permission is fine,
        # consider any authenticated request authorized

        return required_permissions == ANY_PERMISSION


class NullBackend(AuthorizationBackend):
    def authorize(self, account, method, path, required_permissions):
        # consider any authenticated request authorized

        return True
