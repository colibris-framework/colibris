
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

    # Translate settings into whatever peewee prefers
    for param, pparam in _PEEWEE_DB_PARAMS_MAPPING.items():
        if param in db_settings:
            db_settings[pparam] = db_settings.pop(param)

    DatabaseBackend.configure(db_settings)

    if DatabaseBackend.is_enabled():
        models.set_database(get_database())
