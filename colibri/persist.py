
import logging
import os
import peewee

from peewee import *
from playhouse.db_url import connect as peewee_connect

from colibri import settings


# migrations live in the project root package
MIGRATIONS_DIR = os.path.join(settings.PROJECT_PACKAGE_DIR, 'migrations')

logger = logging.getLogger(__name__)
_database = None


def get_database():
    global _database

    if _database is None:
        logger.debug('initializing db connection')
        _database = peewee_connect(settings.DATABASE)
        _database.connect()

    return _database


class Model(peewee.Model):
    # this is currently necessary for aiohttp-apispec request data validation
    def __iter__(self):
        return ((k, v) for (k, v) in self.__data__.items())

    class Meta:
        database = get_database()
