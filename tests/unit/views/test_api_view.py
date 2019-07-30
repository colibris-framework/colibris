import pytest

from aiohttp import web
from marshmallow import Schema, fields

from colibris.views import APIView
from colibris.middleware.errors import handle_errors_json


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
        query = await self.get_validated_query()

        return web.json_response({'query': query})

    async def post(self):
        query = await self.get_validated_query()
        body = await self.get_validated_body()

        return web.json_response({'query': query, 'body': body})


@pytest.fixture
async def http_client(http_client_maker):
    return await http_client_maker(middlewares=[handle_errors_json],
                                   routes=[('/items', ItemsView)])


async def test_get(http_client):
    sent_args = {
        'count': '222'
    }
    expected_args = {
        'count': 222
    }

    response = await http_client.get('/items', params=sent_args)

    assert response.status == 200

    data = await response.json()
    query = data['query']

    assert expected_args == query


async def test_post_body(http_client):
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

    response = await http_client.post('/items', json=sent_data)

    assert response.status == 200

    data = await response.json()
    body = data['body']

    assert expected_data == body


async def test_post_query(http_client):
    sent_data = {
        'count': '22',
    }
    expected_data = {
        'count': 22,
    }

    response = await http_client.post('/items', params=sent_data)

    assert response.status == 200

    data = await response.json()
    query = data['query']

    assert expected_data == query
