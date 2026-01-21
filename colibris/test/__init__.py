from peewee_moves import *
from peewee_moves import DatabaseManager

import colibris

from colibris import persist, conf
from colibris.conf import settings
from colibris.utils import import_module_or_none

from .fixtures import web_app_client


pytest_plugins = [
    'aiohttp.pytest_plugin',
]


def pytest_runtest_setup():
    global pytest_plugins

    conf.setup()

    # prevention
    if 'name' in settings.DATABASE or 'name' in settings.TEST_DATABASE:
        settings.DATABASE.update(settings.TEST_DATABASE)
        if 'name' not in settings.TEST_DATABASE:
            settings.DATABASE['name'] = 'test_' + settings.DATABASE['name']

        settings.DATABASE['create'] = True  # We want dbs to be created when running tests

    # Use project's fixtures as a plugin so that project-specific fixtures are loaded
    fixtures_path = '{}.tests.fixtures'.format(settings.PROJECT_PACKAGE_NAME)
    if import_module_or_none(fixtures_path):
        pytest_plugins.append(fixtures_path)

    colibris.setup()
    if persist.is_enabled():
        manager = DatabaseManager(persist.get_database(), directory=persist.get_migrations_dir())
        manager.upgrade()


def pytest_runtest_teardown():
    if persist.is_created() and not persist.get_database().is_dropped():
        persist.get_database().drop()
