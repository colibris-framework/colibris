from os.path import abspath, join, dirname

from colibris.conf import settings

STATIC_PATH = abspath(join(dirname(__file__), 'swagger'))

UI_URL = settings.API_DOCS_URL
STATIC_URL = '{}/static'.format(UI_URL)
APISPEC_URL = '{}/apispec'.format(UI_URL)
