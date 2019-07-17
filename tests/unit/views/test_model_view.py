import pytest
from aiohttp import web, hdrs
from peewee import SqliteDatabase

from colibris.middleware.errors import handle_errors_json
from colibris.pagination import PageNumberPagination
from colibris.schemas import ModelSchema

from colibris import persist
from colibris.views.generic import ListCreateModelView, RetrieveUpdateDestroyModelView


class Item(persist.Model):
    name = persist.CharField()
    info = persist.CharField()


class ItemSchema(ModelSchema):
    class Meta:
        model = Item


class ItemsView(ListCreateModelView):
    body_schema_class = ItemSchema
    pagination_class = None
    model = Item


class ItemsPaginatedView(ListCreateModelView):
    body_schema_class = ItemSchema
    pagination_class = PageNumberPagination
    model = Item


class ItemView(RetrieveUpdateDestroyModelView):
    body_schema_class = ItemSchema
    model = Item


MODELS = [Item]


@pytest.fixture
def database():
    db = SqliteDatabase(':memory:')
    db.bind(MODELS)
    db.connect()
    db.create_tables(MODELS)


@pytest.fixture
def http(loop, aiohttp_client):
    middlewares = [
        handle_errors_json
    ]

    app = web.Application(middlewares=middlewares)
    app.router.add_route('*', '/paginated-items', ItemsPaginatedView)
    app.router.add_route('*', '/items', ItemsView)
    app.router.add_route('*', '/items/{id}', ItemView)
    return loop.run_until_complete(aiohttp_client(app))


class TestList:
    async def test_get_items(self, database, http):
        response = await http.request(hdrs.METH_GET, '/items')
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)

    async def test_get_pagination_default_page_and_size(self, database, http):
        item__name = 'Ligula Egestas Fermentum'
        item_info = 'Ridiculus Fermentum Quam Porta'

        Item.create(name=item__name, info=item_info)

        response = await http.request(hdrs.METH_GET, '/paginated-items')
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, dict)
        assert 'results' in data
        assert 'count' in data
        assert 'pages' in data
        assert 'page' in data
        assert 'page_size' in data

    async def test_get_pagination_different_page(self, database, http):
        item_info = 'Ridiculus Fermentum Quam Porta'
        first_item_name = 'Ligula Egestas Fermentum'
        second_item_name = 'Euismod Ipsum Vulputate'
        third_item_name = 'Pellentesque Sit Venenatis'

        Item.create(name=first_item_name, info=item_info)
        Item.create(name=second_item_name, info=item_info)
        Item.create(name=third_item_name, info=item_info)

        response = await http.request(hdrs.METH_GET, '/paginated-items', params={'page_size': 1, 'page': 1})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, dict)
        assert data['count'] == 3
        assert data['page'] == 1
        assert data['page_size'] == 1
        assert data['results'][0]['name'] == third_item_name

        response = await http.request(hdrs.METH_GET, '/paginated-items', params={'page_size': 1, 'page': 2})
        assert response.status == 200
        data = await response.json()
        assert data['results'][0]['name'] == second_item_name

        response = await http.request(hdrs.METH_GET, '/paginated-items', params={'page_size': 1, 'page': 3})
        assert response.status == 200
        data = await response.json()
        assert data['results'][0]['name'] == first_item_name

        response = await http.request(hdrs.METH_GET, '/paginated-items', params={'page_size': 1, 'page': 4})
        assert response.status == 200
        data = await response.json()
        assert data['results'] == []


class TestCreate:
    async def test_create_item(self, database, http):
        item_name = 'Commodo Nibh'
        item_info = 'Cras Lorem Purus Etiam Venenatis'

        response = await http.request(hdrs.METH_POST, '/items', json={'name': item_name, 'info': item_info})

        assert response.status == 201

        item = Item.select().where(Item.name == item_name).get()

        assert item.name == item_name

    async def test_create_item_validation(self, database, http):
        response = await http.request(hdrs.METH_POST, '/items')

        assert response.status == 400
        data = await response.json()
        assert 'name' in data['details']
        assert 'info' in data['details']


class TestUpdate:
    async def test_update_item(self, database, http):
        item_initial_name = 'Ligula Egestas Fermentum'
        item_updated_name = 'Cursus Inceptos'
        item_info = 'Ridiculus Fermentum Quam Porta'

        item = Item.create(name=item_initial_name, info=item_info)

        response = await http.request(hdrs.METH_PATCH, '/items/{}'.format(item.id), json={'name': item_updated_name})

        assert response.status == 200

        updated_item = Item.select().where(Item.name == item_updated_name).get()

        assert item.id == updated_item.id

    async def test_update_item_validation(self, database, http):
        item_initial_name = 'Nibh Lorem Amet Aenean'
        item_info = 'Ridiculus Fermentum Quam Porta'

        item = Item.create(name=item_initial_name, info=item_info)

        response = await http.request(hdrs.METH_PATCH, '/items/{}'.format(item.id), json={'name': None})

        assert response.status == 400

        data = await response.json()
        assert 'name' in data['details']

    async def test_update_item_not_found(self, database, http):
        response = await http.request(hdrs.METH_PATCH, '/items/11011', json={'name': 'Egestas Fringilla'})

        assert response.status == 404


class TestDestroy:
    async def test_delete_item(self, database, http):
        item_name = 'Sit Lorem'
        item_info = 'Ridiculus Fermentum Quam Porta'

        item = Item.create(name=item_name, info=item_info)

        response = await http.request(hdrs.METH_DELETE, '/items/{}'.format(item.id))

        assert response.status == 204

        items = Item.select().where(Item.name == item_name)
        assert items.count() == 0

    async def test_delete_item_not_found(self, database, http):
        response = await http.request(hdrs.METH_DELETE, '/items/111111')

        assert response.status == 404
