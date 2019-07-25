
from .exceptions import PermissionNotMet


class Permissions:
    def __init__(self, and_set=None, or_set=None):
        self.and_set = set(and_set or ())
        self.or_set = set(or_set or ())

    def combine(self, permissions):
        return Permissions(self.and_set | permissions.and_set, self.or_set | permissions.or_set)

    def verify(self, actual_permissions):
        # Verify permissions in and set
        for p in self.and_set:
            if p not in actual_permissions:
                raise PermissionNotMet(p)

        # Verify permissions in or set
        if not self.or_set:
            return

        permissions = self.or_set & actual_permissions
        if len(permissions) == 0:
            raise PermissionNotMet(list(self.or_set)[0])

    def __str__(self):
        s = ''
        if self.and_set:
            s = ' & '.join(self.and_set)

        if self.or_set:
            or_set_str = ' | '.join(self.or_set)
            if s:
                s += ' & (' + or_set_str + ')'

            else:
                s = or_set_str

        return s or '*'

    def __bool__(self):
        return bool(self.and_set) or bool(self.or_set)


def _require_permissions(and_set=None, or_set=None):
    and_set = and_set or set()
    or_set = or_set or set()

    new_permissions = Permissions(and_set, or_set)

    def decorator(handler):
        # Combine any existing permissions with the new ones
        permissions = get_required_permissions(handler) or Permissions()
        handler.permissions = permissions.combine(new_permissions)

        return handler

    return decorator


def require_permission(permission):
    return _require_permissions(and_set=[permission])


def require_one_permission(permissions):
    return _require_permissions(or_set=permissions)


def require_all_permissions(permissions):
    return _require_permissions(and_set=permissions)


def get_required_permissions(handler):
    permissions = getattr(handler, 'permissions', None)
    if permissions is None:
        return

    # Permissions can be stored as:
    #  * a set of permissions
    #  * a Permissions instance

    # Normalize possible ways of storing permissions
    if not isinstance(permissions, Permissions):
        permissions = Permissions(and_set=permissions)

    return permissions
