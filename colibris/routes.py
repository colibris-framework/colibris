
from colibris import views

ROUTES = [
    ('GET', '/', views.home),
    ('GET', '/health', views.health),
]
