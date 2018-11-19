

from aiohttp import web
from aiohttp_apispec import docs, use_kwargs, marshal_with

from colibris import api
from colibris.schemas import many_envelope
from colibris.shortcuts import get_object_or_404

from __packagename__ import models
from __packagename__ import schemas

#
# View examples:
#
#
# @docs(tags=['Users'],
#       summary='Reveal details about the current user')
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
# @docs(tags=['Users'],
#       summary='Reveal details about a specific user')
# @marshal_with(schemas.UserSchema())
# def get_user(request):
#     user_id = request.match_info['id']
#     user = get_object_or_404(models.User, user_id)
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result)
#
#
# @docs(tags=['Users'],
#       summary='List all users')
# @marshal_with(many_envelope(schemas.UserSchema))
# def list_users(request):
#     users = models.User.select().order_by(models.User.username.asc())
#     result = schemas.UserSchema(many=True).dump(list(users))
#
#     return web.json_response(result)
#
#
# @docs(tags=['Users'],
#       summary='Add a new user')
# @use_kwargs(schemas.UserSchema())
# @marshal_with(schemas.UserSchema())
# def add_user(request):
#     if models.User.select().where(models.User.username == request.data['username']).exists():
#         raise api.DuplicateException(models.User, 'username')
#
#     user = models.User.create(**request.data)
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result, status=201)
#
#
# @docs(tags=['Users'],
#       summary='Update an existing user')
# @use_kwargs(schemas.UserSchema(partial=True))
# @marshal_with(schemas.UserSchema(partial=True))
# def update_user(request):
#     user_id = request.match_info['id']
#     user = get_object_or_404(models.User, user_id)
#
#     query = (models.User.username == request.data['username'] and
#              models.User.id != user_id)
#     if models.User.select().where(query).exists():
#         raise api.DuplicateException(models.User, 'username')
#
#     user.update_fields(request.data)
#
#     user.save()
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result)
#
#
# @docs(tags=['Users'],
#       summary='Delete a user')
# def delete_user(request):
#     user_id = request.match_info['id']
#     if models.User.delete().where(models.User.id == user_id).execute() == 0:
#         raise api.NotFoundException(models.User)
#
#     return web.json_response(status=204)
#
