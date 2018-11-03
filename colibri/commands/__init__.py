
import sys
import argparse


class BaseCommand:
    def __init__(self, args):
        self.args = args
        self.parser = argparse.ArgumentParser()
        self.add_arguments(self.parser)

    def add_arguments(self, parser):
        pass

    def execute(self, options):
        raise NotImplementedError

    def run(self):
        options = self.parser.parse_args(self.args)
        self.execute(options)

    @classmethod
    def get_name(cls):
        return cls.__name__[0:-7].lower()


def show_commands_usage():
    cmds = '\n  '.join([c.get_name() for c in ALL_COMMANDS.values()])
    usage = '{prog} <command> [args]\n\n' \
            'available commands:\n  {cmds}\n\n' \
            'use {prog} <command> -h for help'

    usage = usage.format(cmds=cmds, prog='manage.py')

    print(usage)


def main():
    args = sys.argv
    if len(args) < 2 or args[1] not in ALL_COMMANDS:
        show_commands_usage()
        sys.exit(1)

    command_class = ALL_COMMANDS[sys.argv[1]]
    command = command_class(args[2:])
    command.run()


from . import makemigrations
from . import migrate
from . import runserver
from . import shell

ALL_COMMANDS = {c.get_name(): c for c in BaseCommand.__subclasses__()}
