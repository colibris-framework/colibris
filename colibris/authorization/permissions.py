
from .exceptions import PermissionNotMet


def _require_permissions(_and=None, _or=None):
    _and = _and or []
    _or = _or or []

    def decorator(obj):
        required_permissions = getattr(obj, '__required_permissions', None)
        obj.__required_permissions = combine_permissions(required_permissions, (_and, _or))

        return obj

    return decorator


def require_permission(permission):
    return _require_permissions(_and=[permission])


def require_any_permission():
    return _require_permissions()


def require_one_permission(permissions):
    return _require_permissions(_or=permissions)


def require_all_permissions(permissions):
    return _require_permissions(_and=permissions)


def get_required_permissions(obj):
    return getattr(obj, '__required_permissions', None)


def combine_permissions(perms1, perms2):
    # If either perms1 or perms2 is None, return the other one.
    # If both are None, return None.
    if None in (perms1, perms2):
        return perms1 or perms2

    return perms1[0] + perms2[0], perms1[1] + perms2[1]


def verify_permissions(actual_permissions, required_permissions):
    _and, _or = required_permissions

    _or = set(_or)
    actual_permissions = set(actual_permissions)

    # Verify permissions in _and
    for p in _and:
        if p not in actual_permissions:
            raise PermissionNotMet(p)

    # Verify permissions in _or
    if not _or:
        return

    permissions = _or & actual_permissions
    if len(permissions) == 0:
        raise PermissionNotMet(permissions.pop())
