
import os

from colibris.conf import settings

from __packagename__ import views

#
# Routes example:
#
# ROUTES = [
#     (r'/users/me',           views.get_me),
#     (r'/users',              views.UsersView),
#     (r'/users/{id:\d+}',     views.UserView)
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
