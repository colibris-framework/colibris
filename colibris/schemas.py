
import marshmallow_peewee.schema

from marshmallow import Schema as MMSchema
from marshmallow import pre_dump, post_dump, pre_load, post_load
from marshmallow import fields, validate

from colibris.api import envelope
from colibris.utils import camelcase_to_underscore


class ModelSchemaOpts(marshmallow_peewee.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)

        if self.model:
            self.name = getattr(meta, 'name', camelcase_to_underscore(self.model.__name__))
            self.name_plural = getattr(meta, 'name_plural', self.name + 's')


class ModelSchema(marshmallow_peewee.ModelSchema):
    OPTIONS_CLASS = ModelSchemaOpts

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        if many:
            return envelope.wrap_many(data)

        else:
            return envelope.wrap_one(data)


def many_envelope(schema_class):
    class SchemaWrapper(MMSchema):
        results = fields.Nested(schema_class, many=True)
        count = fields.Integer()
        pages = fields.Integer()
        page = fields.Integer()
        page_size = fields.Integer()

    return SchemaWrapper()
