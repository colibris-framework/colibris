
import logging

from aiohttp import web

from colibri import auth
from colibri import settings
from colibri import utils
from colibri import webapp


logger = logging.getLogger(__name__)

_auth_backend_settings = dict(settings.AUTHENTICATION or {})
_auth_backend_path = _auth_backend_settings.pop('backend', 'colibri.auth.null.AuthenticationBackend')
_auth_backend_class = utils.import_member(_auth_backend_path)
_auth_backend = _auth_backend_class(**_auth_backend_settings)


@web.middleware
async def handle_authentication(request, handler):
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    path = request.match_info.route.resource.canonical
    route = webapp.routes_by_path.get(path)
    if not route:  # shouldn't happen
        raise web.HTTPNotFound()

    # only go through authentication if route specifies authorization;
    # otherwise route is considered public
    if route[3] is not None:
        try:
            account = _auth_backend.authenticate(request)

        except auth.AuthException as e:
            logger.error('authentication failed: %s', e)

            raise web.HTTPUnauthorized()

        request.account = account

    return await handler(request)


@web.middleware
async def handle_errors_json(request, handler):
    try:
        return await handler(request)

    except web.HTTPException as e:
        if e.status >= 400:
            return web.json_response({'error': e.reason}, status=e.status)

        return e
