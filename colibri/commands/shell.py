
import code

from . import BaseCommand


class ShellCommand(BaseCommand):
    def execute(self, options):
        # stuff to pass to locals()
        import colibri.persist
        import colibri.settings

        code.interact(local=locals())
