
import importlib
import inspect
import os
import re
import sys

from pathlib import Path
from dotenv import load_dotenv
from marshmallow import Schema, fields, EXCLUDE

from colibris import defaultsettings


# default values
from colibris.defaultsettings import *


class EnvVarsValidator(Schema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    DATABASE = fields.String()

    class Meta:
        unknown = EXCLUDE


def _is_setting_name(name):
    # only consider public members that are all in capitals
    return re.match('^[A-Z][A-Z0-9_]*$', name)


def _override_project_settings(settings):
    try:
        project_settings_module = importlib.import_module('settings')

    except ImportError:
        return

    for name, value in inspect.getmembers(project_settings_module):
        if not _is_setting_name(name):
            continue

        setattr(settings, name, value)


def _override_settings_local(settings):
    try:
        settings_local_module = importlib.import_module('settingslocal')

    except ImportError:
        return

    for name, value in inspect.getmembers(settings_local_module):
        if not _is_setting_name(name):
            continue

        setattr(settings, name, value)


def _override_env_settings(settings):
    load_dotenv(Path('.env.default'))
    load_dotenv(Path('.env'), override=True)

    env_vars = EnvVarsValidator().load(os.environ)

    for name, value in env_vars.items():
        if value is not None:
            setattr(settings, name, value)


def _apply_tweaks(settings):
    # update default log level according to DEBUG flag

    if settings.LOGGING is defaultsettings.LOGGING and not DEBUG:
        LOGGING['root']['level'] = 'INFO'


# override settings

_this_module = sys.modules[__name__]
_override_project_settings(_this_module)
_override_settings_local(_this_module)
_override_env_settings(_this_module)


# some final adjustments

_apply_tweaks(_this_module)


# set project-related variables

try:
    PROJECT_PACKAGE = importlib.import_module(PROJECT_PACKAGE_NAME)

except ImportError:
    PROJECT_PACKAGE = importlib.import_module('colibris')

PROJECT_PACKAGE_DIR = os.path.dirname(PROJECT_PACKAGE.__file__)
