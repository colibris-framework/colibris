import operator
from functools import reduce

import peewee
from marshmallow import Schema, ValidationError, EXCLUDE
from marshmallow.schema import SchemaMeta, SchemaOpts

from colibris import api, persist
from colibris.views.filtering import fields, operators

TYPE_MAPPING = {
    peewee.AutoField: fields.String,
    peewee.IntegerField: fields.Integer,
    peewee.CharField: fields.String,
    peewee.BooleanField: fields.Boolean,
    peewee.DateTimeField: fields.DateTime,
    peewee.DateField: fields.Date,
    peewee.TextField: fields.String,
    peewee.FloatField: fields.Float,
    peewee.DecimalField: fields.Decimal,
    peewee.TimeField: fields.Time,
    peewee.BigIntegerField: fields.Integer,
    peewee.SmallIntegerField: fields.Integer,
    peewee.DoubleField: fields.Float,
    peewee.FixedCharField: fields.String
}

NAME_MAPPING = {
    operators.EQ: '',
    operators.GT: '__gt',
    operators.GE: '__ge',
    operators.LT: '__lt',
    operators.LE: '__le',
    operators.NOT: '__not',
    operators.LIKE: '__like',
    operators.ILIKE: '__ilike',
    operators.REGEXP: '__regexp',
}


class ModelFilterMeta(SchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        fields_from_model = []
        model = klass.opts.model

        if model is None:
            return dict_cls(inherited_fields + cls_fields)

        model_fields = {field.name: field for field in model._meta.sorted_fields}

        for model_field, operations in klass.opts.filter_fields.items():
            for operation in operations:
                model_field_class = model_fields[model_field].__class__
                field_class = TYPE_MAPPING[model_field_class]
                field = field_class(field=model_field, operation=operation)
                field_name = model_field + NAME_MAPPING[operation]

                fields_from_model.append(
                    (field_name, field)
                )

        return dict_cls(fields_from_model + inherited_fields + cls_fields)


class ModelFilterSchemaOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.model = getattr(meta, 'model', None)
        self.filter_fields = getattr(meta, 'fields', {})
        meta.fields = ()
        super().__init__(meta, **kwargs)

        if self.model and not issubclass(self.model, persist.Model):
            raise ValueError("`model` must be a subclass of persist.Model")


class ModelFilter(Schema, metaclass=ModelFilterMeta):
    OPTIONS_CLASS = ModelFilterSchemaOpts

    class Meta(Schema.Meta):
        unknown = EXCLUDE
        model = None
        fields = ()

    def __init__(self, filter_args: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_args = filter_args

        try:
            self.validated_filter_args = self.load(self.filter_args)
        except ValidationError as err:
            raise api.SchemaError(details=err.messages)

    def filter_query(self, query):
        assert self.Meta.model is not None, 'The attribute "Meta.model" is required for {}'.format(self)

        conditions = []

        for filter_field, filter_value in self.validated_filter_args.items():
            op = self.fields[filter_field].operation
            field = self.fields[filter_field].field

            model_field = getattr(self.Meta.model, field)
            conditions.append(op(model_field, filter_value))

        if conditions:
            where = reduce(operator.and_, conditions)
            query = query.where(where)

        return query
