from colibris.views.generic import home, health

ROUTES = [
    ('GET', '/', home),
    ('GET', '/health', health),
]

STATIC_ROUTES = []
