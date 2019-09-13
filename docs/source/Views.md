# Views

Add your views by editing the `views.py` file:

    nano ${PACKAGE}/views.py
    
## APIView

For a simple API view, `colibris.views.APIView` can be used. Here is an example:

    class ItemsView(APIView):
        body_schema_class = ItemSchema
        query_schema_class = QuerySchema
    
        async def get(self):
            args = await self.get_validated_query()
    
            return web.json_response(args)
    
        async def post(self):
            data = await self.get_validated_body()
    
            return web.json_response(data)


Where `ItemSchema` and `QuerySchema` are simple [marshmallow](https://marshmallow.readthedocs.io/en/3.0/quickstart.html#declaring-schemas)
schemas.

## ModelView

For a model based view, there is `colibris.views.ModelView` which has to be used together with at least one of:
`ListMixin`, `CreateMixin`, `RetrieveMixin`, `UpdateMixin`, `DestroyMixin`. Here is an example of a model view 
which supports `GET` and `POST` methods:

    class ItemsView(ModelView, ListMixin, CreateMixin):
        model = Model 
        body_schema_class = ItemSchema
        query_schema_class = QuerySchema

For a basic RESTful resource there are predefined base views that can be used like this:

    class ItemsView(ListCreateModelView):
        model = Model 
        body_schema_class = ItemSchema
        
    class ItemsDetailView(RetrieveUpdateDestroyModelView):
        model = Model 
        body_schema_class = ItemSchema

### Filtering

Filtering is also supported. A filter class will be created like this:

    class ItemsFilter(ModelFilter):
        name = fields.String(field='name', operation=operators.EQ)
    
        class Meta:
            model = Item
            fields = {
                'name': (operators.EQ, operators.REGEXP, operators.NOT, operators.ILIKE),
                'count': (operators.GT, operators.GE, operators.LT, operators.LE)
            }


    class ItemsView(ListCreateModelView):
        model = Model 
        body_schema_class = ItemSchema
        filter_class = ItemsFilter  