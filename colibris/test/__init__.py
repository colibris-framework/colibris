from peewee_moves import *
from peewee_moves import DatabaseManager

import colibris

from colibris import persist

from .fixtures import web_app_client


def pytest_runtest_setup():
    colibris.setup()
    if persist.is_enabled():
        manager = DatabaseManager(persist.get_database(), directory=persist.get_migrations_dir())
        manager.upgrade()


def pytest_runtest_teardown():
    if persist.is_created() and not persist.get_database().is_dropped():
        persist.get_database().drop()
