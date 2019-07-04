import pytest
from aiohttp import web
from peewee import SqliteDatabase

from colibris.schemas import ModelSchema

from colibris import persist
from colibris.views import ListCreateModelView, RetrieveUpdateDeleteModelView

db = SqliteDatabase(':memory:')


class Item(persist.Model):
    name = persist.CharField()


class ItemSchema(ModelSchema):
    class Meta:
        model = Item


class ItemsView(ListCreateModelView):
    schema_class = ItemSchema
    model = Item


class ItemView(RetrieveUpdateDeleteModelView):
    schema_class = ItemSchema
    model = Item


MODELS = [Item]


@pytest.fixture
def http_client(loop, aiohttp_client):
    app = web.Application()
    app.router.add_route('*', '/items', ItemsView)
    app.router.add_route('*', '/items/{id}', ItemView)
    return loop.run_until_complete(aiohttp_client(app))


def setup_module(module):
    db.bind(MODELS)

    db.connect()
    db.create_tables(MODELS)


async def test_get_items(http_client):
    resp = await http_client.request("GET", "/items")
    assert resp.status == 200


async def test_create_item(http_client):
    item_name = 'Some Good Name'

    resp = await http_client.request("POST", "/items", json={'name': 'Some Good Name'})

    assert resp.status == 201

    item = Item.select().where(Item.name == item_name).get()

    assert item.name == item_name


async def test_update_item(http_client):
    item_initial_name = 'Some Initial Name'
    item_updated_name = 'Some Updated Name'

    item = Item.create(name=item_initial_name)

    resp = await http_client.request("PATCH", f"/items/{item.id}", json={'name': item_updated_name})

    assert resp.status == 200

    updated_item = Item.select().where(Item.name == item_updated_name).get()

    assert item.id == updated_item.id


async def test_delete_item(http_client):
    item_name = 'Item to delete'

    item = Item.create(name=item_name)

    resp = await http_client.request("DELETE", f"/items/{item.id}")

    assert resp.status == 204

    items = Item.select().where(Item.name == item_name)
    assert items.count() == 0
