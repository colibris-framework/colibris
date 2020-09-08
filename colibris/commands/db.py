
import importlib
import sys

from peewee_migrate.cli import cli

from colibris import persist
from colibris.conf import settings

from .base import BaseCommand


class DBCommand(BaseCommand):

    def parse_arguments(self, parser, args):
        pass

    def execute(self, options):
        defaults = {
            "directory": persist.get_migrations_dir(),
            "database": persist.get_database,
            "auto": True,
            "auto_source": settings.PROJECT_PACKAGE_NAME,
        }
        cli(
            default_map={cmd: defaults for cmd in ['list', 'create', 'merge', 'migrate', 'rollback']},
            args=sys.argv[2:]
        )
