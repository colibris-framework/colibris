
import logging

from colibris import settings
from colibris import utils


DEFAULT_LIFETIME = 300  # seconds

logger = logging.getLogger(__name__)

_backend = None
_default_lifetime = None


def get_backend():
    global _backend, _default_lifetime

    if _backend is None:
        backend_settings = dict(settings.CACHE or {})
        backend_path = backend_settings.pop('backend', 'colibris.cache.LocMemBackend')
        backend_class = utils.import_member(backend_path)
        _default_lifetime = backend_settings.pop('default_lifetime', DEFAULT_LIFETIME)
        _backend = backend_class(**backend_settings)

        logger.debug('backend of class %s created', backend_path)

    return _backend


def get(key, default=None):
    return get_backend().get(key, default)


def set(key, value, lifetime=None):
    lifetime = lifetime or _default_lifetime

    get_backend().set(key, value, lifetime)


def delete(key):
    get_backend().delete(key)
