

from aiohttp import web
from aiohttp_apispec import docs, use_kwargs, marshal_with

from __packagename__ import models
from __packagename__ import schemas

#
# View example:
#
# @docs(summary='List all users')
# @use_kwargs(schemas.UserSchema())
# @marshal_with(schemas.UserSchema())
# def list_users(request):
#     users = models.User.select().order_by(models.User.username.asc())
#     result = schemas.UserSchema(many=True).dump(list(users))
#
#     return web.json_response(result)
#
