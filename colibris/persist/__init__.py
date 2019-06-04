
import logging
import os

from peewee import *
try:
    from playhouse.postgres_ext import *
except ImportError:
    pass

from colibris import settings

from .backends import DatabaseBackend, PostgreSQLBackend, MySQLBackend, SQLiteBackend


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


def _prepare_db_settings():
    db_settings = dict(settings.DATABASE)
    db_settings.setdefault('autorollback', True)

    # Translate settings into whatever peewee prefers
    for param, pparam in _PEEWEE_DB_PARAMS_MAPPING.items():
        if param in db_settings:
            db_settings[pparam] = db_settings.pop(param)

    return db_settings


DatabaseBackend.configure(_prepare_db_settings())

# This needs to be imported here, after defining get_database()
from .models import Model
