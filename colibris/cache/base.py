
ABSENT = object()


class CacheBackend:
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, lifetime):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
