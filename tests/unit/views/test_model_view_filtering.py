import pytest

from colibris.middleware.errors import handle_errors_json
from colibris.schemas import ModelSchema

from colibris import persist
from colibris.views.filtering import fields, operators
from colibris.views.filtering.base import ModelFilter
from colibris.views.generic import ListCreateModelView


class Item(persist.Model):
    name = persist.CharField()
    count = persist.IntegerField()
    info = persist.TextField()


class ItemSchema(ModelSchema):
    class Meta:
        model = Item


class ExplicitFieldsFilter(ModelFilter):
    name = fields.String(field='name', operation=operators.EQ)
    name__regexp = fields.String(field='name', operation=operators.REGEXP)
    name__not = fields.String(field='name', operation=operators.NOT)
    name__ilike = fields.String(field='name', operation=operators.ILIKE)
    count__gt = fields.String(field='count', operation=operators.GT)
    count__ge = fields.String(field='count', operation=operators.GE)
    count__lt = fields.String(field='count', operation=operators.LT)
    count__le = fields.String(field='count', operation=operators.LE)

    class Meta:
        model = Item


class GeneratedFieldsFilter(ModelFilter):
    class Meta:
        model = Item
        fields = {
            'name': (operators.EQ, operators.REGEXP, operators.NOT, operators.ILIKE),
            'count': (operators.GT, operators.GE, operators.LT, operators.LE)
        }


class ExplicitFieldsFilterItemsView(ListCreateModelView):
    body_schema_class = ItemSchema
    model = Item
    filter_class = ExplicitFieldsFilter


class GeneratedFieldsFilterItemsView(ListCreateModelView):
    body_schema_class = ItemSchema
    model = Item
    filter_class = GeneratedFieldsFilter


MODELS = [Item]


def setup_db(models):
    settings = {
        'backend': 'colibris.persist.backends.SQLiteBackend',
        'database': ':memory:',
        'regexp_function': True
    }

    persist.DatabaseBackend.configure(settings)
    db = persist.get_database()
    db.connect()
    persist.models.set_database(db)
    db.create_tables(models)


def setup_module(module):
    setup_db(MODELS)

    Item.create(name='Justo', count=1, info='Ridiculus Risus')
    Item.create(name='Justo', count=2, info='Ligula Dolor')
    Item.create(name='Vestibulum', count=3, info='Justo Dolor')
    Item.create(name='Sit', count=4, info='Tortor Sollicitudin')
    Item.create(name='Porta', count=5, info='Etiam Consectetur')
    Item.create(name='Mattis', count=6, info='Parturient Vulputate')


@pytest.fixture
async def http_client(http_client_maker):
    return await http_client_maker(middlewares=[handle_errors_json],
                                   routes=[
                                       ('/some-items', ExplicitFieldsFilterItemsView),
                                       ('/same-items', GeneratedFieldsFilterItemsView), ]
                                   )


class TestFilterExplicitFields:
    @classmethod
    def setup_class(cls):
        cls.url = '/some-items'

    async def test_single_filter_eq(self, http_client):
        response = await http_client.get(self.url, params={'name': 'Justo'})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['name'] == 'Justo'
        assert data[1]['name'] == 'Justo'

    async def test_single_filter_regexp(self, http_client):
        response = await http_client.get(self.url, params={'name__regexp': '.*J.*u.*s.*t.*o.*'})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['name'] == 'Justo'
        assert data[1]['name'] == 'Justo'

    async def test_single_filter_not(self, http_client):
        response = await http_client.get(self.url, params={'name__not': 'Justo'})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 4

    async def test_single_filter_like(self, http_client):
        response = await http_client.get(self.url, params={'name__ilike': '%%sto%'})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['name'] == 'Justo'
        assert data[1]['name'] == 'Justo'

    async def test_single_filter_gt(self, http_client):
        response = await http_client.get(self.url, params={'count__gt': 3})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    async def test_single_filter_ge(self, http_client):
        response = await http_client.get(self.url, params={'count__ge': 3})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 4

    async def test_single_filter_lt(self, http_client):
        response = await http_client.get(self.url, params={'count__lt': 6})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 5

    async def test_single_filter_le(self, http_client):
        response = await http_client.get(self.url, params={'count__le': 6})
        assert response.status == 200

        data = await response.json()
        assert isinstance(data, list)
        assert len(data) == 6


class TestFilterGeneratedFields(TestFilterExplicitFields):
    @classmethod
    def setup_class(cls):
        cls.url = '/same-items'
