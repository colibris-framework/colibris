from colibris import api
from colibris.views.api import APIView


class ModelView(APIView):
    model = None
    pagination_class = None
    url_identifier = 'id'
    lookup_field = 'id'

    def get_query(self):
        assert self.model is not None, 'The attribute "model" is required for {}'.format(self)

        return self.model.select().order_by(self.model.id.desc())

    def get_object(self):
        identifier_value = self.request.match_info[self.url_identifier]
        query = self.get_query()
        model = query.model

        try:
            instance = query.where(getattr(model, self.lookup_field) == identifier_value).get()

        except query.model.DoesNotExist:
            raise api.ModelNotFoundException(model)

        return instance
