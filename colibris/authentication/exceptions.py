

class AuthenticationException(Exception):
    pass


class NoSuchAccount(AuthenticationException):
    def __init__(self):
        super().__init__('no such account')


class IdentityVerificationFailed(AuthenticationException):
    def __init__(self):
        super().__init__('identity verification failed')
