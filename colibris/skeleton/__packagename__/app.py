
from colibris import app
from colibris import persist


def init(web_app, loop):
    # Add your coroutines to the loop here.

    pass


def get_health():
    # Determine whether your service is currently healthy.
    # Raise app.HealthException() in case of any problem.

    if not persist.connectivity_check():
        raise app.HealthException('database connectivity check failed')

    return 'healthy'
