
from colibris.conf.backends import BackendMixin


class TemplateBackend(BackendMixin):
    def __init__(self, paths):
        self.paths = paths

    def render(self, template_name, context):
        raise NotImplementedError

    def render_string(self, template_str, context):
        raise NotImplementedError
