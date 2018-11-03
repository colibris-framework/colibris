
import importlib

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger

from colibri import middlewares
from colibri import settings
from colibri import views


async def init_swagger(app):  # TODO do we need this to be async?
    setup_swagger(app=app, swagger_url=settings.API_DOCS_PATH, swagger_info=app['swagger_dict'])


app = web.Application(middlewares=[middlewares.authorization])

app.router.add_get('/', views.home)
app.router.add_get('/health', views.health)

# add apispec/swagger support
setup_aiohttp_apispec(
    app=app,
    title='API Documentation',
)

app.on_startup.append(init_swagger)

# add project-specific routes & views
try:
    _routes_module = importlib.import_module('{}.routes'.format(settings.PROJECT_PACKAGE_NAME))

except ImportError:
    _routes_module = lambda: None
    _routes_module.ROUTES = []

try:
    _views_module = importlib.import_module('{}.views'.format(settings.PROJECT_PACKAGE_NAME))

except ImportError:
    _views_module = lambda: None


for _method, _path, _handler_name in _routes_module.ROUTES:
    _handler = getattr(_views_module, _handler_name)
    app.router.add_route(_method, _path, _handler)
