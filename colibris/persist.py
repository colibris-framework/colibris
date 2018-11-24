
import logging
import os
import peewee

from peewee import *
from playhouse.postgres_ext import *

from colibris import settings
from colibris import utils


# migrations live in the project root package
MIGRATIONS_DIR = os.path.join(settings.PROJECT_PACKAGE_DIR, 'migrations')
_PEEWEE_DB_PARAMS_MAPPING = {
    'name': 'database',
    'user': 'username'
}

logger = logging.getLogger(__name__)
_database = None


def get_database():
    global _database

    if _database is None:
        backend_settings = dict(settings.DATABASE)
        backend_path = backend_settings.pop('backend', 'colibris.persist.SqliteDatabase')
        backend_class = utils.import_member(backend_path)

        # translate settings into whatever peewee prefers
        for param, pparam in _PEEWEE_DB_PARAMS_MAPPING.items():
            if param in backend_settings:
                backend_settings[pparam] = backend_settings.pop(param)

        backend_settings.setdefault('autorollback', True)

        _database = backend_class(**backend_settings)
        _database.connect()

        logger.debug('db connection initialized')

    return _database


class Model(peewee.Model):
    # this is currently necessary for aiohttp-apispec request data validation
    def __iter__(self):
        return ((k, v) for (k, v) in self.__data__.items())

    def update_fields(self, fields):
        for n, v in fields.items():
            setattr(self, n, v)

    class Meta:
        database = get_database()
