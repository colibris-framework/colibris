
from marshmallow import pre_dump, post_dump, pre_load, post_load, validates_schema
from marshmallow import fields, validate
from marshmallow import ValidationError
from marshmallow import EXCLUDE as MM_EXCLUDE
from marshmallow.schema import Schema as MMSchema, SchemaMeta as MMSchemaMeta, SchemaOpts as MMSchemaOpts


_settings_schemas = []


class ColonSeparatedStringsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''

        return ':'.join(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        return value.split(':')


class SettingsSchemaOpts(MMSchemaOpts):
    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)

        self.unknown = getattr(meta, 'unknown', MM_EXCLUDE)  # Ignore other env variables, by default
        self.prefix = getattr(meta, 'prefix', '')


class SettingsSchemaMeta(MMSchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        prefix = klass.opts.prefix
        cls_fields = [(prefix + n, v) for n, v in cls_fields]
        inherited_fields = [(prefix + n, v) for n, v in inherited_fields]

        return MMSchemaMeta.get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)


class SettingsSchema(MMSchema, metaclass=SettingsSchemaMeta):
    OPTIONS_CLASS = SettingsSchemaOpts


class CommonSchema(SettingsSchema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    MAX_REQUEST_BODY_SIZE = fields.Integer()
    API_DOCS_PATH = fields.String()
    SECRET_KEY = fields.String()


# authentication

class ModelAuthenticationSchema(SettingsSchema):
    MODEL = fields.String()
    IDENTITY_FIELD = fields.String()
    SECRET_FIELD = fields.String()


class CookieAuthenticationSchema(SettingsSchema):
    COOKIE_NAME = fields.String()
    COOKIE_DOMAIN = fields.String()
    VALIDITY_SECONDS = fields.Number()


class JWTAuthenticationSchema(ModelAuthenticationSchema, CookieAuthenticationSchema):
    IDENTITY_CLAIM = fields.String()


class AllAuthenticationSchema(JWTAuthenticationSchema):
    BACKEND = fields.String()

    class Meta:
        prefix = 'AUTHENTICATION_'


# authorization

class RoleAuthorizationSchema(SettingsSchema):
    ROLE_FIELD = fields.String()


class ModelAuthorizationSchema(SettingsSchema):
    MODEL = fields.String()
    ACCOUNT_FIELD = fields.String()


class RightsAuthorizationSchema(ModelAuthorizationSchema):
    RESOURCE_FIELD = fields.String()
    OPERATIONS_FIELD = fields.String()


class AllAuthorizationSchema(RoleAuthorizationSchema,
                             RightsAuthorizationSchema):

    BACKEND = fields.String()

    class Meta:
        prefix = 'AUTHORIZATION_'


# cache

class LocMemCacheSchema(SettingsSchema):
    MAX_ENTRIES = fields.Integer()


class RedisCacheSchema(SettingsSchema):
    HOST = fields.String()
    PORT = fields.Integer()
    DB = fields.Integer()
    PASSWORD = fields.String()


class AllCacheSchema(LocMemCacheSchema,
                     RedisCacheSchema):

    BACKEND = fields.String()

    class Meta:
        prefix = 'CACHE_'


# database

class SQLiteDatabaseSchema(SettingsSchema):
    NAME = fields.String()


class ServerDatabaseSchema(SettingsSchema):
    NAME = fields.String()
    HOST = fields.String()
    PORT = fields.Integer()
    USERNAME = fields.String()
    PASSWORD = fields.String()


class MySQLDatabaseSchema(ServerDatabaseSchema):
    pass


class PostgreSQLDatabaseSchema(ServerDatabaseSchema):
    pass


class AllDatabaseSchema(SQLiteDatabaseSchema,
                        MySQLDatabaseSchema,
                        PostgreSQLDatabaseSchema):

    BACKEND = fields.String()

    class Meta:
        prefix = 'DATABASE_'


# template

class Jinja2TemplateSchema(SettingsSchema):
    EXTENSIONS = ColonSeparatedStringsField()
    TRANSLATIONS = fields.String()


class AllTemplateSchema(Jinja2TemplateSchema):
    BACKEND = fields.String()
    PATHS = ColonSeparatedStringsField()

    class Meta:
        prefix = 'TEMPLATE_'


# task queue

class RQTaskQueueSchema(SettingsSchema):
    HOST = fields.String()
    PORT = fields.Integer()
    DB = fields.Integer()
    PASSWORD = fields.String()
    POLL_RESULTS_INTERVAL = fields.Integer()


class AllTaskQueueSchema(RQTaskQueueSchema):
    BACKEND = fields.String()

    class Meta:
        prefix = 'TASK_QUEUE_'


# email

class SMTPEmailSchema(SettingsSchema):
    HOST = fields.String()
    PORT = fields.Integer()
    USERNAME = fields.String()
    PASSWORD = fields.String()
    USE_TLS = fields.Boolean()
    TIMEOUT = fields.Integer()


class AllEmailSchema(SMTPEmailSchema):
    BACKEND = fields.String()

    class Meta:
        prefix = 'EMAIL_'


def register_settings_schema(schema):
    _settings_schemas.append(schema)


def get_all_settings_schema():
    meta = type('Meta', (), {})
    return type('AllSettingsSchema', tuple(_settings_schemas), {'Meta': meta})


# put together known schemas

register_settings_schema(CommonSchema)
register_settings_schema(AllAuthenticationSchema)
register_settings_schema(AllAuthorizationSchema)
register_settings_schema(AllCacheSchema)
register_settings_schema(AllDatabaseSchema)
register_settings_schema(AllTemplateSchema)
register_settings_schema(AllTaskQueueSchema)
register_settings_schema(AllEmailSchema)
