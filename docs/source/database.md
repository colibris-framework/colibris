# Database

Choose a backend for the database, by setting the `DATABASE` variable in `${PACKAGE}/settings.py`. By default, no
database is enabled and the persistence layer is disabled.

## SQLite Backend

In `${PACKAGE}/settings.py`, set:

    DATABASE = {
        'backend': 'colibris.persist.SQLiteBackend',
        'name': '/path/to/yourproject.db'
    }

## MySQL Backend

Make sure to have the `mysqldb` or `pymysql` python package installed.

In `${PACKAGE}/settings.py`, set:

    DATABASE = {
        'backend': 'colibris.persist.MySQLBackend',
        'name': 'yourproject',
        'host': '127.0.0.1',
        'port': 3316,
        'username': 'username',
        'password': 'password'
    }

## PostgreSQL Backend

Make sure to have the `psycopg2-binary` python package installed.

In `${PACKAGE}/settings.py`, set:

    DATABASE = {
        'backend': 'colibris.persist.PostgreSQLBackend',
        'name': 'yourproject',
        'host': '127.0.0.1',
        'port': 5432,
        'username': 'username',
        'password': 'password'
    }
