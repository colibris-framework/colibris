from aiohttp import web


class ListMixin:
    async def get(self):
        query = self.get_query()
        schema = self.get_body_schema(many=True)

        if self.pagination_class is not None:
            return await self._get_paginated_response(query, schema)

        result = schema.dump(list(query))

        return web.json_response(result)

    async def _get_paginated_response(self, query, schema):
        paginator = self.pagination_class(query, self.request)
        paginated_query = paginator.paginate_query()
        result = schema.dump(list(paginated_query))
        paginated_result = paginator.get_enveloped_data(result)

        return web.json_response(paginated_result)


class CreateMixin:
    async def post(self):
        schema = self.get_body_schema()
        data = await self.get_validated_body(schema)

        instance = self.perform_create(data)

        result = schema.dump(instance)

        return web.json_response(result, status=201)

    def perform_create(self, data):
        query = self.get_query()
        instance = query.model.create(**data)

        return instance


class UpdateMixin:
    async def patch(self):
        return await self.update(partial=True)

    async def put(self):
        return await self.update(partial=False)

    async def update(self, partial):
        instance = self.get_object()

        schema = self.get_body_schema(partial=partial, instance=instance)
        data = await self.get_validated_body(schema)

        self.perform_update(data, instance)

        result = schema.dump(instance)

        return web.json_response(result)

    def perform_update(self, data, instance):
        instance.update_fields(data)
        instance.save(only=data.keys())

        return instance


class DestroyMixin:
    async def delete(self):
        instance = self.get_object()
        self.perform_destroy(instance)

        return web.json_response(status=204)

    def perform_destroy(self, instance):
        instance.delete_instance()


class RetrieveMixin:
    async def get(self):
        schema = self.get_body_schema()
        instance = self.get_object()

        result = schema.dump(instance)

        return web.json_response(result)
