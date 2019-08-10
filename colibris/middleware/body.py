from aiohttp import web


@web.middleware
async def handle_request_body(request, handler):
    body = await request.text()
    request.body = body

    response = await handler(request)
    return response
