
from .permissions.fixtures import *


@pytest.fixture
def http_client_maker(aiohttp_client):

    def client(authentication_backend=None, authorization_backend=None,
               routes=None, middlewares=None):

        if middlewares is None:
            middlewares = [
                handle_errors_json,
                handle_auth
            ]

        app = web.Application(middlewares=middlewares)
        routes = routes or []

        for path, view in routes:
            app.router.add_route('*', path, view)

        if not authentication_backend:
            authentication_backend = 'colibris.authentication.null.NullBackend'

        if not authorization_backend:
            authorization_backend = 'colibris.authorization.null.NullBackend'

        authentication.AuthenticationBackend.configure({
            'backend': authentication_backend
        })

        if authorization_backend:
            authorization.AuthorizationBackend.configure({
                'backend': authorization_backend
            })

        return aiohttp_client(app)

    return client
