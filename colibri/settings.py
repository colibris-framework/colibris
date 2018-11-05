
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
    'colibri.middleware.handle_errors_json',
    'colibri.middleware.handle_authentication',
]

AUTHENTICATION = None

API_DOCS_PATH = '/api/docs'

PUBLIC_ROUTES = (
    '/',
    API_DOCS_PATH,
    API_DOCS_PATH + '/swagger.json',
    API_DOCS_PATH + '/swagger_static'
)

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


# overwrite default settings with ones provided in SETTINGS_MODULE

_this_settings_module = sys.modules[__name__]

try:
    _project_settings_module = importlib.import_module('settings')

except ImportError:
    _project_settings_module = None

if _project_settings_module:
    for _name, _value in inspect.getmembers(_project_settings_module):
        # only consider public members that are all in capitals
        if _name.startswith('_') or not re.sub('[^a-z]', '', _name, re.IGNORECASE).isupper():
            continue

        setattr(_this_settings_module, _name, _value)


# overwrite settings from local file

try:
    from settingslocal import *

except ImportError:
    pass


# load and validate environment variables

class EnvVarsValidator(Schema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    DATABASE = fields.String()

    class Meta:
        unknown = EXCLUDE


load_dotenv(Path('.env.default'))
load_dotenv(Path('.env'), override=True)

_env_vars = EnvVarsValidator().load(os.environ)

for _name, _value in _env_vars.items():
    if _value is not None:
        setattr(_this_settings_module, _name, _value)


# adjust log level unless logging configured explicitly

if LOGGING is _DEFAULT_LOGGING and not DEBUG:
    LOGGING['root']['level'] = 'INFO'


try:
    PROJECT_PACKAGE = importlib.import_module(PROJECT_PACKAGE_NAME)

except ImportError:
    PROJECT_PACKAGE = importlib.import_module('colibri')

PROJECT_PACKAGE_DIR = os.path.dirname(PROJECT_PACKAGE.__file__)
