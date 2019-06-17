
from aiohttp import web

from colibris import app
from colibris.conf import settings

from .base import BaseCommand


class RunServerCommand(BaseCommand):
    def execute(self, options):
        web.run_app(app.get_web_app(), host=settings.LISTEN, port=settings.PORT)
