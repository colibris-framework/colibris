
import logging

from aiohttp import web

from colibri import settings
from colibri import utils
from colibri import webapp

from colibri.authentication import exceptions as authentication_exceptions


logger = logging.getLogger(__name__)

_authentication_backend_settings = dict(settings.AUTHENTICATION or {})
_authentication_backend_path = _authentication_backend_settings.pop('backend',
                                                                    'colibri.authentication.base.NullBackend')
_authentication_backend_class = utils.import_member(_authentication_backend_path)
_authentication_backend = _authentication_backend_class(**_authentication_backend_settings)

_authorization_backend_settings = dict(settings.AUTHORIZATION or {})
_authorization_backend_path = _authorization_backend_settings.pop('backend', 'colibri.authorization.NullBackend')
_authorization_backend_class = utils.import_member(_authorization_backend_path)
_authorization_backend = _authorization_backend_class(**_authorization_backend_settings)


@web.middleware
async def handle_auth(request, handler):
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    path = request.match_info.route.resource.canonical
    route = webapp.routes_by_path.get(path)
    if not route:  # shouldn't happen
        raise web.HTTPNotFound()

    method, path, _handler, permissions = route

    # only go through authentication if route specifies permissions;
    # otherwise route is considered public
    if permissions:
        try:
            account = _authentication_backend.authenticate(request)

        except authentication_exceptions.AuthenticationException as e:
            logger.error('%s %s authentication failed: %s', method, path, e)

            raise web.HTTPUnauthorized()

        # at this point we can safely associate request with account
        request.account = account

        if not _authorization_backend.authorize(account, permissions):
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
