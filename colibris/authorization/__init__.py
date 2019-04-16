
import logging

from colibris import settings
from colibris import utils


ANY_PERMISSION = '*'

logger = logging.getLogger(__name__)

_backend = None


def get_backend():
    global _backend

    if _backend is None:
        backend_settings = dict(settings.AUTHORIZATION)
        backend_path = backend_settings.pop('backend', 'colibris.authorization.base.NullBackend')
        backend_class = utils.import_member(backend_path)

        logger.debug('creating backend of class %s', backend_path)

        _backend = backend_class(**backend_settings)

    return _backend


def authorize(account, method, path, authorization_info):
    return get_backend().authorize(account, method, path, authorization_info)
