
import pytest

from colibris.authorization import permissions

from .fixtures import DUMMY_PERMISSION, ANOTHER_PERMISSION, YET_ANOTHER_PERMISSION


def test_conjunction():
    p = permissions.Permissions(and_set={DUMMY_PERMISSION, ANOTHER_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify(set())

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({DUMMY_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({ANOTHER_PERMISSION})

    p.verify({DUMMY_PERMISSION, ANOTHER_PERMISSION})


def test_disjunction():
    p = permissions.Permissions(or_set={DUMMY_PERMISSION, ANOTHER_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify(set())

    p.verify({DUMMY_PERMISSION})
    p.verify({ANOTHER_PERMISSION})
    p.verify({DUMMY_PERMISSION, ANOTHER_PERMISSION})


def test_conjunction_disjunction():
    p = permissions.Permissions(and_set={DUMMY_PERMISSION, ANOTHER_PERMISSION},
                                or_set={DUMMY_PERMISSION, YET_ANOTHER_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify(set())

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({DUMMY_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({ANOTHER_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({YET_ANOTHER_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({DUMMY_PERMISSION, YET_ANOTHER_PERMISSION})

    with pytest.raises(permissions.PermissionNotMet):
        p.verify({ANOTHER_PERMISSION, YET_ANOTHER_PERMISSION})

    p.verify({DUMMY_PERMISSION, ANOTHER_PERMISSION})
    p.verify({DUMMY_PERMISSION, ANOTHER_PERMISSION, YET_ANOTHER_PERMISSION})


def test_combine():
    p1 = permissions.Permissions(and_set={DUMMY_PERMISSION}, or_set={ANOTHER_PERMISSION})
    p2 = permissions.Permissions(and_set={ANOTHER_PERMISSION}, or_set={YET_ANOTHER_PERMISSION})

    c = p1.combine(p2)
    assert c.and_set == {DUMMY_PERMISSION, ANOTHER_PERMISSION}
    assert c.or_set == {ANOTHER_PERMISSION, YET_ANOTHER_PERMISSION}
