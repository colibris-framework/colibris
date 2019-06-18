
import logging
import os

from peewee import *
try:
    from playhouse.postgres_ext import *

except ImportError:
    pass

from colibris.conf import settings

from .backends import DatabaseBackend, PostgreSQLBackend, MySQLBackend, SQLiteBackend
from .models import Model


_PEEWEE_DB_PARAMS_MAPPING = {
    'name': 'database',
    'username': 'user'
}

logger = logging.getLogger(__name__)


def get_migrations_dir():
    # Migrations live in the project's root package
    return os.path.join(settings.PROJECT_PACKAGE_DIR, 'migrations')


def get_database():
    return DatabaseBackend.get_instance()


def connectivity_check():
    # run a dummy SQL statement to check connectivity with DB server

    try:
        list(get_database().execute_sql("select 'dummy'"))
        return True

    except Exception:
        return False


def setup():
    db_settings = dict(settings.DATABASE)
    db_settings.setdefault('autorollback', True)

    create = db_settings.pop('create', False)

    # Translate settings into whatever peewee prefers
    for param, pparam in _PEEWEE_DB_PARAMS_MAPPING.items():
        if param in db_settings:
            db_settings[pparam] = db_settings.pop(param)

    DatabaseBackend.configure(db_settings)

    if DatabaseBackend.is_enabled():
        database = get_database()
        if create:
            logger.debug('creating db')
            try:
                database.create()

            except Exception as e:
                logger.error('db creation failed: %s', e, exc_info=True)

        database.connect()
        logger.debug('db connection initialized')

        models.set_database(get_database())


def is_enabled():
    return DatabaseBackend.is_enabled()


def is_created():
    return DatabaseBackend.is_created()
