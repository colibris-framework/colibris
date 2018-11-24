
import importlib
import inspect
import os
import re
import sys

from pathlib import Path
from dotenv import load_dotenv
from marshmallow import Schema, fields, EXCLUDE


# default values

PROJECT_PACKAGE_NAME = 'projectname'

DEBUG = True

LISTEN = '0.0.0.0'
PORT = 8888

MIDDLEWARE = [
    'colibris.middleware.handle_errors_json',
    'colibris.middleware.handle_auth',
    'colibris.middleware.handle_schema_validation',
]

AUTHENTICATION = None
AUTHORIZATION = None

CACHE = None

API_DOCS_PATH = '/api/docs'

DATABASE = 'sqlite:///__projectname__.db'

LOGGING = _DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s: %(levelname)7s: [%(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    },
    'loggers': {
        'peewee_migrate': {
            'level': 'DEBUG'  # always show details when doing migrations
        }
    }
}


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


def _override_project_settings(this_module):
    try:
        project_settings_module = importlib.import_module('settings')

    except ImportError:
        return

    for name, value in inspect.getmembers(project_settings_module):
        if not _is_setting_name(name):
            continue

        setattr(this_module, name, value)


def _override_settings_local(this_module):
    try:
        settings_local_module = importlib.import_module('settingslocal')

    except ImportError:
        return

    for name, value in inspect.getmembers(settings_local_module):
        if not _is_setting_name(name):
            continue

        setattr(this_module, name, value)


def _override_env_settings(this_module):
    load_dotenv(Path('.env.default'))
    load_dotenv(Path('.env'), override=True)

    env_vars = EnvVarsValidator().load(os.environ)

    for name, value in env_vars.items():
        if value is not None:
            setattr(this_module, name, value)


def _apply_tweaks():
    # update default log level according to DEBUG flag

    if LOGGING is _DEFAULT_LOGGING and not DEBUG:
        LOGGING['root']['level'] = 'INFO'


# override settings

_this_module = sys.modules[__name__]
_override_project_settings(_this_module)
_override_settings_local(_this_module)
_override_env_settings(_this_module)


# some final adjustments

_apply_tweaks()


# set project-related variables

try:
    PROJECT_PACKAGE = importlib.import_module(PROJECT_PACKAGE_NAME)

except ImportError:
    PROJECT_PACKAGE = importlib.import_module('colibris')

PROJECT_PACKAGE_DIR = os.path.dirname(PROJECT_PACKAGE.__file__)
