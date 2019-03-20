
from colibris import views


ROUTES = [
    ('GET', '/', views.home),
    ('GET', '/health', views.health),
]


class RouteException(Exception):
    pass


class DuplicateRoute(RouteException):
    def __init__(self, method, path):
        super().__init__('duplicate route {} {}'.format(method, path))
