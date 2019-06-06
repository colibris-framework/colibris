

class TaskQueueException(Exception):
    pass


class TimeoutException(TaskQueueException):
    def __init__(self, timeout):
        super().__init__('task did not complete within {} seconds'.format(timeout))


class TaskExecException(TaskQueueException):
    def __init__(self, exc_str):
        self.exc_str = exc_str

    def __str__(self):
        return 'exception while executing task:\n{}'.format(self.exc_str)
