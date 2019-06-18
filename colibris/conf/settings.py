
PROJECT_PACKAGE_NAME = ''
PROJECT_PACKAGE_DIR = ''

DEBUG = True

LISTEN = '0.0.0.0'
PORT = 8888

MAX_REQUEST_BODY_SIZE = 10 * 1024 * 1024

SECRET_KEY = None

MIDDLEWARE = [
    'colibris.middleware.errors.handle_errors_json',
    'colibris.middleware.auth.handle_auth',
    'colibris.middleware.schema.handle_schema_validation',
]

AUTHENTICATION = {
    'backend': 'colibris.authentication.null.NullBackend'
}

AUTHORIZATION = {
    'backend': 'colibris.authorization.null.NullBackend'
}

CACHE = {}
DATABASE = {}
TEST_DATABASE = {}
TEMPLATE = {}
TASK_QUEUE = {}
EMAIL = {}

API_DOCS_PATH = '/api/docs'

LOGGING = {
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
            'level': 'DEBUG'  # Always show details when doing migrations
        }
    }
}

LOGGING_OVERRIDES = {}
