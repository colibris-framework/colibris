
import logging
import os

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
        import _pytest.config.argparsing

        # Adjust main program invocation (should be "manage.py test")
        _pytest.config.argparsing.Parser.prog = self.make_prog()

        # Prepare database settings for testing
        if 'name' in settings.DATABASE or 'name' in settings.TEST_DATABASE:
            settings.DATABASE.update(settings.TEST_DATABASE)
            if 'name' not in settings.TEST_DATABASE:
                settings.DATABASE['name'] = 'test_' + settings.DATABASE['name']

            settings.DATABASE['create'] = True  # We want dbs to be created when running tests

        # colibris.setup() will be called at the setup phase of each test

    def parse_arguments(self, parser, args):
        # Use pytest internal arg parser instead of the command's default parser.
        return None

    def execute(self, options):
        import pytest

        has_file_or_dir = any(True for arg in self.args if not arg.startswith('-'))

        # Run tests from the project's tests subpackage unless a file or directory is given as argument
        if not has_file_or_dir:
            tests_dir = os.path.join(settings.PROJECT_PACKAGE_DIR, _TESTS_DIR)
            os.chdir(tests_dir)

        plugins = list(_PLUGINS)
        # Use project's fixtures as a plugin so that project-specific fixtures are loaded
        plugins.append('{}.tests.fixtures'.format(settings.PROJECT_PACKAGE_NAME))

        return pytest.main(self.args, plugins=plugins)
