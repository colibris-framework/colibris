
## Starting Your Project

The following variables are assumed:

 * `VENVS` - the folder where you keep your python virtual environments (e.g. `~/.local/share/virtualenvs`)
 * `PROJECT_NAME` - the name of your project (e.g. `my-project`) 
 * `PROJECTS_DIR` - the folder where you keep your projects (e.g. `~/Projects`) 

Create a virtual environment for your new project:

    virtualenv ${VENVS}/${PROJECT_NAME} && source ${VENVS}/${PROJECT_NAME}/bin/activate

Install `colibris`:

    pip install colibris
    
(For mac users) Install gnu sed:

    brew install gnu-sed --with-default-names

Go to your projects folder:

    cd ${PROJECTS_DIR}

Prepare the project:

    colibris-start-project ${PROJECT_NAME}

You can use a different template repository for your project's skeleton:

    colibris-start-project ${PROJECT_NAME} --template git@gitlab.com:safefleet/microservice-template.git 

Your project folder will contain a package derived from your project name as well as various other stuff.

The commands in this document assume you're in your project folder and you have your virtual environment correctly
sourced, unless otherwise specified.


## Database

Choose a backend for the database, by setting the `DATABASE` variable in `settings.py`. By default, no database is
enabled and the persistence layer is disabled.

#### SQLite Backend

In `settings.py`, set:

    DATABASE = {
        'backend': 'colibris.persist.SqliteDatabase',
        'name': '/path/to/yourproject.db'
    }

#### MySQL Backend

Make sure to have the `mysqldb` or `pymysql` python package installed.

In `settings.py`, set:

    DATABASE = {
        'backend': 'colibris.persist.MysqlDatabase',
        'name': 'yourproject',
        'host': '127.0.0.1',
        'port': 3316,
        'username': 'username',
        'password': 'password'
    }

#### PostgreSQL Backend

Make sure to have the `psycopg2-binary` python package installed.

In `settings.py`, set:

    DATABASE = {
        'backend': 'colibris.persist.PostgresqlDatabase',
        'name': 'yourproject',
        'host': '127.0.0.1',
        'port': 5432,
        'username': 'username',
        'password': 'password'
    }


## Models

Add your models by editing the `models.py` file:

    nano ${PACKAGE}/models.py 


## Schemas

Add your schemas by editing the `schemas.py` file:

    nano ${PACKAGE}/schemas.py 


## Views

Add your views by editing the `views.py` file:

    nano ${PACKAGE}/views.py


## Routes

Associate URL paths to views by editing the `routes.py` file: 

    nano ${PACKAGE}/routes.py
    
If you need routes for static files (recommended only for development), add your static prefix/path associations to
`STATIC_ROUTES`.


## Authentication

Choose a backend for the authentication by setting the `AUTHENTICATION` variable in `settings.py`. By default, it is set
to `{}`, associating each request with a dummy identity.

#### JWT Backend

Make sure to have the `pyjwt` python package installed. 

In `settings.py`, set:

    AUTHENTICATION = {
        'backend': 'colibris.authentication.jwt.JWTBackend',
        'model': 'yourproject.models.User',
        'identity_claim': 'sub',
        'identity_field': 'username',
        'secret_field': 'password',
        'cookie_name': 'auth_token',
        'cookie_domain': 'example.com',
        'validity_seconds': 3600 * 24 * 30
    }
    
The `cookie_name` property is optional and tells the backend to look for the token in cookies as well, in addition to
the `Authorization` header.

The `cookie_domain` property is optional and configures the cookie domain.

The `validity_seconds` property is optional and configures the given validity for the token.


## Authorization

Choose a backend for the authorization by setting the `AUTHORIZATION` variable in `settings.py`. By default, it is set
to `{}`, allowing everybody to perform any request.

#### Role Backend

In `settings.py`, set:

    AUTHORIZATION = {
        'backend': 'colibris.authorization.role.RoleBackend',
        'role_field': 'role'
    }

#### Rights Backend

In `settings.py`, set:

    AUTHORIZATION = {
        'backend': 'colibris.authorization.rights.RightsBackend',
        'model': 'yourproject.models.Right',
        'account_field': 'user',
        'resource_field': 'resource',
        'operations_field': 'operations'
    }


## Migrations

#### Create Migrations

To create migrations for your model changes, use:

    ./manage.py makemigrations

You can optionally specify a name for your migrations:

    ./manage.py makemigrations somename

#### Apply Migrations

To apply migrations on the currently configured database, use:

    ./manage.py migrate


## Web Server

Start the web server by running:

    ./manage.py runserver

Then you can test it by pointing your browser to:

    http://localhost:8888


## App Initialization

You can add project-specific initialization code in the `init` function exposed by `app.py`:

    nano ${PACKAGE}/app.py


## Cache

The caching mechanism is configured via the `CACHE` variable in `settings.py`. It defaults to `{}`, in which case the
local in-memory backend is used.

