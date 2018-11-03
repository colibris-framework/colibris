
import importlib
import os

from colibri import settings


try:
    PROJECT_PACKAGE = importlib.import_module(settings.PROJECT_PACKAGE_NAME)
    PROJECT_PACKAGE_DIR = os.path.dirname(PROJECT_PACKAGE.__file__)

except ImportError:
    PROJECT_PACKAGE = __name__
    PROJECT_PACKAGE_DIR = os.path.dirname(__file__)
