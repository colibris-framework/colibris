
import pytest

from colibris import app


@pytest.fixture
async def web_app_client(aiohttp_client):
    return await aiohttp_client(app.get_web_app(force_create=True))
