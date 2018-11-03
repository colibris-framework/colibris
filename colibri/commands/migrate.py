
from peewee_migrate import Router

from colibri import persist

from . import BaseCommand


class MigrateCommand(BaseCommand):
    def execute(self, options):
        router = Router(persist.get_database(), migrate_dir=persist.MIGRATIONS_DIR)
        router.run()
