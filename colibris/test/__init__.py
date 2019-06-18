
from peewee_migrate import Router

import colibris

from colibris import persist

from .fixtures import web_app_client


def pytest_runtest_setup():
    colibris.setup()
    if persist.is_enabled():
        router = Router(persist.get_database(), migrate_dir=persist.get_migrations_dir())
        router.run()


def pytest_runtest_teardown():
    if persist.is_created() and not persist.get_database().is_dropped():
        persist.get_database().drop()
