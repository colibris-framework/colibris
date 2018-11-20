
from colibris.utils import ClassNameException


class AuthenticationException(ClassNameException):
    pass


class NoSuchAccount(AuthenticationException):
    pass


class IdentityVerificationFailed(AuthenticationException):
    pass
