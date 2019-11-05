from colibris.conf.schemas import fields, SettingsSchema

from . import constants


class GeneralSettingsSchema(SettingsSchema):
    DEBUG = fields.Boolean()
    LISTEN = fields.String()
    PORT = fields.Integer()
    SECRET_KEY = fields.String()

    class Meta:
        sensible_fields = ['SECRET_KEY']


DEBUG = True

LISTEN = '0.0.0.0'
PORT = 8888

SECRET_KEY = 'replace-me-with-random-ascii-string-or-supply-via-environment'

DATABASE = {
    'backend': 'colibris.persist.SQLiteBackend',
    'name': '__packagename__.db'
}

AUTHENTICATION = {
    'backend': 'colibris.authentication.apikey.APIKeyBackend',
    'model': '__packagename__.models.User',
    'key_field': 'key',
}

AUTHORIZATION = {
    'backend': 'colibris.authorization.role.RoleBackend',
    'role_field': 'role',
    'order': constants.ROLES
}

GeneralSettingsSchema().load_from_env(target_settings=globals())
