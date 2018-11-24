
## Starting Your Project

Go to your projects folder:

    cd ${PROJECTS_DIR}

Create a virtual environment for your new project:

    virtualenv .venv && source .venv/bin/activate

Install colibris:

    pip install git+https://gitlab.com/safefleet/colibris.git

(For mac users) Install gnu sed:

    brew install gnu-sed --with-default-names

Prepare the project:

    colibris-start-project ${PROJECT_NAME} --template git@gitlab.com:safefleet/microservice-template.git 

Your project folder will contain a package derived from your project name as well as various other stuff.

The rest of the steps assume you're in your project folder and you have your virtual environment correctly sourced.


## Database

Set your database URL by editing the `settings.py` file:

    nano settings.py 


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


## Authentication

Choose a backend for the authentication by setting the `AUTHENTICATION` variable in `settings.py`. By default, it is set
to `None`, associating each request with a dummy identity.

#### JWT Backend

In `settings.py`, set:

    AUTHENTICATION = {
        'backend': 'colibris.authentication.jwt.JWTBackend',
        'model': 'yourproject.models.User',
        'identity_claim': 'sub',
        'identity_field': 'username',
        'secret_field': 'password'
    }


## Authorization

Choose a backend for the authorization by setting the `AUTHORIZATION` variable in `settings.py`. By default, it is set
to `None`, allowing everybody to perform any request.

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


## Web Server

Start the web server by running:

    ./manage.py runserver

Then you can test it by pointing your browser to:

    http://localhost:8888


## Migrations

#### Create Migrations

To create migrations for your model changes, use:

    ./manage.py makemigrations

You can optionally specify a name for your migrations:

    ./manage.py makemigrations somename

#### Apply Migrations

To apply migrations on the currently configured database, use:

    ./manage.py migrate


## App Initialization

You can add project-specific initialization code in the `init` function exposed by `app.py`:

    nano ${PACKAGE}/app.py


## Cache

The caching mechanism is configured via the `CACHE` variable in `settings.py`. It defaults to `None`, in which case the
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

In `settings.py`, set:

    CACHE = {
        'backend': 'colibris.cache.redis.RedisBackend',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': 'yourpassword'
    }


## Health Status

You can (and should) implement your project-specific health check function by exposing the `get_health` function in
`app.py`:

    nano ${PACKAGE}/app.py


## Deployment

#### Dependencies and Pipfile

Add your dependencies to `Pipfile`:

    nano Pipfile
    
If you're using PostgreSQL, you may want to add:

    [packages]
    ....
    psycopg2-binary = "*"
    ...

If you're using JWT for authentication, you may want to add:

    [packages]
    ....
    pyjwt = "*"
    ...

#### Lock Down Versions

Lock your dependencies with their versions in `Pipfile.lock`:

    pipenv lock

#### Install Dependencies

Install all of your project's dependencies:

    pipenv sync

#### Build Docker Image

Build your local docker image, optionally tagging it with your version:

    docker build -t ${PROJECT_NAME}:${VERSION}

#### Manually Run Container

You can run your container locally as follows:

    docker run -it ${PPROJECT_NAME}:${VERSION} -p 8888:8888
    
#### Use docker-compose

Uncomment/add needed services to `docker-compose.yml`:

    nano docker-compose.yml

Start your suite of services using docker-compose:

    docker-compose up
    
When you're done, shut it down by hitting `Ctrl-C`; then you can remove the containers:

    docker-compose down

## Settings

#### `AUTHENTICATION`

Configures the authentication backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

Defaults to `None`, which effectively disables authentication.

#### `AUTHORIZATION`

Configures the authorization backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

Defaults to `None`, which effectively disables authorization, allowing access to all resources for any authenticated
request.

Here's a list of available settings and their default values:

#### `CACHE`

Configures the cache backend. Should be defined as a dictionary with at least one entry, `backend`,
representing the python path to the backend class. The rest of the entries are passed as arguments to the constructor.

Defaults to `None`, which configures the in-memory cache backend.

#### `DATABASE`

Sets the project database.
See [this](http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url) for examples of
database URLs.

Defaults to `'sqlite:///${PROJECT_NAME}.db'`

#### `DEBUG`

Enables or disables debugging. Defaults to `True`.

#### `LISTEN`

Controls the interface(s) on which the server listens. Defaults to `'0.0.0.0'`.

#### `LOGGING`

Configures the logging mechanism.
See [logging.config](https://docs.python.org/3.7/library/logging.config.html) for details.

#### `MIDDLEWARE`

A list of all the middleware functions to be applied, in order, to each request/response. Defaults to:

    [
        'colibris.middleware.handle_errors_json',
        'colibris.middleware.handle_auth',
        'colibris.middleware.handle_schema_validation'
    ]

#### `PORT`

Controls the server TCP listening port. Defaults to `8888`.

#### `PROJECT_PACKAGE_NAME`

Sets the main project package name. Defaults to `'${PROJECT_NAME}'`.
