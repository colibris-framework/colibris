
from colibris.conf.backends import BackendMixin


class AuthorizationBackend(BackendMixin):
    def get_actual_permissions(self, account, method, path):
        raise NotImplementedError

    def authorize(self, account, method, path, handler, required_permissions):
        required_permissions.verify(self.get_actual_permissions(account, method, path))
