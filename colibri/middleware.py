
from aiohttp import web

from colibri import auth
from colibri import settings
from colibri import utils


_auth_backend_class = utils.import_member(settings.AUTHENTICATION['backend'])
_auth_backend = _auth_backend_class(**settings.AUTHENTICATION)


@web.middleware
async def handle_authentication(request, handler):
    try:
        account = _auth_backend.authenticate(request)

    except auth.AuthException:
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
