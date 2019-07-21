# Deployment

## Dependencies and Pipfile

Add your dependencies to `Pipfile`:

    nano Pipfile
    
For example, if you're using PostgreSQL, you may want to add:

    [packages]
    ....
    psycopg2-binary = "*"
    ...

### Lock Down Versions

Lock your dependencies with their versions in `Pipfile.lock`:

    pipenv lock

### Install Dependencies

Install all of your project's dependencies:

    pipenv sync
    
## Using `setuptools`

The project's skeleton comes with a `${PACKAGE}/setup.py` file, effectively allowing your project to be packaged with
`setuptools`.

To create a package of your project, run:

    python setup.py sdist
    
You'll then find your packaged project at `dist/${PROJECT_NAME}-${VERSION}.tar.gz`. The version is automatically read
from `${PACKAGE}/__init__.py`.

The provided setup file will create a console script having your project's main package name, that will basically do
exactly what `manage.py` does.

One thing that is worth noting when using `setuptools` to deploy a project is that the `manage.py` file that used to be
in your project's root folder will now live in the main package of your project.

## Using Docker

If you want to deploy your service using Docker, you'll first need to edit `Dockerfile` and change it according to your
needs:

    nano Dockerfile

If you plan on using Docker Compose, you'll probably want to edit the `docker-compose.yml` file as well:

    nano docker-compose.yml

### Building Docker Image

You can manually build the image for your server like this:

    docker build -t ${PROJECT_NAME}:${VERSION} .

If your project has multiple services (e.g. "server" and "worker"), you'll want to build and tag them separately:

    docker build -t ${PROJECT_NAME}:server-${VERSION} --target server .
    docker build -t ${PROJECT_NAME}:worker-${VERSION} --target worker .

### Manually Run Container

You can run your container locally:

    docker run -it ${PPROJECT_NAME}:${VERSION} -p 8888:8888
    
or, if you have multiple services:

    docker run -it ${PPROJECT_NAME}:server-${VERSION} -p 8888:8888
    docker run -it ${PPROJECT_NAME}:worker-${VERSION}

### Using `docker-compose`

You can use `docker-compose` to build your images, instead of building them manually:

    docker-compose build 

To start your services, use:

    docker-compose up

When you're done, shut it down by hitting `Ctrl-C`; then you can remove the containers:

    docker-compose down
