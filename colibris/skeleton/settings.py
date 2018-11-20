
PROJECT_PACKAGE_NAME = '__packagename__'

DEBUG = True

LISTEN = '0.0.0.0'
PORT = 8888

# DATABASE = 'postgresql://username:password@localhost:5432/__packagename__'
DATABASE = 'sqlite:////tmp/__projectname__.db'

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
