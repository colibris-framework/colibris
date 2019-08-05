# Templates

The templates mechanism is configured via the `TEMPLATE` variable in `${PACKAGE}/settings.py`. Templates are disabled by
default.

## Search Paths

The template files should live in a folder called `templates`, in your project's package directory. If you want them
to be searched for in other folders, just add those paths to the `paths` template setting.

## Basic Usage

To use the templating mechanism, just import it wherever you need it:

    from colibris import template
    
To render a template file, simply call the `render` function and specify context as keyword arguments:

    result = template.render('my_template.txt', var1='value1', var2=16)

To render a template from a string, call the `render_string` function:

    result = template.render_string('Variable var1 is {{ var1 }} and var2 is {{ var2 }}.', var1='value1', var2=16)

## Rendering HTML

The following example will render an HTML template file from a view:

    from colibris.shortcuts import html_response_template    

    def index(request):
        return html_response_template('index.html', var1='value1')

## Jinja2 Backend

Make sure to have the `jinja2` python package installed.

In `${PACKAGE}/settings.py`, set:

    TEMPLATE = {
        'backend': 'colibris.template.jinja2.Jinja2Backend',
        'extensions': [...],
        'translations': 'gettext'
    }

Field `extensions` is optional and represents a list of extensions to be used by the Jinja2 environment.

Field `translations` is optional and, if present, will enable `gettext`-based Jinja2 translations. Its value is the path
to a python object that implements the `gettext` functions (such as the standard library `gettext`).
