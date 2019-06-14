
import logging
import pytest
import _pytest.config.argparsing

from .base import BaseCommand


logger = logging.getLogger(__name__)


class TestCommand(BaseCommand):
    ADD_HELP = False

    def initialize(self):
        _pytest.config.argparsing.Parser.prog = self.make_prog()

    def parse_arguments(self, parser, args):
        # Use pytest internal arg parser instead of the command's default parser.
        return None

    def execute(self, options):
        pytest.main(self.args)
