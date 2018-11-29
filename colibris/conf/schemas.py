
from marshmallow import fields
from marshmallow import Schema as MMSchema, EXCLUDE as MM_EXCLUDE


_settings_schemas = []


class SettingsSchema(MMSchema):
    class Meta:
        unknown = MM_EXCLUDE


class CommonSchema(SettingsSchema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    API_DOCS_PATH = fields.String()
    DATABASE = fields.String()


# authentication

class ModelAuthenticationSchema(SettingsSchema):
    AUTHENTICATION_MODEL = fields.String()
    AUTHENTICATION_IDENTITY_FIELD = fields.String()
    AUTHENTICATION_SECRET_FIELD = fields.String()


class JWTAuthenticationSchema(ModelAuthenticationSchema):
    AUTHENTICATION_IDENTITY_CLAIM = fields.String()


class AllAuthenticationSchema(JWTAuthenticationSchema):
    AUTHENTICATION_BACKEND = fields.String()


# authorization

class RoleAuthorizationSchema(SettingsSchema):
    AUTHORIZATION_ROLE_FIELD = fields.String()


class ModelAuthorizationSchema(SettingsSchema):
    AUTHORIZATION_MODEL = fields.String()
    AUTHORIZATION_ACCOUNT_FIELD = fields.String()


class RightsAuthorizationSchema(ModelAuthorizationSchema):
    AUTHORIZATION_RESOURCE_FIELD = fields.String()
    AUTHORIZATION_OPERATIONS_FIELD = fields.String()


class AllAuthorizationSchema(RoleAuthorizationSchema,
                             RightsAuthorizationSchema):

    AUTHORIZATION_BACKEND = fields.String()


# cache

class LocMemCacheSchema(SettingsSchema):
    CACHE_MAX_ENTRIES = fields.Integer()


class RedisCacheSchema(SettingsSchema):
    CACHE_HOST = fields.String()
    CACHE_PORT = fields.Integer()
    CACHE_DB = fields.Integer()
    CACHE_PASSWORD = fields.String()


class AllCacheSchema(LocMemCacheSchema,
                     RedisCacheSchema):

    CACHE_BACKEND = fields.String()


# database

class SQLiteDatabaseSchema(SettingsSchema):
    DATABASE_NAME = fields.String()


class ServerDatabaseSchema(SettingsSchema):
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


def register_settings_schema(schema):
    _settings_schemas.append(schema)


def get_all_settings_schema():
    return type('AllSettingsSchema', tuple(_settings_schemas), {})


# put together known schemas

register_settings_schema(CommonSchema)
register_settings_schema(AllAuthenticationSchema)
register_settings_schema(AllAuthorizationSchema)
register_settings_schema(AllCacheSchema)
register_settings_schema(AllDatabaseSchema)
