
import importlib
import inspect
import os
import sys

from pathlib import Path

from dotenv import load_dotenv
from marshmallow import Schema, fields, INCLUDE


# load and validate environment variables
class EnvVarsValidator(Schema):
    SETTINGS_MODULE = fields.String(missing='settings')
    DEBUG = fields.Boolean(missing=True)
    LISTEN = fields.String(missing='0.0.0.0')
    PORT = fields.Integer(missing=8888)
    DATABASE = fields.String(missing='sqlite:///default.db')

    class Meta:
        unknown = INCLUDE


load_dotenv(Path('.env.default'))
load_dotenv(Path('.env'), override=True)

_env_vars = EnvVarsValidator().load(os.environ)


# configurable stuff

PROJECT_PACKAGE_NAME = 'projectname'

DEBUG = _env_vars['DEBUG']

LISTEN = _env_vars['LISTEN']
PORT = _env_vars['PORT']

API_DOCS_PATH = '/api/docs'

PUBLIC_ROUTES = (
    '/',
    API_DOCS_PATH,
    API_DOCS_PATH + '/swagger.json',
    API_DOCS_PATH + '/swagger_static'
)

# DATABASE = 'sqlite:////path/to/file.db
# DATABASE = 'postgresql://username:password@host:5432/dbname'
DATABASE = _env_vars['DATABASE']


# overwrite default settings with ones provided in SETTINGS_MODULE
try:
    _settings_module = importlib.import_module(_env_vars['SETTINGS_MODULE'])
    _this_settings_module = sys.modules[__name__]

    for _name, _value in inspect.getmembers(_settings_module):
        if _name.startswith('_'):
            continue

        if not _name[0].isupper():
            continue

        setattr(_this_settings_module, _name, _value)

except ImportError:
    pass

