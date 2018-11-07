
class AuthenticationException(Exception):
    def __str__(self):
        message = super().__str__()
        if not message:
            message = self.__class__.__name__

        return message


class NoSuchAccount(AuthenticationException):
    pass


class IdentityVerificationFailed(AuthenticationException):
    pass
