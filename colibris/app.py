import asyncio
import inspect
import logging
import time

from aiohttp import web, hdrs
from aiohttp_apispec import setup_aiohttp_apispec

from colibris import utils
from colibris.conf import settings

logger = logging.getLogger(__name__)
middleware = []

_web_app = None
_project_app = None
_start_time = time.time()


class HealthException(Exception):
    pass


# Web App & Middleware

def _make_web_app():
    for path in settings.MIDDLEWARE:
        middleware.append(utils.import_member(path))

    return web.Application(middlewares=middleware, client_max_size=settings.MAX_REQUEST_BODY_SIZE)


async def _init_app(app):
    global _project_app

    _project_app = utils.import_module_or_none('{}.app'.format(settings.PROJECT_PACKAGE_NAME))
    if _project_app is not None:
        init = getattr(_project_app, 'init', None)
        if init:
            init(app, asyncio.get_event_loop())


# Health

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


# Routes

def _add_route_tuple(web_app, route):
    path, handler = route

    # aiohttp reuses the last resource if and only if two successive routes are the same,
    # which is kind of random.

    # Explicitly add resource instead of using add_route(),
    # since we want to prevent reusing the last resource.

    resource = web_app.router.add_resource(path)
    resource.add_route(hdrs.METH_ANY, handler)


def _add_static_route_tuple(web_app, route):
    fs_path, prefix = route

    web_app.router.add_static(prefix, fs_path)


def _init_routes(web_app):
    routes = utils.import_module_or_none('{}.routes'.format(settings.PROJECT_PACKAGE_NAME))
    if routes is None:
        return

    for route in getattr(routes, 'ROUTES', []):
        _add_route_tuple(web_app, route)

    for route in getattr(routes, 'STATIC_ROUTES', []):
        _add_static_route_tuple(web_app, route)


# API Docs support

def _init_docs(web_app):
    from colibris.docs.openapi.setup import setup_openapi_ui

    setup_openapi_ui(app=web_app)
    setup_aiohttp_apispec(app=web_app, title='API Documentation')


def get_web_app(force_create=False):
    global _web_app

    if _web_app is None or force_create:
        _web_app = _make_web_app()

        _init_routes(_web_app)
        _init_docs(_web_app)

        _web_app.on_startup.append(_init_app)
        _web_app.on_startup.append(_initial_health_check)

    return _web_app
