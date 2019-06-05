

from colibris import monkey  # Apply monkey patches before anything else

from colibris.conf import settings

from colibris import authorization
from colibris import cache
from colibris import email
from colibris import persist
from colibris import taskqueue
from colibris import template


VERSION = '0.6.2'


def setup():
    authorization.setup()
    cache.setup()
    email.setup()
    persist.setup()
    taskqueue.setup()
    template.setup()
