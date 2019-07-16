from os.path import join

from aiohttp.web_response import Response, json_response

from colibris.docs import STATIC_PATH, APISPEC_URL, STATIC_URL


async def swagger_view(request):
    with open(join(STATIC_PATH, "index.html")) as f:
        content = f.read().replace("##API_SPEC_URL##", APISPEC_URL).replace("##STATIC_BASE_URL##", STATIC_URL)

    return Response(
        text=content,
        content_type="text/html"
    )


async def api_spec_view(request):
    return json_response(request.app["swagger_dict"])
