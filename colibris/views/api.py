from json import JSONDecodeError

from aiohttp import web
from marshmallow import ValidationError

from colibris import api


class APIView(web.View):
    body_schema_class = None
    query_schema_class = None

    def get_body_schema_class(self, *args, **kwargs):
        assert self.body_schema_class is not None, 'The attribute "body_schema_class" is required for {}'.format(self)

        kwargs.update({
            'context': {'request': self.request}
        })

        schema = self.body_schema_class(*args, **kwargs)

        return schema

    def get_query_schema_class(self, *args, **kwargs):
        assert self.query_schema_class is not None, 'The attribute "query_schema_class" is required for {}'.format(self)

        kwargs.update({
            'context': {'request': self.request}
        })

        schema = self.query_schema_class(*args, **kwargs)

        return schema

    async def get_validated_body(self, schema=None):
        if schema is None:
            schema = self.get_body_schema_class()

        json_payload = await self.get_request_payload()

        try:
            data = schema.load(json_payload)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

        return data

    async def get_request_payload(self):
        if not self.request.can_read_body:
            return {}

        try:
            json_payload = await self.request.json()
        except JSONDecodeError:
            raise api.JSONParseError()

        return json_payload

    async def get_validated_query(self, schema=None):
        if schema is None:
            schema = self.get_query_schema_class()

        query = await self.get_request_query()

        try:
            data = schema.load(query)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

        return data

    async def get_request_query(self):
        return self.request.query
