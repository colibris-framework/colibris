
class APIException(Exception):
    def __init__(self, code, message, details=None,  status=400):
        self.code = code
        self.message = message
        self.details = details
        self.status = status

    def __str__(self):
        return self.code


class NotFoundException(APIException):
    def __init__(self, model):
        super().__init__('not_found',
                         'The requested {} cannot be found.'.format(model._meta.name),
                         status=404)
