
import code

from colibris import utils
from colibris.conf import settings

from .base import BaseCommand


class ShellCommand(BaseCommand):
    def execute(self, options):
        # have models automatically imported into locals
        loc = locals()
        models = utils.import_module_or_none('{}.models'.format(settings.PROJECT_PACKAGE_NAME))
        if models:
            loc['models'] = models

        code.interact(local=loc)
