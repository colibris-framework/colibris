
import importlib

from peewee_migrate import Router

from colibris import persist
from colibris import settings

from . import BaseCommand


class MakeMigrationsCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', help='An optional migration name', type=str, default='auto', nargs='?')

    def execute(self, options):
        router = Router(persist.get_database(), migrate_dir=persist.get_migrations_dir())
        router.create(options.name, auto=importlib.import_module(settings.PROJECT_PACKAGE_NAME))
