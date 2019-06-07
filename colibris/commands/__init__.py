
import logging.config
import sys

import colibris

from colibris import conf
from colibris import utils
from colibris import settings


from .base import BaseCommand


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


def main():
    conf.setup()

    gather_all_commands()

    args = sys.argv
    if len(args) < 2 or args[1] not in ALL_COMMANDS:
        show_commands_usage()
        sys.exit(1)

    colibris.setup()

    command_class = ALL_COMMANDS[sys.argv[1]]
    command = command_class(args[2:])
    command.run()


from . import makemigrations
from . import migrate
from . import runserver
from . import runworker
from . import shell
