from os.path import abspath, join, dirname

from colibris.conf import settings

STATIC_PATH = abspath(join(dirname(__file__), "ui"))

SWAGGER_URL = settings.API_DOCS_PATH
STATIC_URL = '{}/static'.format(SWAGGER_URL)
APISPEC_URL = '{}/apispec'.format(SWAGGER_URL)
