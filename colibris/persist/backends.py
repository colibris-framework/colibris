
from peewee import PostgresqlDatabase, MySQLDatabase, SqliteDatabase

from colibris.conf.backends import BackendMixin


class DatabaseBackend(BackendMixin):
    def connect(self):
        pass

    def on_create(self):
        from . import logger  # colibris.persist logger

        # Connect to DB as soon as the backend is instantiated
        self.connect()

        logger.debug('db connection initialized')


class PostgreSQLBackend(PostgresqlDatabase, DatabaseBackend):
    pass


class MySQLBackend(MySQLDatabase, DatabaseBackend):
    pass


class SQLiteBackend(SqliteDatabase, DatabaseBackend):
    pass
