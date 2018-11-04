
from aiohttp import web
from aiohttp_apispec import docs

from colibri import settings


def home(request):
    raise web.HTTPFound(settings.API_DOCS_PATH)


@docs(summary='The health-check endpoint')
def health(request):
    return web.json_response({'detail': 'ok'})
