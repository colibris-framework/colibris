
import code
import importlib

from colibri import settings

from . import BaseCommand


class ShellCommand(BaseCommand):
    def execute(self, options):
        # have models automatically imported into locals()
        models = importlib.import_module('{}.models'.format(settings.PROJECT_PACKAGE_NAME))

        code.interact(local=locals())
