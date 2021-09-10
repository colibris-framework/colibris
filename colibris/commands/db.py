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
@click.pass_context
def peewee_moves_cli_proxy(ctx, **kwargs):
    class ScriptInfo:
        def __init__(self):
            self.data = {'manager': None}

    ctx.obj = ctx.obj or ScriptInfo()
    ctx.obj.data['manager'] = DatabaseManager(database=persist.get_database(),
                                              directory=persist.get_migrations_dir())


peewee_moves_cli_proxy.add_command(cli_info)
peewee_moves_cli_proxy.add_command(cli_status)
peewee_moves_cli_proxy.add_command(cli_create)
peewee_moves_cli_proxy.add_command(cli_revision)
peewee_moves_cli_proxy.add_command(cli_upgrade)
peewee_moves_cli_proxy.add_command(cli_downgrade)
peewee_moves_cli_proxy.add_command(cli_delete)


class DBCommand(BaseCommand):

    def parse_arguments(self, parser, args):
        pass

    def execute(self, options):
        peewee_moves_cli_proxy(args=sys.argv[2:])
