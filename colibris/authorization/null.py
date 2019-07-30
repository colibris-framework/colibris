
from .base import AuthorizationBackend


class NullBackend(AuthorizationBackend):
    def __init__(self, **kwargs):
        pass

    def authorize(self, account, method, path, handler, required_permissions):
        # Consider any authenticated request authorized

        return True

    def get_actual_permissions(self, account, method, path):
        return set()
