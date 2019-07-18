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

        instance = query.model.create(**data)

        result = schema.dump(instance)

        return web.json_response(result, status=201)



class UpdateMixin:
    async def patch(self):
        return await self._update(partial=True)

    async def put(self):
        return await self._update(partial=False)

    async def _update(self, partial):
        instance = self.get_object()

        schema = self.get_body_schema(partial=partial, instance=instance)
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



class RetrieveMixin:
    async def get(self):
        schema = self.get_body_schema()
        instance = self.get_object()

        result = schema.dump(instance)

        return web.json_response(result)
