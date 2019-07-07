import abc
import traceback
from json import JSONDecodeError

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import response_schema, request_schema

from colibris.persist import Model
from colibris.schemas import ModelSchema
from marshmallow import ValidationError
from peewee import IntegrityError

from colibris import app, api
from colibris.conf import settings


async def home(request):
    raise web.HTTPFound(settings.API_DOCS_PATH)


# TODO: I would suggest to move it into some template.
@docs(tags=['Service'],
      summary='The health-check endpoint')
async def health(request):
    h = await app.get_health()
    return web.json_response(h)


class _GenericMixinMeta(abc.ABCMeta):
    def __init__(cls, name, bases, attrs):
        assert cls.schema_class, 'The "schema_class" field is required for {}.'.format(cls)
        assert cls.model, 'The "model" field is required for {}.'.format(cls)

        correct_model = issubclass(cls.model, Model)
        correct_schema = issubclass(cls.schema_class, ModelSchema)
        assert correct_model is True, 'The "model" should be a subclass of {}.'.format(Model)
        assert correct_schema is True, 'The "schema_class" should be a subclass of {}.'.format(ModelSchema)

        if hasattr(cls, 'get'):
            cls.get = response_schema(cls.schema_class)(cls.get)

        if hasattr(cls, 'post'):
            cls.post = request_schema(cls.schema_class)(response_schema(cls.schema_class)(cls.post))

        if hasattr(cls, 'put'):
            cls.put = request_schema(cls.schema_class)(response_schema(cls.schema_class)(cls.put))

        if hasattr(cls, 'patch'):
            cls.patch = request_schema(cls.schema_class)(response_schema(cls.schema_class)(cls.patch))

        super().__init__(name, bases, attrs)


class ListMixin(metaclass=_GenericMixinMeta):
    model = Model
    schema_class = ModelSchema

    async def get(self):
        items = self.get_query()
        schema = self.get_schema(many=True)
        result = schema.dump(list(items))

        return web.json_response(result)


class CreateMixin(metaclass=_GenericMixinMeta):
    model = Model
    schema_class = ModelSchema

    async def post(self):
        schema = self.get_schema()
        data = await self.get_validated_data(schema)

        try:
            item = self.model.create(**data)
        except IntegrityError as err:
            traceback.print_exc()
            raise api.ServerError(code='server_error', message=str(err))

        result = schema.dump(item)

        return web.json_response(result, status=201)


class RetrieveMixin(metaclass=_GenericMixinMeta):
    model = Model
    schema_class = ModelSchema

    async def get(self):
        schema = self.get_schema()
        instance = self.get_object()

        result = schema.dump(instance)

        return web.json_response(result)


class UpdateMixin(metaclass=_GenericMixinMeta):
    model = Model
    schema_class = ModelSchema

    async def patch(self):
        schema = self.get_schema(partial=True)
        data = await self.get_validated_data(schema)

        instance = self.get_object()
        instance.update_fields(data)

        try:
            instance.save(only=data.keys())
        except IntegrityError as err:
            traceback.print_exc()
            raise api.ServerError(code='server_error', message=str(err))

        result = schema.dump(instance)

        return web.json_response(result)

    async def put(self):
        schema = self.get_schema()
        data = await self.get_validated_data(schema)

        instance = self.get_object()
        instance.update_fields(data)

        try:
            instance.save()
        except IntegrityError as err:
            traceback.print_exc()
            raise api.ServerError(code='server_error', message=str(err))

        result = schema.dump(instance)

        return web.json_response(result)


class DestroyMixin:
    async def delete(self):
        instance = self.get_object()
        instance.delete_instance()

        return web.json_response(status=204)


class BaseModelView(web.View):
    model = Model
    schema_class = ModelSchema
    url_identifier = 'id'
    lookup_field = 'id'

    def get_query(self):
        return self.model.select().order_by(self.model.id.desc())

    def get_object(self):
        identifier_value = self.request.match_info[self.url_identifier]

        try:
            instance = self.get_query().where(getattr(self.model, self.lookup_field) == identifier_value).get()
        except self.model.DoesNotExist:
            raise api.ModelNotFoundException(self.model)

        return instance

    def get_schema(self, *args, **kwargs):
        kwargs.update({
            'context': {'request': self.request}
        })

        schema = self.schema_class(*args, **kwargs)

        return schema

    async def get_validated_data(self, schema):
        json_payload = await self.get_request_payload()

        try:
            data = schema.load(json_payload)
        except ValidationError as err:
            raise api.InvalidRequest(code='invalid_request', message=err.messages)

        return data

    async def get_request_payload(self):
        try:
            json_payload = await self.request.json()
        except JSONDecodeError:
            raise api.JSONParseError()

        return json_payload


class ListCreateModelView(BaseModelView, ListMixin, CreateMixin):
    pass


class RetrieveUpdateDeleteModelView(BaseModelView, RetrieveMixin, UpdateMixin, DestroyMixin):
    pass
