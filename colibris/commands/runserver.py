
from aiohttp import web

from colibris import settings
from colibris import app

from . import BaseCommand


class RunServerCommand(BaseCommand):
    def execute(self, options):
        web.run_app(app.app, host=settings.LISTEN, port=settings.PORT)
