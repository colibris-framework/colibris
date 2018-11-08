
import marshmallow_peewee.schema

from marshmallow import Schema
from marshmallow import fields, validate
from marshmallow import pre_load, post_load, pre_dump, post_dump

from colibri import envelope
from colibri.utils import camelcase_to_underscore


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
