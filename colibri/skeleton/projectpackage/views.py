

from aiohttp import web
from aiohttp_apispec import docs

from __packagename__ import models
from __packagename__ import schemas

#
# View example:
#
# @docs(summary='List all users')
# def list_users(request):
#     users = models.User.select().order_by(models.User.username.asc())
#     result = schemas.dump(list(users))
#
#     return web.json_response(result)
#
