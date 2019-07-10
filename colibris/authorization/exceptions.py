

class AuthorizationException(Exception):
    pass


class PermissionNotMet(AuthorizationException):
    def __init__(self, permission):
        super().__init__('permission not met: {}'.format(permission))

        self.permission = permission
