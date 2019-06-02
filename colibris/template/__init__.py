
import logging
import os

from colibris import settings

from .exceptions import *
from .base import TemplateBackend


PACKAGE_TEMPLATE_PATH = 'templates'

logger = logging.getLogger(__name__)

_backend = None


def render(template_name, **context):
    return TemplateBackend.get_instance().render(template_name, context)


def render_string(template_str, **context):
    return TemplateBackend.get_instance().render_string(template_str, context)


# Prepend package template dir to path array
paths = [os.path.join(settings.PROJECT_PACKAGE_DIR, PACKAGE_TEMPLATE_PATH)] + list(settings.TEMPLATE.get('paths', []))

TemplateBackend.configure(dict(settings.TEMPLATE, paths=paths))
