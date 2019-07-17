import math

from colibris.api.envelope import wrap_many
from marshmallow.validate import Range

from colibris import api
from colibris.schemas import fields, Schema, ValidationError

page_validator = Range(min=1, error='Value must be greater than 0.')


class PageNumberPagination:
    PAGE_SIZE = 25
    PAGE_SIZE_QUERY_PARAM = 'page_size'
    PAGE_QUERY_PARAM = 'page'

    _query_schema = type('PaginationQuerySchema', (Schema,), {
        PAGE_SIZE_QUERY_PARAM: fields.Integer(missing=PAGE_SIZE, validate=page_validator),
        PAGE_QUERY_PARAM: fields.Integer(missing=1, validate=page_validator)
    })()

    def __init__(self, query, request):
        self.query = query
        self.request = request

        try:
            query_params = self._query_schema.load(self.request.query)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

        self.page = query_params[self.PAGE_QUERY_PARAM]
        self.page_size = query_params[self.PAGE_SIZE_QUERY_PARAM]

    def paginate_query(self):
        return self.query.paginate(self.page, self.page_size)

    def get_enveloped_data(self, data):
        count = self.query.count()
        pages = math.ceil(count / self.page_size)

        return wrap_many(
            objs=data,
            count=count,
            page=self.page,
            pages=pages,
            page_size=self.page_size
        )
