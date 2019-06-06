
from colibris.conf.backends import BackendMixin


class AuthorizationBackend(BackendMixin):
    def authorize(self, account, method, path, required_permissions):
        raise NotImplementedError
