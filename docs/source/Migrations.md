# Migrations


## Manage Migrations
The migrations are managed by [`peewee-moves`](https://github.com/timster/peewee-moves), a small and
flexible migration manager for Peewee ORM.

    ./${PACKAGE}/manage.py db --help
    Usage: manage.py [OPTIONS] COMMAND [ARGS]...

      Run database migration commands.

    Options:
      --table TEXT
      --help            Show this message and exit.

    Commands:
      create     Create a migration based on an existing model.
      delete     Delete the target migration from the filesystem and database.
      downgrade  Run database downgrades.
      info       Show information about the current database.
      revision   Create a blank migration file.
      status     Show information about migration status.
      upgrade    Run database upgrades.



## Create Migrations

To create the initial migrations for models, use:

    ./${PACKAGE}/manage.py db create .models

Where `.models` represents the python models module.


## Apply Migrations

To apply migrations on the currently configured database, use:

    ./${PACKAGE}/manage.py db upgrade
    

## Upgrade model

Peewee Moves supports only creating a new model. The alteration of an existing model is done manually
by generating a new revision and editing it. For generating an empty migration, use:

    ./${PACKAGE}/manage.py db revisions alter_model
    
Then update the newly generated file `migrations/0XXX_alter_model.py` to contain the model changes.
The documentation of `peewee-moves` Migrator API can be found
[here](https://peewee-moves.readthedocs.io/en/latest/usage.html#migrator-api).



### Adding/Removing/Renaming a model field

Create an empty revision file, using `manage.py db revisions <revision name>`, then
edit the `upgrade` and `downgrade` sections as follows:

```python
def upgrade(migrator):
    # Add display_name field
    migrator.add_column('user', 'display_name', 'char', max_length=58, null=True)
    
    # Remove role field
    migrator.drop_column('user', 'role')
    
    # Rename key field to password
    migrator.rename_column('user', 'key', 'password')

def downgrade(migrator):
    # Remove display name field
    migrator.drop_column('user', 'display_name')
    
    # Add role field
    migrator.add_column('user', 'role', 'char', max_length=10)
    
    # Rename password field to key
    migrator.rename_columen('user', 'password', 'key')
```


### Custom SQL

Peewee Migrate allows running SQL queries directly in the migrations. Here is an example of how to
do it:

```python
def upgrade(migrator):
    migrator.execute_sql('CREATE INDEX idx_user_email ON user (email)')

def downgrade(migrator):
    migrator.execute_sql('DROP INDEX idx_user_email')
```


### Python script

Peewee Migrate allows running Python code directly in the migrations. Here is an example of how to
do it:

```python
from package_name.models import models

def upgrade(migrator):
    migrator.add_column('user', 'display_name', 'char', max_length=58, null=True)

    query = models.User.update(display_name=fn.UPPER(models.User.username))
    query.execute()


def downgrade(migrator):
    migrator.drop_column('user', 'display_name')
```


## Upgrade from peewee-migrate

Colibris version `<=0.9` used `peewee-migrate` for migrations, but starting with version `0.10`,
it uses `peewee-moves`, a more lightweight manager.

 1. Delete old migrations including `migrations/__init__.py`.
 
 2. Generate an initial migration containing all the application models.

    ```bash
    ./${PACKAGE}/manage.py db create .models
    ```
    
 3. Fake apply the migration into the running environment. This will create the migration table and insert
    the initial migration.

    ```bash
    ./${PACKAGE}/manage.py db upgrade  --fake
    ```
