

class TemplateException(Exception):
    pass


class TemplateNotConfigured(Exception):
    def __init__(self):
        super().__init__('template mechanism has not been configured')


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
