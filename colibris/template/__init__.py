
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


def setup():
    template_settings = dict(settings.TEMPLATE)
    package_template_path = os.path.join(settings.PROJECT_PACKAGE_DIR, PACKAGE_TEMPLATE_PATH)

    # Prepend package template dir to path array
    template_settings['path'] = [package_template_path] + list(template_settings.get('paths', []))

    TemplateBackend.configure(template_settings)
