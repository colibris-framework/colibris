
class AuthorizationBackend:
    def authorize(self, account, method, path, required_permissions):
        raise NotImplementedError


class NullBackend(AuthorizationBackend):
    def authorize(self, account, method, path, required_permissions):
        return True
