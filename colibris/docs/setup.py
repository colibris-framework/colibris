from colibris.docs.views import api_spec_view, swagger_view
from colibris.docs import STATIC_PATH, APISPEC_URL, STATIC_URL, SWAGGER_URL


def setup_swagger(app):
    app.router.add_route('GET', APISPEC_URL, api_spec_view)
    app.router.add_route('GET', SWAGGER_URL, swagger_view)

    app.router.add_static(STATIC_URL, STATIC_PATH)
