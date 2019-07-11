
from colibris.conf.backends import BackendMixin


class AuthorizationBackend(BackendMixin):
    def get_actual_permissions(self, account, method, path):
        raise NotImplementedError

    def authorize(self, account, method, path, handler, required_permissions):
        actual_permissions = self.get_actual_permissions(account, method, path)
        required_permissions.verify(actual_permissions)
