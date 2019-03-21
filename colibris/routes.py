
from colibris import views


ROUTES = [
    ('GET', '/', views.home),
    ('GET', '/health', views.health),
]

STATIC_ROUTES = []
