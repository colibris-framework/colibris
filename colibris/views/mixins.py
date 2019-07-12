import abc

from aiohttp import hdrs, web
from aiohttp_apispec import response_schema, request_schema

from colibris.persist import Model


class _GenericMixinMeta(abc.ABCMeta):
    def __init__(cls, name, bases, attrs):
        if getattr(cls, 'model', None) is not None:
            assert issubclass(cls.model, Model) is True, 'The "model" should be a subclass of {}.'.format(Model)

        if getattr(cls, 'body_schema_class', None) is not None:
            if hasattr(cls, 'get'):
                cls.get = response_schema(cls.body_schema_class)(cls.get)

            if hasattr(cls, 'post'):
                cls.post = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.post))

            if hasattr(cls, 'put'):
                cls.put = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.put))

            if hasattr(cls, 'patch'):
                cls.patch = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.patch))

        if getattr(cls, 'query_schema_class', None) is not None:
            for http_method in hdrs.METH_ALL:
                method_name = http_method.lower()

                if hasattr(cls, method_name):
                    handler = getattr(cls, method_name)
                    setattr(cls, method_name, request_schema(cls.query_schema_class, location='query')(handler))

        super().__init__(name, bases, attrs)


class ListMixin(metaclass=_GenericMixinMeta):
    async def get(self):
        items = self.get_query()
        schema = self.get_body_schema_class(many=True)
        result = schema.dump(list(items))

        return web.json_response(result)


class CreateMixin(metaclass=_GenericMixinMeta):
    async def post(self):
        query = self.get_query()
        schema = self.get_body_schema_class()
        data = await self.get_validated_body(schema)

        instance = query.model.create(**data)

        result = schema.dump(instance)

        return web.json_response(result, status=201)


class UpdateMixin(metaclass=_GenericMixinMeta):
    async def patch(self):
        return await self._update(partial=True)

    async def put(self):
        return await self._update(partial=False)

    async def _update(self, partial):
        instance = self.get_object()

        schema = self.get_body_schema_class(partial=partial, instance=instance)
        data = await self.get_validated_body(schema)

        instance.update_fields(data)
        instance.save(only=data.keys())

        result = schema.dump(instance)

        return web.json_response(result)


class DestroyMixin:
    async def delete(self):
        instance = self.get_object()
        instance.delete_instance()

        return web.json_response(status=204)


class RetrieveMixin(metaclass=_GenericMixinMeta):
    async def get(self):
        schema = self.get_body_schema_class()
        instance = self.get_object()

        result = schema.dump(instance)

        return web.json_response(result)
