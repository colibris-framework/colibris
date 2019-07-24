
import inspect

from aiohttp import web

from colibris import api
from colibris import authentication
from colibris import authorization
from colibris import views


@web.middleware
async def handle_auth(request, handler):
    # Bail out with exception if we haven't gotten proper match_info
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    request = authentication.process_request(request)

    method = request.method
    path = request.match_info.route.resource.canonical

    original_handler = request.match_info.handler

    # First look for auth info in the view handler itself (class or function)
    required_authentication = authentication.get_required_authentication(original_handler)
    required_permissions = authorization.get_required_permissions(original_handler)

    # Then, if we've got a class-based view, look for required permissions in method function
    if inspect.isclass(original_handler) and issubclass(original_handler, views.View):
        method_func = getattr(original_handler, method.lower(), None)
        if method_func:
            method_func_required_authentication = authentication.get_required_authentication(method_func)
            method_func_required_permissions = authorization.get_required_permissions(method_func)

            if method_func_required_permissions and required_permissions:
                required_permissions = required_permissions.combine(method_func_required_permissions)

            else:
                required_permissions = required_permissions or method_func_required_permissions

            if method_func_required_authentication is not None:
                required_authentication = method_func_required_authentication

    # A value of None for required_authentication indicates decision based on permissions
    if required_authentication is None:
        required_authentication = bool(required_permissions)

    if not required_authentication and required_permissions:
        raise authorization.AuthorizationException('view requires permissions but does not require authentication')

    if required_authentication:
        try:
            account = authentication.authenticate(request)

        except authentication.AuthenticationException:
            raise api.UnauthenticatedException()

        if required_permissions is not None:
            try:
                authorization.authorize(account, method, path, original_handler, required_permissions)

            except authorization.AuthorizationException:
                raise api.ForbiddenException()

    response = await handler(request)
    response = authentication.process_response(request, response)

    return response
