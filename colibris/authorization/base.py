
from colibris.conf.backends import BackendMixin

from .permissions import verify_permissions


class AuthorizationBackend(BackendMixin):
    def get_actual_permissions(self, account, method, path):
        raise NotImplementedError

    def authorize(self, account, method, path, required_permissions):
        actual_permissions = self.get_actual_permissions(account, method, path)
        verify_permissions(actual_permissions, required_permissions)
