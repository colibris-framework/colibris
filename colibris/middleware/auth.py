
from aiohttp import web

from colibris import api
from colibris import authentication
from colibris import authorization
from colibris import views
from colibris.authorization.permissions import get_required_permissions, combine_permissions


@web.middleware
async def handle_auth(request, handler):
    # Bail out with exception if we haven't gotten proper match_info
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    request = authentication.process_request(request)

    method = request.method
    path = request.match_info.route.resource.canonical

    required_permissions = get_required_permissions(handler)
    if isinstance(handler, views.View):
        method = getattr(handler, method, None)
        if method:
            required_permissions = combine_permissions(required_permissions, get_required_permissions(method))

    # Only go through authentication if permissions are specified; otherwise view is considered public.
    if required_permissions is not None:
        try:
            account = authentication.authenticate(request)

        except authentication.AuthenticationException:
            raise api.UnauthenticatedException()

        try:
            authorization.authorize(account, method, path, handler, required_permissions)

        except authorization.AuthorizationException:
            raise api.ForbiddenException()

    response = await handler(request)
    response = authentication.process_response(request, response)

    return response
