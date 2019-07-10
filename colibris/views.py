import abc
import traceback
from json import JSONDecodeError

from aiohttp import web, hdrs
from aiohttp_apispec import docs
from aiohttp_apispec import response_schema, request_schema

from colibris.persist import Model
from colibris.schemas import ModelSchema
from marshmallow import ValidationError, Schema
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
        assert cls.model, 'The "model" field is required for {}.'.format(cls)

        assert issubclass(cls.model, Model) is True, 'The "model" should be a subclass of {}.'.format(Model)

        if hasattr(cls, 'get'):
            cls.get = response_schema(cls.body_schema_class)(cls.get)

        if hasattr(cls, 'post'):
            cls.post = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.post))

        if hasattr(cls, 'put'):
            cls.put = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.put))

        if hasattr(cls, 'patch'):
            cls.patch = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.patch))

        for http_method in hdrs.METH_ALL:
            method_name = http_method.lower()

            if hasattr(cls, method_name) and getattr(cls, 'query_schema_class', None) is not None:
                handler = getattr(cls, method_name)
                setattr(cls, method_name, request_schema(cls.query_schema_class, location='query')(handler))

        super().__init__(name, bases, attrs)


class ListMixin(metaclass=_GenericMixinMeta):
    model = Model
    body_schema_class = ModelSchema

    async def get(self):
        items = self.get_query()
        schema = self.get_body_schema_class(many=True)
        result = schema.dump(list(items))

        return web.json_response(result)


class CreateMixin(metaclass=_GenericMixinMeta):
    model = Model
    body_schema_class = ModelSchema

    async def post(self):
        schema = self.get_body_schema_class()
        data = await self.get_validated_body(schema)
        print(data)
        try:
            item = self.model.create(**data)
        except IntegrityError as err:
            traceback.print_exc()
            raise api.ServerError(code='server_error', message=str(err))

        result = schema.dump(item)

        return web.json_response(result, status=201)


class RetrieveMixin(metaclass=_GenericMixinMeta):
    model = Model
    body_schema_class = ModelSchema

    async def get(self):
        schema = self.get_body_schema_class()
        instance = self.get_object()

        result = schema.dump(instance)

        return web.json_response(result)


class UpdateMixin(metaclass=_GenericMixinMeta):
    model = Model
    body_schema_class = ModelSchema

    async def patch(self):
        schema = self.get_body_schema_class(partial=True)
        data = await self.get_validated_body(schema)

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
        schema = self.get_body_schema_class()
        data = await self.get_validated_body(schema)

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


class APIView(web.View):
    body_schema_class = Schema
    query_schema_class = None

    def get_body_schema_class(self, *args, **kwargs):
        kwargs.update({
            'context': {'request': self.request}
        })

        schema = self.body_schema_class(*args, **kwargs)

        return schema

    def get_query_schema_class(self, *args, **kwargs):
        if self.query_schema_class is None:
            return None

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

        assert schema is not None, 'The attribute "query_schema_class" is required for {}'.format(self)

        query = await self.get_request_query()

        try:
            data = schema.load(query)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

        return data

    async def get_request_query(self):
        return self.request.query


class ModelView(APIView):
    model = Model
    body_schema_class = ModelSchema
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


class ListCreateModelView(ModelView, ListMixin, CreateMixin):
    pass


class RetrieveUpdateDeleteModelView(ModelView, RetrieveMixin, UpdateMixin, DestroyMixin):
    pass
