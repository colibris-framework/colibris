
import pickle
import redis

from colibris.cache.base import CacheBackend, ABSENT


class RedisBackend(CacheBackend):
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self._host = host
        self._port = port
        self._db = db

        self._client = redis.Redis(host=host, port=port, db=db, password=password)

    def get(self, key):
        svalue = self._client.get(key)
        if svalue is None:
            return ABSENT

        return self._load_value(svalue)

    def set(self, key, value, lifetime):
        self._client.setex(key, lifetime, self._dump_value(value))

    def delete(self, key):
        self._client.delete(key)

    def _dump_value(self, value):
        return pickle.dumps(value)

    def _load_value(self, svalue):
        return pickle.loads(svalue)
