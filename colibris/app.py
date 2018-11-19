
import asyncio
import importlib

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger

from colibris import routes as default_routes
from colibris import settings
from colibris import utils


middleware = []
routes_by_path = {}  # indexed by path


# app middleware

for _path in settings.MIDDLEWARE:
    middleware.append(utils.import_member(_path))

app = web.Application(middlewares=middleware)


# routes

def add_route_tuple(route):
    if len(route) < 4:
        route = route + (None,)

    method, path, handler, authorize = route

    app.router.add_route(method, path, handler)
    routes_by_path[path] = route


async def build_routes_cache(app):
    # add missing route paths to routes cache
    for r in app.router.routes():
        path = r.resource.canonical
        routes_by_path.setdefault(path, (r.method, path, r.handler, None))


for _route in default_routes.ROUTES:
    add_route_tuple(_route)


# apispec/swagger support

async def init_swagger(app):
    setup_swagger(app=app, swagger_url=settings.API_DOCS_PATH, swagger_info=app['swagger_dict'])

setup_aiohttp_apispec(app=app, title='API Documentation')
app.on_startup.append(init_swagger)


# project-specific routes

try:
    _project_routes = importlib.import_module('{}.routes'.format(settings.PROJECT_PACKAGE_NAME))

except ImportError:
    _project_routes = None

if _project_routes:
    for _route in getattr(_project_routes, 'ROUTES', []):
        add_route_tuple(_route)

app.on_startup.append(build_routes_cache)


# app initialization

def _init_app(app):
    try:
        _project_app = importlib.import_module('{}.app'.format(settings.PROJECT_PACKAGE_NAME))

    except ImportError:
        _project_app = None

    if _project_app:
        init = getattr(_project_app, 'init', None)
        if init:
            init(app, asyncio.get_running_loop())


app.on_startup.append(_init_app)
