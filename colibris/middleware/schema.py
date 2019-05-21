
import logging

from aiohttp import web
from aiohttp_apispec import validation_middleware
from webargs import aiohttpparser


logger = logging.getLogger(__name__)


class HTTPSchemaValidationError(web.HTTPUnprocessableEntity):
    def __init__(self, schema_error, **kwargs):
        super().__init__(**kwargs)

        self.details = schema_error.messages


@web.middleware
async def handle_schema_validation(request, handler):
    return await validation_middleware(request, handler)


@aiohttpparser.parser.error_handler
def _handle_schema_validation_error(error, req, schema, status_code, headers):
    raise HTTPSchemaValidationError(error)
