
import sys
from peewee_migrate.cli import cli

from colibris import persist
from colibris.conf import settings

from .base import BaseCommand


class DBCommand(BaseCommand):

    def execute(self, options):
        cli(
            default_map={
                "directory": persist.get_migrations_dir(),
                "database": persist.get_database,
            },
            args=sys.argv[2:]
        )
