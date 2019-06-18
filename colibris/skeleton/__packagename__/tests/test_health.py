
from colibris import persist


async def test_health_check_healthy(web_app_client):
    resp = await web_app_client.get('/health')
    assert resp.status == 200

    j = await resp.json()
    assert j == 'healthy'


async def test_health_check_db_down(web_app_client):
    persist.get_database().drop()

    resp = await web_app_client.get('/health')
    assert resp.status == 500

    j = await resp.json()
    assert j['code'] == 'unhealthy'
