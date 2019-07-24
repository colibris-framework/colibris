
from aiohttp import web

from colibris import authorization
from colibris import views


DUMMY_PERMISSION = 'dummy_permission'


class DummyView(views.View):
    async def get(self):
        return web.json_response({'message': 'dummy'})


class DummyViewWithClassPermission(DummyView):
    required_permissions = {DUMMY_PERMISSION}


class DummyViewWithMethodPermission(DummyView):
    @authorization.require_permission(DUMMY_PERMISSION)
    async def get(self):
        return await super().get()


class PermissionAuthorizationBackend(authorization.AuthorizationBackend):
    def get_actual_permissions(self, account, method, path):
        return {DUMMY_PERMISSION}


class NoPermissionAuthorizationBackend(authorization.AuthorizationBackend):
    def get_actual_permissions(self, account, method, path):
        return ()


async def test_default_view_permissions(http_client_maker):
    client = await http_client_maker(routes=[('/dummy', DummyView)])
    response = await client.get('/dummy')

    assert response.status == 200


async def test_class_required_permissions_fulfilled(http_client_maker):
    client = await http_client_maker(routes=[('/dummy', DummyViewWithClassPermission)],
                                     authorization_backend=PermissionAuthorizationBackend)
    response = await client.get('/dummy')

    assert response.status == 200


async def test_class_required_permissions_not_fulfilled(http_client_maker):
    client = await http_client_maker(routes=[('/dummy', DummyViewWithClassPermission)],
                                     authorization_backend=NoPermissionAuthorizationBackend)
    response = await client.get('/dummy')

    assert response.status == 403


async def test_method_required_permissions_fulfilled(http_client_maker):
    client = await http_client_maker(routes=[('/dummy', DummyViewWithMethodPermission)],
                                     authorization_backend=PermissionAuthorizationBackend)
    response = await client.get('/dummy')

    assert response.status == 200


async def test_method_required_permissions_not_fulfilled(http_client_maker):
    client = await http_client_maker(routes=[('/dummy', DummyViewWithMethodPermission)],
                                     authorization_backend=NoPermissionAuthorizationBackend)
    response = await client.get('/dummy')

    assert response.status == 403
