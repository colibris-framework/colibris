from marshmallow import post_load
from marshmallow_peewee import ModelSchema as MMPWModelSchema
from marshmallow_peewee import schema as marshmallow_peewee_schema

from colibris.utils import camelcase_to_underscore

DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class ModelSchemaOpts(marshmallow_peewee_schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)

        if self.model:
            self.name = getattr(meta, 'name', camelcase_to_underscore(self.model.__name__))
            self.name_plural = getattr(meta, 'name_plural', self.name + 's')

        self.load_instance = getattr(meta, 'load_instance', False)

        self.datetimeformat = DEFAULT_DATETIME_FORMAT


class ModelSchema(MMPWModelSchema):
    OPTIONS_CLASS = ModelSchemaOpts

    @post_load
    def make_instance(self, data, **kwargs):
        if not self.opts.load_instance:
            return data

        return super().make_instance(data)
