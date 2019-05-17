
from aiohttp import web

from colibris import api
from colibris import app
from colibris import authentication
from colibris import authorization


@web.middleware
async def handle_auth(request, handler):
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    authorization_info = app.route_auth_mapping.get(request.match_info.route)
    method = request.method
    path = request.match_info.route.resource.canonical

    request = authentication.process_request(request)

    # Only go through authentication if route specifies permissions;
    # otherwise route is considered public.
    if authorization_info is not None:
        try:
            account = authentication.authenticate(request)

        except authentication.AuthenticationException:
            raise api.UnauthenticatedException()

        if not authorization.authorize(account, method, path, authorization_info):
            raise api.ForbiddenException()

    response = await handler(request)
    response = authentication.process_response(request, response)

    return response
