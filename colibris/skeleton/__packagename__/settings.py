
from colibris.conf.schemas import fields, SettingsSchema

#
# class GeneralSettingsSchema(SettingsSchema):
#     DEBUG = fields.Boolean()
#     LISTEN = fields.String()
#     PORT = fields.Integer()
#     SECRET_KEY = fields.String()
#
#    class Meta:
#        sensible_fields = ['SECRET_KEY']
#
#
# class DatabaseSettingsSchema(SettingsSchema):
#     NAME = fields.String()
#     HOST = fields.String()
#     PORT = fields.Integer()
#     USERNAME = fields.String()
#     PASSWORD = fields.String()
#
#     class Meta:
#         prefix = 'DATABASE_'
#         sensible_field = ['PASSWORD']
#

DEBUG = True

LISTEN = '0.0.0.0'
PORT = 8888

SECRET_KEY = 'replace-me-with-random-ascii-string-or-supply-via-environment'

# DATABASE = {
#     'backend': 'colibris.persist.PostgreSQLBackend',
#     'name': '__packagename__',
#     'host': '127.0.0.1',
#     'port': 5432,
#     'username': 'username',
#     'password': 'password'
# }

# AUTHENTICATION = {
#     'backend': 'colibris.authentication.jwt.JWTBackend',
#     'model': '__packagename__.models.User',
#     'identity_claim': 'sub',
#     'identity_field': 'username',
#     'secret_field': 'password'
# }

# AUTHORIZATION = {
#     'backend': 'colibris.authorization.role.RoleBackend',
#     'role_field': 'role'
# }

#
# GeneralSettingsSchema().load_from_env(globals())
# DatabaseSettingsSchema().load_from_env(globals())
#
