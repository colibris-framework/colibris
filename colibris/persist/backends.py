
from peewee import PostgresqlDatabase, MySQLDatabase, SqliteDatabase

from colibris.conf.backends import BackendMixin


class DatabaseBackend(BackendMixin):
    @classmethod
    def get_instance(cls):
        from . import logger  # colibris.persist logger

        instance = super(DatabaseBackend, cls).get_instance()

        # Connect to DB as soon as the backend is instantiated
        instance.connect()

        logger.debug('db connection initialized')

        return instance


class PostgreSQLBackend(PostgresqlDatabase, DatabaseBackend):
    pass


class MySQLBackend(MySQLDatabase, DatabaseBackend):
    pass


class SQLiteBackend(SqliteDatabase, DatabaseBackend):
    pass
