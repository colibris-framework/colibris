
import logging

from aiohttp import web

from colibri import authentication
from colibri import settings
from colibri import utils
from colibri import webapp


logger = logging.getLogger(__name__)

_auth_backend_settings = dict(settings.AUTHENTICATION or {})
_auth_backend_path = _auth_backend_settings.pop('backend', 'colibri.authentication.NullBackend')
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

    method, path, _handler, authorize = route

    # only go through authentication if route specifies authorization;
    # otherwise route is considered public
    if authorize:
        try:
            account = _auth_backend.authenticate(request)

        except authentication.AuthenticationException as e:
            logger.error('%s %s authentication failed: %s', method, path, e)

            raise web.HTTPUnauthorized()

        # at this point we can safely associate request with account
        request.account = account

        if not authorize(account, method, path):
            logger.error('%s %s forbidden for %s', method, path, account)

            raise web.HTTPForbidden()

    return await handler(request)


@web.middleware
async def handle_errors_json(request, handler):
    try:
        return await handler(request)

    except web.HTTPException as e:
        if e.status >= 400:
            return web.json_response({'error': e.reason}, status=e.status)

        return e
