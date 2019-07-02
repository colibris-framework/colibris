from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import response_schema, request_schema
from marshmallow import Schema, ValidationError
from peewee import IntegrityError

from colibris import app, api
from colibris.api.envelope import many_envelope
from colibris.conf import settings


async def home(request):
    raise web.HTTPFound(settings.API_DOCS_PATH)


# TODO: I would suggest to move it into some template.
@docs(tags=['Service'],
      summary='The health-check endpoint')
async def health(request):
    h = await app.get_health()
    return web.json_response(h)


class ListMixin:
    request = None
    schema_class = Schema

    @response_schema(many_envelope(schema_class))
    async def get(self):
        items = self.get_query()
        result = self.schema_class(many=True, context={'request': self.request}).dump(list(items))

        return web.json_response(result)


class CreateMixin:
    request = None
    schema_class = Schema

    @request_schema(schema_class)
    @response_schema(schema_class)
    async def post(self):
        schema = self.schema_class(context={'request': self.request})
        json_payload = await self.request.json()

        try:
            data = schema.load(json_payload)
        except ValidationError as err:
            raise api.InvalidRequest(code='invalid_request', message=err.messages)

        try:
            item = self.model.create(**data)
        except IntegrityError as err:
            raise api.InvalidRequest(code='invalid_request', message=str(err))

        result = schema.dump(item)

        return web.json_response(result, status=201)


class RetrieveMixin:
    request = None
    schema_class = Schema

    @response_schema(many_envelope(schema_class))
    async def get(self):
        schema = self.schema_class(context={'request': self.request})

        instance = self.get_object()
        result = schema.dump(instance)

        return web.json_response(result)


class UpdateMixin:
    request = None
    schema_class = Schema

    @request_schema(schema_class)
    @response_schema(schema_class)
    async def patch(self):
        schema = self.schema_class(partial=True, context={'request': self.request})
        json_payload = await self.request.json()

        instance = self.get_object()

        try:
            data: dict = schema.load(json_payload)
        except ValidationError as err:
            raise api.InvalidRequest(code='invalid_request', message=err.messages)

        instance.update_fields(data)

        try:
            instance.save(only=data.keys())
        except IntegrityError as err:
            raise api.InvalidRequest(code='invalid_request', message=str(err))

        result = schema.dump(instance)

        return web.json_response(result)

    @request_schema(schema_class)
    @response_schema(schema_class)
    async def put(self):
        schema = self.schema_class(context={'request': self.request})
        json_payload = await self.request.json()

        instance = self.get_object()

        try:
            data: dict = schema.load(json_payload)
        except ValidationError as err:
            raise api.InvalidRequest(code='invalid_request', message=err.messages)

        instance.update_fields(data)

        try:
            instance.save()
        except IntegrityError as err:
            raise api.InvalidRequest(code='invalid_request', message=str(err))

        result = schema.dump(instance)

        return web.json_response(result)


class DestroyMixin:
    async def delete(self):
        instance = self.get_object()
        instance.delete_instance()

        return web.json_response(status=204)


class BaseView(web.View):
    model = None
    lookup_field = 'id'

    def get_query(self):
        return self.model.select().order_by(self.model.id.desc())

    def get_object(self):
        object_identifier = self.request.match_info[self.lookup_field]

        try:
            instance = self.get_query().where(getattr(self.model, self.lookup_field) == object_identifier).get()
        except self.model.DoesNotExist:
            raise api.ModelNotFoundException(self.model)

        return instance


class ListCreateModelView(BaseView, ListMixin, CreateMixin):
    pass


class RetrieveUpdateDeleteModelView(BaseView, RetrieveMixin, UpdateMixin, DestroyMixin):
    pass
