# Settings

## The `settings` Module

Each project should have a `${PACKAGE}/settings.py` file, specifying settings that are particular for the project.

## Settings Schemas

Settings that need to be specified at runtime and depend on the running environment can be supplied via environment
variables.

Settings schemas are used to validate and adapt environment variables before being used as settings. You have to define
your settings schemas that will handle the settings your project wants to collect from the environment.

The following example will use the `DEBUG`, `LISTEN` and `PORT` environment variables to configure the corresponding
settings, when added at the end of your `${PACKAGE}/settings.py`:

    from colibris.conf.schemas import SettingsSchema, fields

    class GeneralSettingsSchema(SettingsSchema):
        DEBUG = fields.Boolean()
        LISTEN = fields.String()
        PORT = fields.Integer()

    GeneralSettingsSchema().load_from_env(globals())

The `globals()` argument ensures overriding values defined in your `${PACKAGE}/settings.py` module. 

Providing values for complex settings, such as `DATABASE` which is defined as a dictionary with parameters, can be done
by specifying the name of the setting as variable prefix:

    class DatabaseSettingsSchema(SettingsSchema):
        NAME = fields.String()
        HOST = fields.String()
        PORT = fields.Integer()
        USERNAME = fields.String()
        PASSWORD = fields.String()
    
        class Meta:
            prefix = 'DATABASE_'

If your project tends to have many such settings schemas, it is recommended that you move them to an e.g.
`${PACKAGE}/settingsshemas.py` module:

    from colibris.conf.schemas import SettingsSchema, fields

    class GeneralSettingsSchema(SettingsSchema):
        DEBUG = fields.Boolean()
        LISTEN = fields.String()
        PORT = fields.Integer()

    class DatabaseSettingsSchema(SettingsSchema):
        NAME = fields.String()
        HOST = fields.String()
        PORT = fields.Integer()
        USERNAME = fields.String()
        PASSWORD = fields.String()
    
        class Meta:
            prefix = 'DATABASE_'

    ...

    def load_from_env(target_settings):
        GeneralSettingsSchema().load_from_env(target_settings)
        DatabaseSettingsSchema().load_from_env(target_settings)

Then import it in `${PACKAGE}/settings.py` and simply call `load_from_env` at the end:

    settingsschemas.load_from_env(globals())

Environment variables can be put together in a `.env` file that is located in the directory where you run your project
from (usually the root folder of your project). This file should never be added to git.

If you want your variables to be part of your project's repository, you can add them to `${PACKAGE}/.env.default`, which
should be added to git.

## Available Settings

### `API_DOCS_URL`

Controls the path where the API documentation is served. Defaults to `/api/docs`.

### `AUTHENTICATION`

Configures the authentication backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

### `AUTHORIZATION`

Configures the authorization backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

### `CACHE`

Configures the cache backend. Should be defined as a dictionary with at least one entry, `backend`, representing the
python path to the backend class. The rest of the entries are passed as arguments to the constructor.

### `DATABASE`

Sets the project database.
See [this](http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url) for examples of
database URLs.

### `DEBUG`

Enables or disables debugging. Defaults to `True`.

### `EMAIL`

Configures the email backend. Should be defined as a dictionary with at least one entry, `backend`, representing the
python path to the backend class. The rest of the entries are passed as arguments to the constructor.

### `LISTEN`

Controls the interface(s) on which the server listens. Defaults to `'0.0.0.0'`.

### `LOGGING`

Configures the logging mechanism.
See [logging.config](https://docs.python.org/3.7/library/logging.config.html) for details.

### `LOGGING_OVERRIDES`

Allows overriding parts of the logging configuration (for example silencing a library).

### `MAX_REQUEST_BODY_SIZE`

Controls the maximum allowed size of a request body, in bytes. Defaults to `10MB`.  

### `MIDDLEWARE`

A list of all the middleware functions to be applied, in order, to each request/response. Defaults to:

    [
        'colibris.middleware.handle_errors_json',
        'colibris.middleware.handle_auth',
        'colibris.middleware.handle_schema_validation'
    ]

### `PORT`

Controls the server TCP listening port. Defaults to `8888`.

### `PROJECT_PACKAGE_DIR`

Sets the path to the project directory. This setting is determined automatically and should not be changed.

### `PROJECT_PACKAGE_NAME`

Sets the main project package name. This setting is determined automatically and should not be changed.

### `SECRET_KEY`

Sets the project secret key that is used to create various tokens. Defaults to `None` and must be set explicitly.

### `TASKQUEUE`

Configures the background tasks backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

### `TEMPLATES`

Configures the templates backend. Should be defined as a dictionary with at least one entry, `backend`, representing the
python path to the backend class. The rest of the entries are passed as arguments to the constructor.

### `TEST_DATABASE`

Similar to `DATABASE` but used when running tests. Missing fields are used from `DATABASE`. If `name` is not specified,
`DATABASE['name']` with a `test_` prefix will be used. 
