
import json
import logging
import re

from aiohttp import web
from aiohttp_apispec import validation_middleware
from webargs import aiohttpparser

from colibris import api
from colibris import app
from colibris import authentication
from colibris import authorization
from colibris import settings
from colibris import utils
from colibris.api import BaseJSONException, envelope


logger = logging.getLogger(__name__)


class HTTPSchemaValidationError(web.HTTPUnprocessableEntity):
    def __init__(self, schema_error, **kwargs):
        super().__init__(**kwargs)

        self.details = schema_error.messages


def _extract_request_logging_info(request):
    info = '{method} {path}'.format(method=request.method, path=request.path)
    account = authentication.get_account(request)
    if account:
        info += ' (account={})'.format(account)

    info += ': '

    return info


@web.middleware
async def handle_errors_json(request, handler):
    try:
        return await handler(request)

    except BaseJSONException as e:
        logger.warning('%s%s', _extract_request_logging_info(request), e)

        return web.json_response(envelope.wrap_error(e.code, e.message, e.details), status=e.status)

    except HTTPSchemaValidationError as e:
        code = 'invalid_fields'
        message = 'Some of the supplied fields are invalid.'
        logger.warning('%sschema validation error: %s', _extract_request_logging_info(request), e.details)

        return web.json_response(envelope.wrap_error(code, message, e.details), status=e.status)

    except web.HTTPRedirection as e:
        return e

    except (web.HTTPClientError, web.HTTPServerError) as e:
        code = utils.camelcase_to_underscore(re.sub('[^a-zA-Z0-9_]', '', e.reason))
        message = e.reason
        logger.warning('%s%s', _extract_request_logging_info(request), e)

        return web.json_response(envelope.wrap_error(code, message), status=e.status)

    except json.JSONDecodeError as e:
        code = 'invalid_json'
        message = 'Invalid JSON.'
        details = str(e)
        logger.warning('%sinvalid JSON: %s', _extract_request_logging_info(request), e)

        return web.json_response(envelope.wrap_error(code, message, details), status=400)

    except app.HealthException as e:
        code = 'unhealthy'
        message = 'Service is not healthy.'
        details = str(e)
        logger.critical('%sservice is not healthy: %s', _extract_request_logging_info(request), e)

        return web.json_response(envelope.wrap_error(code, message, details), status=500)

    except Exception as e:
        code = 'server_error'
        message = 'Internal Server Error'
        details = None
        logger.error('%sinternal server error: %s', _extract_request_logging_info(request), e, exc_info=True)

        if settings.DEBUG:
            import traceback

            details = traceback.format_exc()

        return web.json_response(envelope.wrap_error(code, message, details), status=500)


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


@web.middleware
async def handle_schema_validation(request, handler):
    return await validation_middleware(request, handler)


@aiohttpparser.parser.error_handler
def _handle_schema_validation_error(error, req, schema, status_code, headers):
    raise HTTPSchemaValidationError(error)
