
import asyncio
import inspect
import logging
import time

from aiohttp import web, hdrs
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger

from colibris import routes as default_routes
from colibris import utils
from colibris.conf import settings


logger = logging.getLogger(__name__)
middleware = []
route_auth_mapping = {}

_web_app = None
_project_app = None
_start_time = time.time()


# web app & middleware

def _make_web_app():
    for path in settings.MIDDLEWARE:
        middleware.append(utils.import_member(path))

    return web.Application(middlewares=middleware, client_max_size=settings.MAX_REQUEST_BODY_SIZE)


# app

class HealthException(Exception):
    pass


async def _init_app(app):
    global _project_app

    _project_app = utils.import_module_or_none('{}.app'.format(settings.PROJECT_PACKAGE_NAME))
    if _project_app is not None:
        init = getattr(_project_app, 'init', None)
        if init:
            init(app, asyncio.get_event_loop())


async def get_health():
    if hasattr(_project_app, 'get_health'):
        h = _project_app.get_health()
        if inspect.isawaitable(h):
            h = await h

        return h

    return {
        'uptime': int(time.time() - _start_time)
    }


async def _initial_health_check(app):
    try:
        await get_health()

    except Exception as e:
        logger.critical('initial health check problem: %s', e)
        raise


# routes

def _add_route_tuple(web_app, route):
    while len(route) < 4:
        route = route + (None,)

    method, path, handler, authorize = route

    if inspect.isclass(handler):  # class-based view
        method = hdrs.METH_ANY

    # aiohttp reuses the last resource if and only if two successive routes are the same,
    # which is kind of random.

    # Explicitly add resource instead of using add_route(),
    # since we want to prevent reusing the last resource.

    resource = web_app.router.add_resource(path)
    resource_route = resource.add_route(method, handler)

    route_auth_mapping[resource_route] = authorize


def _add_static_route_tuple(web_app, route):
    fs_path, prefix = route

    web_app.router.add_static(prefix, fs_path)


def _init_default_routes(web_app):
    for route in default_routes.ROUTES:
        _add_route_tuple(web_app, route)

    for route in default_routes.STATIC_ROUTES:
        _add_static_route_tuple(web_app, route)


def _init_project_routes(web_app):
    project_routes = utils.import_module_or_none('{}.routes'.format(settings.PROJECT_PACKAGE_NAME))
    if project_routes is None:
        return

    for _route in getattr(project_routes, 'ROUTES', []):
        _add_route_tuple(web_app, _route)

    for _route in getattr(project_routes, 'STATIC_ROUTES', []):
        _add_static_route_tuple(web_app, _route)


# apispec/swagger support

def _init_swagger(web_app):
    async def init_wrapper(app):
        setup_swagger(app=app, swagger_url=settings.API_DOCS_PATH, swagger_info=app['swagger_dict'])

    setup_aiohttp_apispec(app=web_app, title='API Documentation')
    web_app.on_startup.append(init_wrapper)


def get_web_app(force_create=False):
    global _web_app

    if _web_app is None or force_create:
        _web_app = _make_web_app()

        _init_project_routes(_web_app)
        _init_default_routes(_web_app)
        _init_swagger(_web_app)

        _web_app.on_startup.append(_init_app)
        _web_app.on_startup.append(_initial_health_check)

    return _web_app