#### Usage

To use the caching mechanism, just import it wherever you need it:

    from colibris import cache
    
To set a value, use `set`:

    cache.set('my_key', my_value, lifetime=300)

Later, you can get your value back:

    my_value = cache.get('my_key', default='some_default')

You can invalidate a key using `delete`:

    cache.delete('my_key')

#### Redis Backend

Make sure to have the `redis` python package installed.

In `settings.py`, set:

    CACHE = {
        'backend': 'colibris.cache.redis.RedisBackend',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': 'yourpassword'
    }


## Templates

The templates mechanism is configured via the `TEMPLATE` variable in `settings.py`. It defaults to `{}`, in which case
the templates are disabled.

#### Search Paths

The template files should live in a folder called `templates`, in your project's package directory. If you want them
to be searched for in other folders, just add those paths to the `paths` template setting.

#### Basic Usage

To use the templating mechanism, just import it wherever you need it:

    from colibris import template
    
To render a template file, simply call the `render` function and specify context as keyword arguments:

    result = template.render('my_template.txt', var1='value1', var2=16)

To render a template from a string, call the `render_string` function:

    result = template.render_string('Variable var1 is {{ var1 }} and var2 is {{ var2 }}.', var1='value1', var2=16)

#### Rendering HTML

The following example will render an HTML template file from a view:

    from colibris.shortcuts import html_response_template    

    def index(request):
        return html_response_template('index.html', var1='value1')

#### Jinja2 Backend

Make sure to have the `jinja2` python package installed.

In `settings.py`, set:

    TEMPLATE = {
        'backend': 'colibris.template.jinja2.Jinja2Backend',
        'extensions': [...],
        'translations': 'gettext'
    }

Field `extensions` is optional and represents a list of extensions to be used by the Jinja2 environment.

Field `translations` is optional and, if present, will enable `gettext`-based Jinja2 translations. Its value is the path
to a python object that implements the `gettext` functions (such as the standard library `gettext`).


## Email Sending

The email sending mechanism is controlled by the `EMAIL` variable in `settings.py`. By default, this function is
disabled and, if you try to send an email, nothing more than a logging message will happen.

#### Basic Usage

To send an email, just import the `email` package wherever you need it:

    from colibris import email

Then create an email message:

    msg = email.EmailMessage('My Subject', 'my body', to=['email@example.com'])

You can now send it:

    email.send(msg)

Sending is done using the "fire and forget" way; don't expect any result or exceptions from this call. Any errors that
might occur will be logged, though.

Make sure you configure your `default_from` value in your `EMAIL` setting, in `settings.py`:

    EMAIL = {
        'default_from': 'myservice@example.com',
        ...
    }

#### Attachments

Attaching a file is as simple as calling the `attach()` method:

    with open('/path/to/myfile.pdf', 'rb') as f:
        msg.attach('myfile.pdf', f.read())

#### HTML Content

Sending HTML content is achieved by specifying the `html` argument to `EmailMessage`:

    msg = email.EmailMessage('My Subject', 'my text body', html='<p>My HTML content</p>', to=['email@example.com'])

The HTML content acts as an alternative to the body and will be used by the mail readers that are capable to show it.

#### Console Backend

In `settings.py`, set:

    EMAIL = {
        'backend': 'colibris.email.console.ConsoleBackend'
    }

You'll see the email content printed at standard output.

#### SMTP Backend

Make sure you have the `aiosmtplib` python package installed.

In `settings.py`, set:

    EMAIL = {
        'backend': 'colibris.email.smtp.SMTPBackend',
        'host': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'username': 'user@gmail.com',
        'password': 'yourpassword'
    }


## Background Tasks

Running time-consuming tasks can be done by using the `taskqueue` functionality. The `TASK_QUEUE` variable in
`settings.py` configures the background running task mechanism. It defaults to `{}`, in which case the background tasks
are disabled.

#### Usage

To run a background task, import the `taskqueue` wherever you need it:

    from colibris import taskqueue
    
Then run your time consuming task:

    def time_consuming_task(arg1, arg2):
        time.sleep(10)
    
    ...
    
    try:
        result = await taskqueue.execute(time_consuming_task, 'value1', arg2='value2', timeout=20)
    
    except Exception as e:
        handle_exception(e)

#### RQ Backend

Make sure to have the `rq` and `redis` python packages installed.

In `settings.py`, set:

    TASK_QUEUE = {
        'backend': 'colibris.taskqueue.rq.RQBackend',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': 'yourpassword',
        'poll_results_interval': 1
    }

#### Background Worker

To actually execute the queued background tasks, you'll need to spawn at least one worker:

    ./manage.py runworker


## Health Status

You can (and should) implement your project-specific health check function by exposing the `get_health` function in
`app.py`:

    nano ${PACKAGE}/app.py


## Deployment

#### Dependencies and Pipfile

