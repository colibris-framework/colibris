from marshmallow import fields


class FilterMixin:
    def __init__(self, field, operation, *args, **kwargs):
        self.field = field
        self.operation = operation

        super().__init__(*args, **kwargs)


class String(FilterMixin, fields.String):
    pass


class Integer(FilterMixin, fields.Integer):
    pass


class List(FilterMixin, fields.List):
    pass


class Boolean(FilterMixin, fields.Boolean):
    pass


class DateTime(FilterMixin, fields.DateTime):
    pass


class Date(FilterMixin, fields.Date):
    pass


class Time(FilterMixin, fields.Time):
    pass


class Float(FilterMixin, fields.Float):
    pass


class Decimal(FilterMixin, fields.Decimal):
    pass
