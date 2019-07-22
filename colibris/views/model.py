import operator
from functools import reduce

from marshmallow import Schema, ValidationError

from colibris import api
from colibris.views.api import APIView


class ModelView(APIView):
    model = None
    pagination_class = None
    filter_class = None
    url_identifier = 'id'
    lookup_field = 'id'

    def get_query(self):
        assert self.model is not None, 'The attribute "model" is required for {}'.format(self)

        conditions = []
        query = self.model.select().order_by(self.model.id.desc())
        if self.filter_class is not None:
            filter_schema: Schema = self.filter_class()

            try:
                filter_items = filter_schema.load(self.request.query)
            except ValidationError as err:
                raise api.SchemaError(details=err.messages)

            for field, value in filter_items.items():
                model_field = getattr(self.model, field)
                conditions.append(model_field == value)

            if conditions:
                where = reduce(operator.and_, conditions)
                query = query.where(where)

        return query

    def get_object(self):
        identifier_value = self.request.match_info[self.url_identifier]
        query = self.get_query()
        model = query.model

        try:
            instance = query.where(getattr(model, self.lookup_field) == identifier_value).get()
        except query.model.DoesNotExist:
            raise api.ModelNotFoundException(model)

        return instance
