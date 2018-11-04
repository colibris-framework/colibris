
import re

from aiohttp import web
from aiohttp.web_response import json_response

from colibri import settings


_AUTH_HEADER = 'Authorization'
_AUTH_TOKEN_REGEX = re.compile('Bearer (.+)', re.IGNORECASE)

_all_routes = []


@web.middleware
async def authorization(request, handler):
    global _all_routes

    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    if not _all_routes:
        _all_routes = set(path.resource.canonical for path in request.app.router.routes())

    canonical = request.match_info.route.resource.canonical
    needs_auth = (canonical in _all_routes) and (canonical not in settings.PUBLIC_ROUTES)

    if needs_auth:
        auth_header = request.headers.get(_AUTH_HEADER)
        if auth_header is None:
            return json_response({'detail': 'Not authenticated request.'}, status=401)

        m = _AUTH_TOKEN_REGEX.match(auth_header)
        if not m:
            return json_response({'detail': 'Auth header format is wrong.'}, status=401)

        token = m.group(1)

        # TODO: Check token in db
        return json_response({'detail': 'Not authenticated request.'}, status=401)

    response = await handler(request)

    return response


@web.middleware
async def handle_errors_json(request, handler):
    try:
        return await handler(request)

    except web.HTTPException as e:
        if e.status >= 400:
            return web.json_response({'error': e.reason}, status=e.status)

        return e
