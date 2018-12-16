
class TaskQueueBackend:
    async def execute(self, func, *args, timeout, **kwargs):
        raise NotImplementedError

    def add_worker_arguments(self, parser):
        pass

    def run_worker(self, options):
        raise NotImplementedError
