

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
# @marshal_with(schemas.UserSchema())
# def get_me(request):
#     if request.account:
#         result = schemas.UserSchema().dump(request.account)
#
#     else:
#         result = None
#
#     return web.json_response(result)
#
#
# @docs(summary='Reveal details about a specific user')
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
#
# @docs(summary='Update an existing user')
# @use_kwargs(schemas.UserSchema(partial=True))
# @marshal_with(schemas.UserSchema(partial=True))
# def update_user(request):
#     user_id = request.match_info['id']
#     try:
#         user = models.User.select().where(models.User.id == user_id).get()
#
#     except models.User.DoesNotExist:
#         raise web.HTTPNotFound()
#
#     user.update_fields(request.data)
#
#     try:
#         user.save()
#
#     except persist.IntegrityError as e:
#         return web.json_response({'error': str(e)}, status=422)
#
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result)
#
#
# @docs(summary='Deletes a user')
# def delete_user(request):
#     user_id = request.match_info['id']
#     if models.User.delete().where(models.User.id == user_id).execute() == 0:
#         raise web.HTTPNotFound()
#
#     return web.json_response(status=204)
#
