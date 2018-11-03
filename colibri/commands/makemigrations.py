
import importlib

from peewee_migrate import Router

from colibri import persist
from colibri import settings

from . import BaseCommand


class MakeMigrationsCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', help='An optional migration name', type=str, default='auto', nargs='?')

    def execute(self, options):
        router = Router(persist.get_database(), migrate_dir=persist.MIGRATIONS_DIR)
        router.create(options.name, auto=importlib.import_module(settings.PROJECT_PACKAGE_NAME))
