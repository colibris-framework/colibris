from colibris import api
from colibris.views.api import APIView


class ModelView(APIView):
    model = None
    pagination_class = None
    url_identifier = 'id'
    lookup_field = 'id'

    async def get_object(self):
        identifier_value = self.request.match_info[self.url_identifier]
        query = self.get_query()
        model = query.model

        try:
            instance = query.where(getattr(model, self.lookup_field) == identifier_value).get()
        except query.model.DoesNotExist:
            raise api.ModelNotFoundException(model)

        return instance

    def get_query(self):
        model = self.get_model()

        return model.select().order_by(model.id.desc())

    def get_model(self):
        assert self.model is not None, 'The attribute "model" is required for {}'.format(self)

        return self.model
