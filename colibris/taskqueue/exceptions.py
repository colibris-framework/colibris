
from colibris.utils import ClassNameException


class TaskQueueException(ClassNameException):
    pass


class UnpicklableException(TaskQueueException):
    def __init__(self, exc_str):
        self.exc_str = exc_str

    def __str__(self):
        return self.exc_str

