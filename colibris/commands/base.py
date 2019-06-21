
import argparse
import sys

import colibris


class BaseCommand:
    PROG = None
    USAGE = None
    DESCRIPTION = None
    EPILOG = None
    ADD_HELP = True

    def __init__(self, args):
        self.args = args
        self.parser = self.make_argument_parser()
        self.add_arguments(self.parser)
        self.initialize()

    def initialize(self):
        colibris.setup()

    def run(self):
        options = self.parse_arguments(self.parser, self.args)
        return self.execute(options)

    def make_argument_parser(self):
        return argparse.ArgumentParser(prog=self.PROG or self.make_prog(),
                                       usage=self.USAGE,
                                       description=self.DESCRIPTION,
                                       epilog=self.EPILOG,
                                       add_help=self.ADD_HELP)

    def make_prog(self):
        return '{arg0} {cmd}'.format(arg0=sys.argv[0], cmd=self.get_name())

    def add_arguments(self, parser):
        pass

    def parse_arguments(self, parser, args):
        return parser.parse_args(args)

    def execute(self, options):
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        return cls.__name__[0:-7].lower()
