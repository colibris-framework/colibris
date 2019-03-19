
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import TemplateNotFound, TemplateSyntaxError, TemplateError
from jinja2 import select_autoescape

from colibris.template import exceptions
from colibris.template import base


class JinjaBackend(base.TemplateBackend):
    def __init__(self, paths):
        super().__init__(paths)

        self.loader = FileSystemLoader(paths)
        self.env = Environment(loader=self.loader, autoescape=select_autoescape())

    def render(self, template_name, context):
        try:
            template = self.env.get_template(template_name)
            return template.render(context)

        except TemplateNotFound:
            raise exceptions.TemplateNotFound(template_name)

        except TemplateSyntaxError as e:
            raise exceptions.TemplateSyntaxError(str(e))

        except TemplateError as e:
            raise exceptions.TemplateException(str(e))

    def render_string(self, template_str, context):
        try:
            template = self.env.from_string(template_str)
            return template.render(context)

        except TemplateSyntaxError as e:
            raise exceptions.TemplateSyntaxError(str(e))

        except TemplateError as e:
            raise exceptions.TemplateException(str(e))
