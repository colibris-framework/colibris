
import inspect

from aiohttp import web

from colibris import api
from colibris import authentication
from colibris import authorization
from colibris import views
from colibris.authorization.permissions import get_required_permissions


@web.middleware
async def handle_auth(request, handler):
    # Bail out with exception if we haven't gotten proper match_info
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    request = authentication.process_request(request)

    method = request.method
    path = request.match_info.route.resource.canonical

    original_handler = request.match_info.handler

    # First look for required permissions in the view handler itself (class or function)
    required_permissions = get_required_permissions(original_handler)

    # Then, if we've got a class-based view, look for required permissions in method function
    if inspect.isclass(original_handler) and issubclass(original_handler, views.View):
        method_func = getattr(original_handler, method.lower(), None)
        if method_func:
            method_func_required_permissions = get_required_permissions(method_func)
            if method_func_required_permissions and required_permissions:
                required_permissions = required_permissions.combine(method_func_required_permissions)

            else:
                required_permissions = required_permissions or method_func_required_permissions

    try:
        account = authentication.authenticate(request)

    except authentication.AuthenticationException:
        if required_permissions is not None:
            raise api.UnauthenticatedException()

        account = None

    if required_permissions is not None:
        try:
            authorization.authorize(account, method, path, original_handler, required_permissions)

        except authorization.AuthorizationException:
            raise api.ForbiddenException()

    response = await handler(request)
    response = authentication.process_response(request, response)

    return response
