
import time

from colibris.cache.base import CacheBackend, ABSENT


DEFAULT_MAX_ENTRIES = 1e5


class LocMemBackend(CacheBackend):
    def __init__(self, max_entries=DEFAULT_MAX_ENTRIES):
        self.max_entries = max_entries
        self.store = {}

    def get(self, key):
        entry = self.store.get(key, ABSENT)
        if entry is ABSENT:
            return ABSENT

        added, lifetime, value = entry
        if time.time() - added > lifetime:  # entry expired
            self.store.pop(key, None)
            return ABSENT

        return value

    def set(self, key, value, lifetime):
        # clean up expired entries as soon as we hit the limit
        if len(self.store) >= self.max_entries:
            self._cleanup_expired()

        # remove random elements until we have enough room
        while len(self.store) >= self.max_entries:
            self.store.popitem()

        self.store[key] = time.time(), lifetime, value

    def delete(self, key):
        self.store.pop(key, None)

    def _cleanup_expired(self):
        expired_keys = []
        now = time.time()
        for key, (added, lifetime, value) in self.store.items():
            if now - added > lifetime:
                expired_keys.append(key)

        for key in expired_keys:
            self.store.pop(key)
