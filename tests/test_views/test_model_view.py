import pytest
from aiohttp import web, hdrs
from peewee import SqliteDatabase

from colibris.middleware.errors import handle_errors_json
from colibris.schemas import ModelSchema

from colibris import persist
from colibris.views.generic import ListCreateModelView, RetrieveUpdateDestroyModelView

db = SqliteDatabase(':memory:')


class Item(persist.Model):
    name = persist.CharField()
    info = persist.CharField()


class ItemSchema(ModelSchema):
    class Meta:
        model = Item


class ItemsView(ListCreateModelView):
    body_schema_class = ItemSchema
    model = Item


class ItemView(RetrieveUpdateDestroyModelView):
    body_schema_class = ItemSchema
    model = Item


MODELS = [Item]


@pytest.fixture
def http_client(loop, aiohttp_client):
    middlewares = [
        handle_errors_json
    ]

    app = web.Application(middlewares=middlewares)
    app.router.add_route('*', '/items', ItemsView)
    app.router.add_route('*', '/items/{id}', ItemView)
    return loop.run_until_complete(aiohttp_client(app))


def setup_module(module):
    db.bind(MODELS)

    db.connect()
    db.create_tables(MODELS)


async def test_get_items(http_client):
    response = await http_client.request(hdrs.METH_GET, "/items")
    assert response.status == 200


async def test_create_item(http_client):
    item_name = 'Commodo Nibh'
    item_info = 'Cras Lorem Purus Etiam Venenatis'

    response = await http_client.request(hdrs.METH_POST, "/items", json={'name': item_name, 'info': item_info})

    assert response.status == 201

    item = Item.select().where(Item.name == item_name).get()

    assert item.name == item_name


async def test_create_item_validation(http_client):
    response = await http_client.request(hdrs.METH_POST, "/items")

    assert response.status == 400
    data = await response.json()
    assert 'name' in data['details']
    assert 'info' in data['details']


async def test_update_item(http_client):
    item_initial_name = 'Ligula Egestas Fermentum'
    item_updated_name = 'Cursus Inceptos'
    item_info = 'Ridiculus Fermentum Quam Porta'

    item = Item.create(name=item_initial_name, info=item_info)

    response = await http_client.request(hdrs.METH_PATCH, f"/items/{item.id}", json={'name': item_updated_name})

    assert response.status == 200

    updated_item = Item.select().where(Item.name == item_updated_name).get()

    assert item.id == updated_item.id


async def test_update_item_validation(http_client):
    item_initial_name = 'Nibh Lorem Amet Aenean'
    item_info = 'Ridiculus Fermentum Quam Porta'

    item = Item.create(name=item_initial_name, info=item_info)

    response = await http_client.request(hdrs.METH_PATCH, f"/items/{item.id}", json={'name': None})

    assert response.status == 400

    data = await response.json()
    assert 'name' in data['details']


async def test_update_item_not_found(http_client):
    response = await http_client.request(hdrs.METH_PATCH, f"/items/11011", json={'name': 'Egestas Fringilla'})

    assert response.status == 404


async def test_delete_item(http_client):
    item_name = 'Sit Lorem'
    item_info = 'Ridiculus Fermentum Quam Porta'

    item = Item.create(name=item_name, info=item_info)

    response = await http_client.request(hdrs.METH_DELETE, f"/items/{item.id}")

    assert response.status == 204

    items = Item.select().where(Item.name == item_name)
    assert items.count() == 0


async def test_delete_item_not_found(http_client):
    response = await http_client.request(hdrs.METH_DELETE, f"/items/111111")

    assert response.status == 404
