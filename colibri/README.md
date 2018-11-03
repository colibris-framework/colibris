
## Start A New Project

Go to your projects folder:

    cd ${PROJECTS_DIR}

Create a new folder for your project:

    mkdir ${PROJECT} && cd ${PROJECT}

Create a virtual environment for your new project:

    virtualenv .venv && source .venv/bin/activate

Install colibri:

    pip install git+git@gitlab.com/ccrisan/colibri.git

Prepare the project:

    colibri-start-project


## Run The Web Server

Make sure you're using your project's virtual environment:

    cd ${PROJECTS_DIR}/${PROJECT} && source .venv/bin/activate

Start your web server by running:

    ./manage.py runserver


## Migrations

Make sure you're using your project's virtual environment:

    cd ${PROJECTS_DIR}/${PROJECT} && source .venv/bin/activate

### Create Migrations

To create migrations for your model changes, use:

    ./manage.py makemigrations

You can optionally specify a name for your migrations:

    ./manage.py makemigrations somename

### Apply Migrations

To apply migrations on the currently configured database, use:

    ./manage.py migrate
