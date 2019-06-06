
import logging

from colibris import taskqueue

from .base import BaseCommand


logger = logging.getLogger(__name__)


class RunWorkerCommand(BaseCommand):
    def add_arguments(self, parser):
        taskqueue.add_worker_arguments(parser)

    def execute(self, options):
        taskqueue.run_worker(options)
