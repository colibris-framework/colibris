
import sys

from peewee_moves import cli_command

from colibris import persist

from .base import BaseCommand


class DBCommand(BaseCommand):

    def parse_arguments(self, parser, args):
        pass

    def execute(self, options):
        # proxy to peewee moves cli
        cli_command(
            default_map={
                "directory": persist.get_migrations_dir(),
                "database": persist.get_database,
            },
            args=sys.argv[2:],
        )
