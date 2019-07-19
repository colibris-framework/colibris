
import os

from colibris.conf import settings

from __packagename__ import views

# Here are some examples of routes. Just remove what you don't need.

ROUTES = [
    (r'/', views.HomeView),
    (r'/health', views.HealthView),
    (r'/users/me', views.MeView),
    (r'/users', views.UsersView),
    (r'/users/{id:\d+}', views.UserView)
]


# Add static routes, for development purposes

if settings.DEBUG:
    STATIC_ROUTES = [
        (os.path.join(settings.PROJECT_PACKAGE_DIR, 'static'), '/static'),
    ]
