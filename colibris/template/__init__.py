
import logging
import os

from colibris import settings
from colibris import utils

from .exceptions import *


PACKAGE_TEMPLATE_PATH = 'templates'

logger = logging.getLogger(__name__)

_backend = None


def get_backend():
    global _backend

    if _backend is None:
        backend_settings = dict(settings.TEMPLATE)
        backend_path = backend_settings.pop('backend', None)
        if backend_path is None:
            raise TemplateNotConfigured()

        # inject package dir into path array
        paths = backend_settings.get('paths', [])
        paths = [os.path.join(settings.PROJECT_PACKAGE_DIR, PACKAGE_TEMPLATE_PATH)] + list(paths)
        backend_settings['paths'] = paths

        backend_class = utils.import_member(backend_path)
        _backend = backend_class(**backend_settings)

        logger.debug('backend of class %s created', backend_path)

    return _backend


def render(template_name, **context):
    return get_backend().render(template_name, context)


def render_string(template_str, **context):
    return get_backend().render_string(template_str, context)
