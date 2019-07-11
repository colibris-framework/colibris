
import os

from colibris.conf import settings

from __packagename__ import views


ROUTES = [
    (r'/users/me',           views.get_me),
    (r'/users',              views.UsersView),
    (r'/users/{id:\d+}',     views.UserView)
]

if settings.DEBUG:
    STATIC_ROUTES = [
        (os.path.join(settings.PROJECT_PACKAGE_DIR, 'static'), '/static'),
    ]
