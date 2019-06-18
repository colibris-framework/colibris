
import logging

from colibris.conf import settings

from .base import ABSENT
from .base import CacheBackend


DEFAULT_LIFETIME = 300  # seconds

logger = logging.getLogger(__name__)

_default_lifetime = None


def get(key, default=None):
    value = CacheBackend.get_instance().get(key)
    if value is ABSENT:
        return default

    return value


def set(key, value, lifetime=None):
    lifetime = lifetime or _default_lifetime

    CacheBackend.get_instance().set(key, value, lifetime)


def delete(key):
    CacheBackend.get_instance().delete(key)


def setup():
    global _default_lifetime

    cache_settings = dict(settings.CACHE)
    _default_lifetime = cache_settings.pop('default_lifetime', DEFAULT_LIFETIME)

    CacheBackend.configure(cache_settings)


def is_enabled():
    return CacheBackend.is_enabled()


def is_created():
    return CacheBackend.is_created()
