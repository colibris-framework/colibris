
class APIException(Exception):
    def __init__(self, code, message, details=None,  status=400):
        self.code = code
        self.message = message
        self.details = details
        self.status = status

    def __str__(self):
        return self.code
