
import logging

from colibris import commands
from colibris import taskqueue


logger = logging.getLogger(__name__)


class RunWorkerCommand(commands.BaseCommand):
    def add_arguments(self, parser):
        taskqueue.add_worker_arguments(parser)

    def execute(self, options):
        taskqueue.run_worker(options)
