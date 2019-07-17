from colibris.docs.openapi.views import apispec_view, ui_view
from colibris.docs.openapi import STATIC_PATH, APISPEC_URL, STATIC_URL, UI_URL


def setup_openapi_ui(app):
    app.router.add_route('GET', APISPEC_URL, apispec_view)
    app.router.add_route('GET', UI_URL, ui_view)

    app.router.add_static(STATIC_URL, STATIC_PATH)
