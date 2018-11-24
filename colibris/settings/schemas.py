
from marshmallow import Schema, fields, EXCLUDE


class EnvVarsSchema(Schema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    DATABASE = fields.String()

    class Meta:
        unknown = EXCLUDE
