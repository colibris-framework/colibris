
import logging

from colibris import monkey as __monkey  # Apply monkey patches before anything else

from colibris import authentication
from colibris import authorization
from colibris import cache
from colibris import commands
from colibris import conf
from colibris import email
from colibris import persist
from colibris import taskqueue
from colibris import template


VERSION = '0.7.1'


def setup():
    authentication.setup()
    authorization.setup()
    cache.setup()
    email.setup()
    persist.setup()
    taskqueue.setup()
    template.setup()


# Initially gather logging records into a memory handler and flush them as soon as logging is properly set up
logging.basicConfig(level=logging.DEBUG, handlers=[conf.get_logging_memory_handler()])


def is_test_mode():
    return isinstance(commands.get_command(), commands.test.TestCommand)
