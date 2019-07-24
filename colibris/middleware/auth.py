
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
    authentication_required = authentication.get_authentication_required(original_handler)
    permissions = authorization.get_required_permissions(original_handler)

    # Then, if we've got a class-based view, look for required permissions in method function
    if inspect.isclass(original_handler) and issubclass(original_handler, views.View):
        method_func = getattr(original_handler, method.lower(), None)
        if method_func:
            method_func_authentication_required = authentication.get_authentication_required(method_func)
            method_func_permissions = authorization.get_required_permissions(method_func)

            if method_func_permissions and permissions:
                permissions = permissions.combine(method_func_permissions)

            else:
                permissions = permissions or method_func_permissions

            if method_func_authentication_required is not None:
                authentication_required = method_func_authentication_required

    # A value of None for authentication_required indicates decision based on permissions
    if authentication_required is None:
        authentication_required = bool(permissions)

    if not authentication_required and permissions:
        raise authorization.AuthorizationException('view requires permissions but does not require authentication')

    if authentication_required:
        try:
            account = authentication.authenticate(request)

        except authentication.AuthenticationException:
            raise api.UnauthenticatedException()

        if permissions is not None:
            try:
                authorization.authorize(account, method, path, original_handler, permissions)

            except authorization.AuthorizationException:
                raise api.ForbiddenException()

    response = await handler(request)
    response = authentication.process_response(request, response)

    return response
