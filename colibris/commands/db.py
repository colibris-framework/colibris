import sys

import click
from peewee_moves import (
    DatabaseManager,
    cli_info,
    cli_status,
    cli_create,
    cli_revision,
    cli_upgrade,
    cli_downgrade,
    cli_delete
)

from colibris import persist
from .base import BaseCommand


@click.group()
@click.option("--directory")
@click.option("--database")
@click.option("--table")
@click.pass_context
def db_command_proxy(ctx, **kwargs):
    class ScriptInfo:
        def __init__(self):
            self.data = {'manager': None}

    ctx.obj = ctx.obj or ScriptInfo()
    ctx.obj.data['manager'] = DatabaseManager(database=persist.get_database(),
                                              directory=persist.get_migrations_dir())


db_command_proxy.add_command(cli_info)
db_command_proxy.add_command(cli_status)
db_command_proxy.add_command(cli_create)
db_command_proxy.add_command(cli_revision)
db_command_proxy.add_command(cli_upgrade)
db_command_proxy.add_command(cli_downgrade)
db_command_proxy.add_command(cli_delete)


class DBCommand(BaseCommand):

    def parse_arguments(self, parser, args):
        pass

    def execute(self, options):
        db_command_proxy(args=sys.argv[2:])
