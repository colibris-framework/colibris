

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from colibris import api
from colibris import authentication
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
# @response_schema(schemas.UserSchema())
# async def get_me(request):
#     user = authentication.get_account(request)
#     result = schemas.UserSchema().dump(user)
#
#     return web.json_response(result)
#
#
# class UsersView(web.View):
#     @docs(tags=['Users'],
#           summary='List all users')
#     @response_schema(many_envelope(schemas.UserSchema))
#     async def get(self):
#         users = models.User.select().order_by(models.User.username.asc())
#         result = schemas.UserSchema(many=True).dump(list(users))
#
#         return web.json_response(result)
#
#     @docs(tags=['Users'],
#           summary='Add a new user')
#     @request_schema(schemas.UserSchema())
#     @response_schema(schemas.UserSchema())
#     async def post(self):
#         data = self.request['data']
#
#         if models.User.select().where(models.User.username == data['username']).exists():
#             raise api.DuplicateModelException(models.User, 'username')
#
#         user = models.User.create(**data)
#         result = schemas.UserSchema().dump(user)
#
#         return web.json_response(result, status=201)
#
#
# class UserView(web.View):
#     @docs(tags=['Users'],
#           summary='Reveal details about a specific user')
#     @response_schema(schemas.UserSchema())
#     async def get(self):
#         user_id = self.request.match_info['id']
#         user = get_object_or_404(models.User, user_id)
#
#         result = schemas.UserSchema().dump(user)
#
#         return web.json_response(result)
#
#     @docs(tags=['Users'],
#           summary='Update an existing user')
#     @request_schema(schemas.UserSchema(partial=True))
#     @response_schema(schemas.UserSchema(partial=True))
#     async def patch(self):
#         user_id = self.request.match_info['id']
#         user = get_object_or_404(models.User, user_id)
#         data = self.request['data']
#
#         if 'username' in data:
#             query = (models.User.username == data['username']) & (models.User.id != user_id)
#             if models.User.select().where(query).exists():
#                 raise api.DuplicateModelException(models.User, 'username')
#
#         user.update_fields(data)
#         user.save()
#
#         result = schemas.UserSchema().dump(user)
#
#         return web.json_response(result)
#
#     @docs(tags=['Users'],
#           summary='Delete a user')
#     async def delete(self):
#         user_id = self.request.match_info['id']
#         if models.User.delete().where(models.User.id == user_id).execute() == 0:
#             raise api.ModelNotFoundException(models.User)
#
#         return web.json_response(status=204)
#
