
import os

from colibris.conf import settings

from __packagename__ import views


# Here are some examples of routes. Just remove what you don't need.
from colibris.docs.openapi import DOCS_STATIC_PATH
from colibris.docs.openapi.views import apispec_ui_view, apispec_view

ROUTES = [
    (r'/',                      views.HomeView),
    (r'/health',                views.HealthView),
    (r'/users/me',              views.MeView),
    (r'/users',                 views.UsersView),
    (r'/users/{id:\d+}',        views.UserView),

    (settings.API_DOCS_URL, apispec_ui_view),
    (settings.APISPEC_URL,      apispec_view)
]


STATIC_ROUTES = [
    (DOCS_STATIC_PATH, settings.DOCS_STATIC_URL),
]

# Add static routes, for development purposes
if settings.DEBUG:
    STATIC_ROUTES += [
        (os.path.join(settings.PROJECT_PACKAGE_DIR, 'static'), '/static'),
    ]
