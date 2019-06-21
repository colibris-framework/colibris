
import sys

from colibris import conf
from colibris import utils
from colibris.conf import settings

from .base import BaseCommand

from . import makemigrations
from . import migrate
from . import runserver
from . import runworker
from . import shell
from . import test


_command = None  # Currently running command


def gather_all_commands():
    global ALL_COMMANDS

    # Import any project-specific commands
    utils.import_module_or_none('{}.commands'.format(settings.PROJECT_PACKAGE_NAME))

    ALL_COMMANDS = {c.get_name(): c for c in BaseCommand.__subclasses__()}


def show_commands_usage():
    cmds = '\n  '.join([c.get_name() for c in ALL_COMMANDS.values()])
    usage = '{prog} <command> [args]\n\n' \
            'available commands:\n  {cmds}\n\n' \
            'use {prog} <command> -h for help'

    usage = usage.format(cmds=cmds, prog='manage.py')

    print(usage)


def get_command():
    return _command


def main():
    global _command

    conf.setup()

    gather_all_commands()

    args = sys.argv
    if len(args) < 2 or args[1] not in ALL_COMMANDS:
        show_commands_usage()
        sys.exit(1)

    command_class = ALL_COMMANDS[sys.argv[1]]
    _command = command_class(args[2:])
    exit_code = _command.run() or 0

    sys.exit(exit_code)
