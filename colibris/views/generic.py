from aiohttp import web
from aiohttp_apispec import docs

from colibris import app
from colibris.views.mixins import ListMixin, CreateMixin, RetrieveMixin, UpdateMixin, DestroyMixin
from colibris.views.model import ModelView


class ListCreateModelView(ModelView, ListMixin, CreateMixin):
    pass


class RetrieveUpdateDeleteModelView(ModelView, RetrieveMixin, UpdateMixin, DestroyMixin):
    pass
