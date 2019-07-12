from aiohttp import web
from aiohttp_apispec import docs, response_schema

from colibris import views
from colibris.authentication import get_account
from colibris.authorization import require_any_permission, ANY_PERMISSION
from colibris.views.generic import RetrieveUpdateDeleteModelView, ListCreateModelView

from __packagename__ import constants
from __packagename__ import models
from __packagename__ import schemas


# Here are some examples of views. Just remove what you don't need.

class MeView(views.View):
    required_permissions = ANY_PERMISSION

    @docs(tags=['Users'], summary='Reveal details about the current user')
    @response_schema(schemas.UserSchema())
    @require_any_permission()
    async def get(self):
        user = get_account(self.request)
        result = schemas.UserSchema().dump(user)

        return web.json_response(result)


class UsersView(ListCreateModelView):
    required_permissions = constants.ROLE_ADMIN
    body_schema_class = schemas.UserSchema
    model = models.User

    @docs(tags=['Users'], summary='List all users')
    async def get(self):
        return await super().get()

    @docs(tags=['Users'], summary='Add a new user')
    async def post(self):
        return await super().post()


class UserView(RetrieveUpdateDeleteModelView):
    required_permissions = constants.ROLE_ADMIN
    body_schema_class = schemas.UserSchema
    model = models.User

    @docs(tags=['Users'], summary='Reveal details about a specific user')
    async def get(self):
        return await super().get()

    @docs(tags=['Users'], summary='Update an existing user')
    async def patch(self):
        return await super().patch()

    @docs(tags=['Users'], summary='Update an existing user')
    async def put(self):
        return await super().put()

    @docs(tags=['Users'], summary='Delete a user')
    async def delete(self):
        return await super().delete()