Add your dependencies to `Pipfile`:

    nano Pipfile
    
For example, if you're using PostgreSQL, you may want to add:

    [packages]
    ....
    psycopg2-binary = "*"
    ...

#### Lock Down Versions

Lock your dependencies with their versions in `Pipfile.lock`:

    pipenv lock

#### Install Dependencies

Install all of your project's dependencies:

    pipenv sync
    
#### Using `setuptools`

The project's skeleton comes with a `setup.py` file, effectively allowing your project to be packaged with `setuptools`.

To create a package of your project, run:

    python setup.py sdist
    
You'll then find your packaged project at `dist/${PROJECT_NAME}-${VERSION}.tar.gz`. The version is automatically read
from your main package's `__init__.py`.

The provided setup file will create a console script having your project's main package name, that will basically do
exactly what `manage.py` does.

One thing that is worth noting when using `setuptools` to deploy a project is that the `manage.py` and `settings.py`
files that used to be in your project's root folder will now live in the main package of your project. 

#### Building Docker Image

Build your local docker image, optionally tagging it with your version:

    docker build -t ${PROJECT_NAME}:${VERSION} .

#### Manually Run Container

You can run your container locally as follows:

    docker run -it ${PPROJECT_NAME}:${VERSION} -p 8888:8888

#### Using `docker-compose`

Uncomment/add needed services to `docker-compose.yml`:

    nano docker-compose.yml

Start your suite of services using docker-compose:

    docker-compose up
    
When you're done, shut it down by hitting `Ctrl-C`; then you can remove the containers:

    docker-compose down

## Settings

#### The `settings` Module

Each project should have a `settings.py` file, specifying settings that are particular for the project.

#### The `settingslocal` Module

For local deployments or development environments, you can specify your particular settings in a `settingslocal.py`
file. It has a higher precedence than the project's `settings` module.

#### Environment Variables

Settings can be overridden using environment variables. Environment variables have the highest precedence when it comes
to specifying settings. This is the recommended way of particularizing setting values on specific deployments.

For simple settings, such as `DEBUG`, the corresponding environment variable coincides with the setting.

For complex settings, such as `DATABASE`, each setting parameter will have a separate corresponding environment
variable. For example, `DATABASE_HOST` will set the `host` parameter of the `DATABASE` setting.

Environment variables can be put together in a `.env` file that is located in the root folder of the project. This file
should never be added to git.

If you want your variables to be part of your project's repository, you can add them to `.env.default`, which should be
added to git.

#### Settings Schemas

Environment variables are validated and transformed before assigned to settings. These validations are handled by 
settings schemas. Settings schemas are predefined for all Colibris settings. For project-specific settings, you must
define your own settings schemas in your `settings.py` and decorate them accordingly:

    from colibris.conf.schemas import SettingsSchema, fields, register_settings_schema

    @register_settings_schema
    class MySettingsSchema(SettingsSchema):
        MY_INT_SETTING = fields.Integer()
        MY_STR_SETTING = fields.String()

#### Available Settings

###### `API_DOCS_PATH`

Controls the path where the API documentation is served. Defaults to `/api/docs`.

###### `AUTHENTICATION`

Configures the authentication backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

Defaults to `{}`, which effectively disables authentication.

###### `AUTHORIZATION`

Configures the authorization backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

Defaults to `{}`, which effectively disables authorization, allowing access to all resources for any authenticated
request.

###### `CACHE`

Configures the cache backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

Defaults to `{}`, which configures the in-memory cache backend.

###### `DATABASE`

Sets the project database.
See [this](http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url) for examples of
database URLs.

Defaults to `{}`, which disables the persistence mechanism.

###### `DEBUG`

Enables or disables debugging. Defaults to `True`.

###### `LISTEN`

Controls the interface(s) on which the server listens. Defaults to `'0.0.0.0'`.

###### `LOGGING`

Configures the logging mechanism.
See [logging.config](https://docs.python.org/3.7/library/logging.config.html) for details.

###### `LOGGING_OVERRIDES`

Allows overriding parts of the logging configuration (for example silencing a library).

###### `MAX_REQUEST_BODY_SIZE`

Controls the maximum allowed size of a request body, in bytes. Defaults to `10MB`.  

###### `MIDDLEWARE`

A list of all the middleware functions to be applied, in order, to each request/response. Defaults to:

    [
        'colibris.middleware.handle_errors_json',
        'colibris.middleware.handle_auth',
        'colibris.middleware.handle_schema_validation'
    ]

###### `PORT`

Controls the server TCP listening port. Defaults to `8888`.

###### `PROJECT_PACKAGE_DIR`

Sets the path to the project directory. By default, it is automatically deduced. 

###### `PROJECT_PACKAGE_NAME`

Sets the main project package name. Defaults to `'${PROJECT_NAME}'`.

###### `SECRET_KEY`

Sets the project secret key that is used to create various tokens. Defaults to `None` and must be set explicitly.
