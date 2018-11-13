
from aiohttp import web

from colibris import settings
from colibris import webapp

from . import BaseCommand


class RunServerCommand(BaseCommand):
    def execute(self, options):
        web.run_app(webapp.app, host=settings.LISTEN, port=settings.PORT)
