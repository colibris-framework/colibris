import json
from json import JSONDecodeError

from marshmallow import ValidationError

from colibris import api
from colibris.views.base import View

REQUEST_BODY_KEY = 'body_text'


class APIView(View):
    body_schema_class = None
    query_schema_class = None

    async def _iter(self):
        await self.prepare()

        return await super()._iter()

    async def prepare(self):
        self.request[REQUEST_BODY_KEY] = await self.request.text()

    def get_body_schema(self, *args, **kwargs):
        assert self.body_schema_class is not None, 'The attribute "body_schema_class" is required for {}'.format(self)

        kwargs.update({
            'context': {'request': self.request}
        })

        schema = self.body_schema_class(*args, **kwargs)

        return schema

    def get_query_schema(self, *args, **kwargs):
        assert self.query_schema_class is not None, 'The attribute "query_schema_class" is required for {}'.format(self)

        kwargs.update({
            'context': {'request': self.request}
        })

        schema = self.query_schema_class(*args, **kwargs)

        return schema

    def get_validated_body(self, schema=None):
        if schema is None:
            schema = self.get_body_schema()

        json_payload = self.get_request_body()

        try:
            data = schema.load(json_payload)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

        return data

    def get_request_body(self):
        if not self.request.body_exists:
            return {}

        try:
            json_payload = json.loads(self.request[REQUEST_BODY_KEY])
        except JSONDecodeError:
            raise api.JSONParseError()

        return json_payload

    def get_validated_query(self, schema=None):
        if schema is None:
            schema = self.get_query_schema()

        query = self.get_request_query()

        try:
            data = schema.load(query)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

        return data

    def get_request_query(self):
        return self.request.query
