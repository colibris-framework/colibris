
class AuthorizationBackend:
    def authorize(self, account, permissions):
        raise NotImplementedError


class NullBackend(AuthorizationBackend):
    def authorize(self, account, permissions):
        return True
