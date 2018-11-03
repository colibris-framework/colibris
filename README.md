
## Starting Your Project

Go to your projects folder:

    cd ${PROJECTS_DIR}

Create a new folder for your project:

    mkdir ${PROJECT} && cd ${PROJECT}

Create a virtual environment for your new project:

    virtualenv .venv && source .venv/bin/activate

Install colibri:

    pip install git+https://gitlab.com/ccrisan/colibri.git

Prepare the project:

    colibri-start-project

Your project folder will contain a package derived from your project name as well as various other stuff.

The rest of the steps assume you're in your project folder and you have your virtual environment correctly sourced.


## Database

Set your database URL by editing the `settings.py` file:

    nano settings.py 


## Models

Add your models by editing the `models.py` file:

    nano ${PACKAGE}/settings.py 


## Views

Add your views by editing the `views.py` file:

    nano ${PACKAGE}/views.py 


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
