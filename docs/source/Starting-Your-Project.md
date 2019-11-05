# Starting Your Project

The following variables are assumed:

 * `VENVS` - the folder where you keep your python virtual environments (e.g. `~/.local/share/virtualenvs`)
 * `PROJECT_NAME` - the name of your project (e.g. `my-project`) 
 * `PROJECTS_DIR` - the folder where you keep your projects (e.g. `~/Projects`)
 * `PACKAGE` - the name of your main project's package 
 * `VERSION` - the version of your project

Create a virtual environment for your new project:

    virtualenv ${VENVS}/${PROJECT_NAME} && source ${VENVS}/${PROJECT_NAME}/bin/activate

Install `colibris`:

    pip install colibris
    

Go to your projects folder:

    cd ${PROJECTS_DIR}

Prepare the project:

    colibris-start-project ${PROJECT_NAME}

You can use a different skeleton template repository for your project:

    colibris-start-project ${PROJECT_NAME} --skeleton git@github.com:myorganization/microservice-skeleton.git 

Your project folder will contain a package derived from your project name as well as various other stuff. You'll find
a `manage.py` module in the project package, which is in fact the main script of your project.

You'll also find a `settings.py` module that you'll want to edit to adapt it to your project's needs.

The commands in this document assume you're in your project folder and you have your virtual environment correctly
sourced, unless otherwise specified.
