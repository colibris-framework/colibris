
import os

from colibris.conf import settings
from colibris.authorization import ANY_PERMISSION

from __packagename__ import views
from __packagename__.constants import ROLE_ADMIN, ROLE_REGULAR


ROUTES = [
    ('GET',     r'/users/me',           views.get_me,           ANY_PERMISSION),
    (None,      r'/users',              views.UsersView,        {ROLE_ADMIN}),
    (None,      r'/users/{id:\d+}',     views.UserView,         {ROLE_ADMIN})
]

if settings.DEBUG:
    STATIC_ROUTES = [
        (os.path.join(settings.PROJECT_PACKAGE_DIR, 'static'), '/static'),
    ]
