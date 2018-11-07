

from aiohttp import web
from aiohttp_apispec import docs, use_kwargs, marshal_with

from colibri import persist

from __packagename__ import models
from __packagename__ import schemas

#
# View examples:
#
#
# @docs(summary='Reveal details about the current user')
# @use_kwargs(schemas.UserSchema())
# @marshal_with(schemas.UserSchema())
# def get_me(request):
#     result = schemas.UserSchema().dump(request.account)
#
#     return web.json_response(result)
#
#
# @docs(summary='Reveal details about a specific user')
# @use_kwargs(schemas.UserSchema())
# @marshal_with(schemas.UserSchema())
# def get_user(request):
#     user_id = request.match_info['id']
#     try:
#         user = models.User.select().where(models.User.id == user_id).get()
#
#     except models.User.DoesNotExist:
#         raise web.HTTPNotFound()
#
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result)
#
#
# @docs(summary='List all users')
# @use_kwargs(schemas.UserSchema())
# @marshal_with(schemas.UserSchema(many=True))
# def list_users(request):
#     users = models.User.select().order_by(models.User.username.asc())
#     result = schemas.UserSchema(many=True).dump(list(users))
#
#     return web.json_response(result)
#
#
# @docs(summary='Add a new user')
# @use_kwargs(schemas.UserSchema())
# @marshal_with(schemas.UserSchema())
# def add_user(request):
#     try:
#         user = models.User.create(**request.data)
#
#     except persist.IntegrityError as e:
#         return web.json_response({'error': str(e)}, status=422)
#
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result, status=201)
#
