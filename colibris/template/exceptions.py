

class TemplateException(Exception):
    pass


class TemplateNotFound(TemplateException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'template not found: {}'.format(self.name)


class TemplateSyntaxError(TemplateException):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'template syntax error: {}'.format(self.error)
