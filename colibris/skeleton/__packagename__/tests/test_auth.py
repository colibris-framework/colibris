
from . import fixtures

#
# async def test_unauthenticated(web_app_client):
#     resp = await web_app_client.get('/api/users')
#     assert resp.status == 401
#
#     j = await resp.json()
#     assert j['code'] == 'unauthenticated'
#
#
# async def test_authenticated(web_app_client, test_user, write_right):
#     token = fixtures.TEST_USER_JWT
#     resp = await web_app_client.get('/api/users/me', headers={'Authorization': 'Bearer {}'.format(token)})
#     assert resp.status == 200
#
