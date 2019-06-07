
import json
import logging
import re

from aiohttp import web

from colibris import app
from colibris import authentication
from colibris import utils
from colibris.api import BaseJSONException, envelope
from colibris.conf import settings

from .schema import HTTPSchemaValidationError


logger = logging.getLogger(__name__)


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
