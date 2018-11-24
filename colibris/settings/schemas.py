
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


# cache

class LocMemCacheSchema(Schema):
    CACHE_MAX_ENTRIES = fields.Integer()


class RedisCacheSchema(Schema):
    CACHE_HOST = fields.String()
    CACHE_PORT = fields.Integer()
    CACHE_DB = fields.Integer()
    CACHE_PASSWORD = fields.String()


class AllCacheSchema(LocMemCacheSchema,
                     RedisCacheSchema):

    CACHE_BACKEND = fields.String()


# database

class SQLiteDatabaseSchema(Schema):
    DATABASE_NAME = fields.String()


class ServerDatabaseSchema(Schema):
    DATABASE_NAME = fields.String()
    DATABASE_HOST = fields.String()
    DATABASE_PORT = fields.Integer()
    DATABASE_USERNAME = fields.String()
    DATABASE_PASSWORD = fields.String()


class MySQLDatabaseSchema(ServerDatabaseSchema):
    pass


class PostgreSQLDatabaseSchema(ServerDatabaseSchema):
    pass


class AllDatabaseSchema(SQLiteDatabaseSchema,
                        MySQLDatabaseSchema,
                        PostgreSQLDatabaseSchema):

    DATABASE_BACKEND = fields.String()


# put together all schemas

class EnvVarsSchema(CommonSchema,
                    AllAuthenticationSchema,
                    AllAuthorizationSchema,
                    AllCacheSchema):

    class Meta:
        unknown = EXCLUDE
