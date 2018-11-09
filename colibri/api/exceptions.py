
class APIException(Exception):
    pass


class BaseJSONException(APIException):
    def __init__(self, code, message, status, details=None):
        self.code = code
        self.message = message
        self.details = details
        self.status = status

    def __str__(self):
        return self.code


class DuplicateException(APIException):
    def __init__(self, model, field):
        super().__init__('duplicate_{}'.format(field),
                         'A {} with this {} already exists.'.format(model._meta.name, field),
                         status=400)


class NotFoundException(APIException):
    def __init__(self, model):
        super().__init__('not_found',
                         'The requested {} cannot be found.'.format(model._meta.name),
                         status=404)
