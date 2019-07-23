# Migrations

## Create Migrations

To create migrations for your model changes, use:

    ./${PACKAGE}/manage.py makemigrations

You can optionally specify a name for your migrations:

    ./${PACKAGE}/manage.py makemigrations somename

## Apply Migrations

To apply migrations on the currently configured database, use:

    ./${PACKAGE}/manage.py migrate
