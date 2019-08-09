from marshmallow import fields


class FilterMixin:
    def __init__(self, operation, field=None, *args, **kwargs):
        self.operation = operation
        self.field = field

        super().__init__(*args, **kwargs)


class String(FilterMixin, fields.String):
    pass


class Integer(FilterMixin, fields.Integer):
    pass


class List(FilterMixin, fields.List):
    pass
