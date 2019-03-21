
PROJECT_PACKAGE_NAME = 'colibris'

DEBUG = True

LISTEN = '0.0.0.0'
PORT = 8888

MAX_REQUEST_BODY_SIZE = 10 * 1024 * 1024

MIDDLEWARE = [
    'colibris.middleware.handle_errors_json',
    'colibris.middleware.handle_auth',
    'colibris.middleware.handle_schema_validation',
]

AUTHENTICATION = {}
AUTHORIZATION = {}

CACHE = {}
DATABASE = {}
TEMPLATE = {}
TASK_QUEUE = {}

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
            'level': 'DEBUG'  # always show details when doing migrations
        }
    }
}

LOGGING_OVERRIDES = {}
