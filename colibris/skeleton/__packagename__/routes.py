
import os

from colibris import settings
from colibris.authorization import ANY_PERMISSION

from __packagename__ import views
from __packagename__.constants import ROLE_ADMIN, ROLE_REGULAR

#
# Routes example:
#
# ROUTES = [
#     ('GET',    '/users/me',   views.get_me,       ANY_PERMISSION),
#     ('GET',    '/users/{id}', views.get_user,     {ROLE_ADMIN}),
#     ('GET',    '/users',      views.list_users,   {ROLE_ADMIN}),
#     ('POST',   '/users',      views.add_user,     {ROLE_ADMIN}),
#     ('PATCH',  '/users/{id}', views.update_user,  {ROLE_ADMIN}),
#     ('DELETE', '/users/{id}', views.delete_user,  {ROLE_ADMIN}),
#
#     ('GET',    '/my_resource/{id}', views.get_my_resource, {ROLE_ADMIN, ROLE_REGULAR}),
# ]
#

#
# Add static routes, for development purposes
#
# if settings.DEBUG:
#     STATIC_ROUTES = [
#         (os.path.join(settings.PROJECT_PACKAGE_DIR, 'static'), '/static'),
#     ]
#