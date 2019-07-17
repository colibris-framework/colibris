import marshmallow_peewee.schema
from marshmallow import post_dump, post_load

from colibris.api import envelope
from colibris.utils import camelcase_to_underscore

DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class ModelSchemaOpts(marshmallow_peewee.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)

        if self.model:
            self.name = getattr(meta, 'name', camelcase_to_underscore(self.model.__name__))
            self.name_plural = getattr(meta, 'name_plural', self.name + 's')

        self.load_instance = getattr(meta, 'load_instance', False)

        self.datetimeformat = DEFAULT_DATETIME_FORMAT


class ModelSchema(marshmallow_peewee.ModelSchema):
    OPTIONS_CLASS = ModelSchemaOpts

    @post_load
    def make_instance(self, data, **kwargs):
        if not self.opts.load_instance:
            return data

        return super().make_instance(data)
