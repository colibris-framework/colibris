
from .base import AuthorizationBackend


class NullBackend(AuthorizationBackend):
    def __init__(self, **kwargs):
        pass

    def authorize(self, account, method, path, required_permissions):
        # Consider any authenticated request authorized

        return True
