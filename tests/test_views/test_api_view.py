import pytest
from aiohttp import web, hdrs
from marshmallow import Schema, fields

from colibris.middleware.errors import handle_errors_json

from colibris.views import APIView


class ItemSchema(Schema):
    name = fields.String()
    info = fields.String()
    count = fields.Integer()


class QuerySchema(Schema):
    count = fields.Integer()


class ItemsView(APIView):
    body_schema_class = ItemSchema
    query_schema_class = QuerySchema

    async def get(self):
        args = await self.get_validated_query()

        return web.json_response(args)

    async def post(self):
        data = await self.get_validated_body()

        return web.json_response(data)


@pytest.fixture
def http_client(loop, aiohttp_client):
    middlewares = [
        handle_errors_json
    ]

    app = web.Application(middlewares=middlewares)
    app.router.add_route('*', '/items', ItemsView)

    return loop.run_until_complete(aiohttp_client(app))


async def test_get(http_client):
    sent_args = {
        'count': '222'
    }
    expected_args = {
        'count': 222
    }

    response = await http_client.request(hdrs.METH_GET, "/items", params=sent_args)

    assert response.status == 200

    actual_data = await response.json()

    assert expected_args == actual_data


async def test_post(http_client):
    sent_data = {
        'name': 'Risus Fusce',
        'info': 'Egestas Lorem Sit Fringilla',
        'count': '22',
    }
    expected_data = {
        'name': 'Risus Fusce',
        'info': 'Egestas Lorem Sit Fringilla',
        'count': 22,
    }

    response = await http_client.request(hdrs.METH_POST, "/items", json=sent_data)

    assert response.status == 200

    actual_data = await response.json()

    assert expected_data == actual_data
