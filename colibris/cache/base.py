
class CacheBackend:
    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value, lifetime):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
