
from colibris.authorization.role import RoleBackend

from .fixtures import DUMMY_PERMISSION, ANOTHER_PERMISSION, YET_ANOTHER_PERMISSION, DUMMY_ACCOUNT, ANOTHER_ACCOUNT


def test_extract_role():
    backend = RoleBackend(role_field='role')
    assert backend.get_role(account=DUMMY_ACCOUNT) == DUMMY_PERMISSION


def test_actual_permissions_simple():
    backend = RoleBackend(role_field='role')
    assert backend.get_actual_permissions(account=DUMMY_ACCOUNT, method='GET', path='/') == {DUMMY_PERMISSION}


def test_actual_permissions_order():
    backend = RoleBackend(role_field='role', order=[DUMMY_PERMISSION, ANOTHER_PERMISSION, YET_ANOTHER_PERMISSION])
    permissions = backend.get_actual_permissions(account=ANOTHER_ACCOUNT, method='GET', path='/')
    assert permissions == {DUMMY_PERMISSION, ANOTHER_PERMISSION}
