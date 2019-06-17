
import os

from peewee import PostgresqlDatabase, MySQLDatabase, SqliteDatabase, mysql

from colibris.conf.backends import BackendMixin


class DatabaseBackend(BackendMixin):
    def create(self):
        self._create(self.database)

    def drop(self):
        if not self.is_closed():
            self.close()

        self._drop(self.database)

    def _create(self, name):
        raise NotImplementedError

    def _drop(self, name):
        raise NotImplementedError


class PostgreSQLBackend(PostgresqlDatabase, DatabaseBackend):
    def _one_shot_sql(self, sql):
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        conn = psycopg2.connect(dbname='postgres',
                                host=self.connect_params['host'],
                                port=self.connect_params.get('port'),
                                user=self.connect_params['user'],
                                password=self.connect_params['password'])

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()
        cur.execute(sql)

        conn.close()

    def _create(self, name):
        self._one_shot_sql('CREATE DATABASE {name}'.format(name=name))

    def _drop(self, name):
        self._one_shot_sql('DROP DATABASE {name}'.format(name=name))


class MySQLBackend(MySQLDatabase, DatabaseBackend):
    def _one_shot_sql(self, sql):
        conn = mysql.connect(host=self.connect_params['host'],
                             port=self.connect_params.get('port'),
                             user=self.connect_params['user'],
                             passwd=self.connect_params['password'])
        cur = conn.cursor()
        cur.execute(sql)

        conn.close()

    def _create(self, name):
        self._one_shot_sql('CREATE DATABASE {name}'.format(name=name))

    def _drop(self, name):
        self._one_shot_sql('DROP DATABASE {name}'.format(name=name))


class SQLiteBackend(SqliteDatabase, DatabaseBackend):
    def _create(self, name):
        pass  # SQLite automatically creates the DB file when opened

    def _drop(self, name):
        os.remove(name)
