
import asyncio
import inspect
import logging
import time

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger

from colibris import routes as default_routes
from colibris import settings
from colibris import utils


logger = logging.getLogger(__name__)
middleware = []
routes_by_path = {}  # indexed by path

_project_app = None
_start_time = time.time()


# webapp & middleware

def _init_webapp():
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
        gh = _project_app.get_health
        if inspect.iscoroutinefunction(gh):
            h = await gh()

        else:
            h = gh()

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

async def _build_routes_cache(app):
    # add route paths to routes cache
    for r in app.router.routes():
        path = r.resource.canonical
        routes_by_path.setdefault(path, (r.method, path, r.handler, None))


def _add_route_tuple(route):
    if len(route) < 4:
        route = route + (None,)

    method, path, handler, authorize = route

    if inspect.isclass(handler):
        try:
            webapp.router.add_view(path, handler)
        except RuntimeError:
            # view was already added because of possible duplication of views in routes
            pass
    else:
        webapp.router.add_route(method, path, handler)

    routes_by_path[path] = route


def _init_default_routes():
    for route in default_routes.ROUTES:
        _add_route_tuple(route)


def _init_project_routes():
    project_routes = utils.import_module_or_none('{}.routes'.format(settings.PROJECT_PACKAGE_NAME))
    if project_routes is None:
        return

    for _route in getattr(project_routes, 'ROUTES', []):
        _add_route_tuple(_route)


# apispec/swagger support

def _init_swagger():
    async def init_wrapper(app):
        setup_swagger(app=app, swagger_url=settings.API_DOCS_PATH, swagger_info=app['swagger_dict'])

    setup_aiohttp_apispec(app=webapp, title='API Documentation')
    webapp.on_startup.append(init_wrapper)


webapp = _init_webapp()

_init_default_routes()
_init_swagger()
_init_project_routes()

webapp.on_startup.append(_init_app)
webapp.on_startup.append(_build_routes_cache)
webapp.on_startup.append(_initial_health_check)
