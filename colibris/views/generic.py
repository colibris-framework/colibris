from aiohttp import web
from aiohttp_apispec import docs

from colibris import app
from colibris.conf import settings
from colibris.views.mixins import ListMixin, CreateMixin, RetrieveMixin, UpdateMixin, DestroyMixin
from colibris.views.model import ModelView


class View(web.View):
    pass


async def home(request):
    raise web.HTTPFound(settings.API_DOCS_PATH)


@docs(tags=['Service'],
      summary='The health-check endpoint')
async def health(request):
    h = await app.get_health()
    return web.json_response(h)


class ListCreateModelView(ModelView, ListMixin, CreateMixin):
    pass


class RetrieveUpdateDeleteModelView(ModelView, RetrieveMixin, UpdateMixin, DestroyMixin):
    pass
