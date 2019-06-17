
import colibris

from colibris import persist

from .base import TestCase
from .fixtures import web_app_client


def pytest_runtest_setup():
    colibris.setup()


def pytest_runtest_teardown():
    if persist.is_created():
        persist.get_database().drop()
