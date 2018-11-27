
import json
import logging
import re

from aiohttp import web
from aiohttp_apispec import validation_middleware
from webargs import aiohttpparser

from colibris import app
from colibris import settings
from colibris import utils
from colibris.api import BaseJSONException, envelope

from colibris.authentication import exceptions as authentication_exceptions


logger = logging.getLogger(__name__)

_authentication_backend_settings = dict(settings.AUTHENTICATION)
_authentication_backend_path = _authentication_backend_settings.pop('backend',
                                                                    'colibris.authentication.base.NullBackend')
_authentication_backend_class = utils.import_member(_authentication_backend_path)
_authentication_backend = _authentication_backend_class(**_authentication_backend_settings)

_authorization_backend_settings = dict(settings.AUTHORIZATION)
_authorization_backend_path = _authorization_backend_settings.pop('backend',
                                                                  'colibris.authorization.base.NullBackend')
_authorization_backend_class = utils.import_member(_authorization_backend_path)
_authorization_backend = _authorization_backend_class(**_authorization_backend_settings)


class HTTPSchemaValidationError(web.HTTPUnprocessableEntity):
    def __init__(self, schema_error, **kwargs):
        super().__init__(**kwargs)

        self.details = schema_error.messages


@web.middleware
async def handle_errors_json(request, handler):
    try:
        return await handler(request)

    except BaseJSONException as e:
        return web.json_response(envelope.wrap_error(e.code, e.message, e.details), status=e.status)

    except HTTPSchemaValidationError as e:
        code = 'invalid_fields'
        message = 'Some of the supplied fields are invalid.'

        return web.json_response(envelope.wrap_error(code, message, e.details), status=e.status)

    except web.HTTPRedirection as e:
        return e

    except (web.HTTPClientError, web.HTTPServerError) as e:
        code = utils.camelcase_to_underscore(re.sub('[^a-zA-Z0-9_]', '', e.reason))
        message = e.reason

        return web.json_response(envelope.wrap_error(code, message), status=e.status)

    except json.JSONDecodeError as e:
        code = 'invalid_json'
        message = 'Invalid JSON.'
        details = str(e)

        return web.json_response(envelope.wrap_error(code, message, details), status=400)

    except app.HealthException as e:
        code = 'unhealthy'
        message = 'Service is not healthy.'
        details = str(e)

        return web.json_response(envelope.wrap_error(code, message, details), status=500)

    except Exception as e:
        code = 'server_error'
        message = 'Internal Server Error'
        details = None

        if settings.DEBUG:
            import traceback

            logger.error('internal server error: %s', e, exc_info=True)
            details = traceback.format_exc()

        return web.json_response(envelope.wrap_error(code, message, details), status=500)


@web.middleware
async def handle_auth(request, handler):
    if request.match_info.http_exception is not None:
        raise request.match_info.http_exception

    path = request.match_info.route.resource.canonical
    route = app.routes_by_path.get(path)
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

        if not _authorization_backend.authorize(account, method, path, permissions):
            logger.error('%s %s forbidden for %s', method, path, account)

            raise web.HTTPForbidden()

    return await handler(request)


@web.middleware
async def handle_schema_validation(request, handler):
    return await validation_middleware(request, handler)


@aiohttpparser.parser.error_handler
def _handle_schema_validation_error(error, req, schema):
    raise HTTPSchemaValidationError(error)
