
from marshmallow import Schema, fields, EXCLUDE


class CommonSchema(Schema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    API_DOCS_PATH = fields.String()
    DATABASE = fields.String()


# authentication

class ModelAuthenticationSchema(Schema):
    AUTHENTICATION_MODEL = fields.String()
    AUTHENTICATION_IDENTITY_FIELD = fields.String()
    AUTHENTICATION_SECRET_FIELD = fields.String()


class JWTAuthenticationSchema(ModelAuthenticationSchema):
    AUTHENTICATION_IDENTITY_CLAIM = fields.String()


class AllAuthenticationSchema(JWTAuthenticationSchema):
    AUTHENTICATION_BACKEND = fields.String()


# authorization

class RoleAuthorizationSchema(Schema):
    AUTHORIZATION_ROLE_FIELD = fields.String()


class ModelAuthorizationSchema(Schema):
    AUTHORIZATION_MODEL = fields.String()
    AUTHORIZATION_ACCOUNT_FIELD = fields.String()


class RightsAuthorizationSchema(ModelAuthorizationSchema):
    AUTHORIZATION_RESOURCE_FIELD = fields.String()
    AUTHORIZATION_OPERATIONS_FIELD = fields.String()


class AllAuthorizationSchema(RoleAuthorizationSchema,
                             RightsAuthorizationSchema):

    AUTHORIZATION_BACKEND = fields.String()


# put together all schemas

class EnvVarsSchema(CommonSchema,
                    AllAuthenticationSchema,
                    AllAuthorizationSchema):

    class Meta:
        unknown = EXCLUDE
