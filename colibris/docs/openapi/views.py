from os.path import join

from aiohttp.web_response import Response, json_response

from colibris.conf import settings
from colibris.docs.openapi import DOCS_STATIC_PATH


async def apispec_ui_view(request):
    with open(join(DOCS_STATIC_PATH, "index.html")) as f:
        content = f.read()

    content = content.replace("##API_SPEC_URL##", settings.APISPEC_URL)
    content = content.replace("##STATIC_BASE_URL##", settings.DOCS_STATIC_URL)

    return Response(text=content, content_type="text/html")


async def apispec_view(request):
    return json_response(request.app["swagger_dict"])
