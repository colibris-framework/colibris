
from colibris.conf.backends import BackendMixin


ABSENT = object()


class CacheBackend(BackendMixin):
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, lifetime):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
