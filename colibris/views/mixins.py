import inspect

from aiohttp import web


class ListMixin:
    async def get(self):
        query = self.get_query()
        schema = self.get_body_schema(many=True)

        if self.pagination_class is not None:
            return await self._get_paginated_response(query, schema)

        data = schema.dump(list(query))

        return web.json_response(data)

    async def _get_paginated_response(self, query, schema):
        paginator = self.pagination_class(query, self.request)
        paginated_query = paginator.paginate_query()
        data = schema.dump(list(paginated_query))
        paginated_data = paginator.get_enveloped_data(data)

        return web.json_response(paginated_data)


class CreateMixin:
    async def post(self):
        schema = self.get_body_schema()
        data = await self.get_validated_body(schema)

        result = self.perform_create(data)
        if inspect.isawaitable(result):
            instance = await result
        else:
            instance = result

        data = schema.dump(instance)

        return web.json_response(data, status=201)

    def perform_create(self, data):
        query = self.get_query()
        instance = query.model.create(**data)

        return instance


class RetrieveMixin:
    async def get(self):
        schema = self.get_body_schema()
        instance = self.get_object()

        data = schema.dump(instance)

        return web.json_response(data)


class UpdateMixin:
    async def patch(self):
        return await self.update(partial=True)

    async def put(self):
        return await self.update(partial=False)

    async def update(self, partial):
        instance = self.get_object()

        schema = self.get_body_schema(partial=partial, instance=instance)
        data = await self.get_validated_body(schema)

        result = self.perform_update(data, instance)
        if inspect.isawaitable(result):
            instance = await result
        else:
            instance = result

        data = schema.dump(instance)

        return web.json_response(data)

    def perform_update(self, data, instance):
        instance.update_fields(data)
        instance.save(only=data.keys())

        return instance


class DestroyMixin:
    async def delete(self):
        instance = self.get_object()

        result = self.perform_destroy(instance)
        if inspect.isawaitable(result):
            await result

        return web.json_response(status=204)

    def perform_destroy(self, instance):
        instance.delete_instance()

        return None
