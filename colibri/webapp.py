
import importlib

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger

from colibri import routes
from colibri import settings
from colibri import views


# load & prepare app middleware

middleware = []

for _path in settings.MIDDLEWARE:
    _m = importlib.import_module('.'.join(_path.split('.')[:-1]))
    _mw = getattr(_m, _path.split('.')[-1])
    middleware.append(_mw)

app = web.Application(middlewares=middleware)


# common routes

for _method, _path, _handler_name in routes.ROUTES:
    _handler = getattr(views, _handler_name)
    app.router.add_route(_method, _path, _handler)


# add apispec/swagger support

async def init_swagger(app):
    setup_swagger(app=app, swagger_url=settings.API_DOCS_PATH, swagger_info=app['swagger_dict'])

setup_aiohttp_apispec(app=app, title='API Documentation')
app.on_startup.append(init_swagger)


# add project-specific routes & views

try:
    _project_routes_module = importlib.import_module('{}.routes'.format(settings.PROJECT_PACKAGE_NAME))

except ImportError:
    _project_routes_module = None

try:
    _project_views_module = importlib.import_module('{}.views'.format(settings.PROJECT_PACKAGE_NAME))

except ImportError:
    _project_views_module = None

if _project_views_module and _project_routes_module:
    for _method, _path, _handler_name in getattr(_project_routes_module, 'ROUTES', []):
        _handler = getattr(_project_views_module, _handler_name)
        app.router.add_route(_method, _path, _handler)
