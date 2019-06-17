
import logging
import os
import pytest
import _pytest.config.argparsing

from colibris.conf import settings

from .base import BaseCommand


logger = logging.getLogger(__name__)

_PLUGINS = [
    'aiohttp.pytest_plugin',
    'colibris.test'
]

_TESTS_DIR = 'tests'


class TestCommand(BaseCommand):
    ADD_HELP = False

    def initialize(self):
        # Adjust main program invocation (should be "manage.py test")
        _pytest.config.argparsing.Parser.prog = self.make_prog()

        # Prepare database settings for testing
        if 'name' in settings.DATABASE:
            settings.DATABASE['name'] = 'test_' + settings.DATABASE['name']
            settings.DATABASE['create'] = True

        # colibris.setup() will be called at the setup phase of each test

    def parse_arguments(self, parser, args):
        # Use pytest internal arg parser instead of the command's default parser.
        return None

    def execute(self, options):
        tests_dir = os.path.join(settings.PROJECT_PACKAGE_DIR, '..', _TESTS_DIR)
        os.chdir(tests_dir)

        pytest.main(self.args, plugins=_PLUGINS)
