# Authorization

Choose a backend for the authorization by setting the `AUTHORIZATION` variable in `${PACKAGE}/settings.py`. By default,
a null backend is used, allowing everybody to perform any request.

## Role Backend

In `${PACKAGE}/settings.py`, set:

    AUTHORIZATION = {
        'backend': 'colibris.authorization.role.RoleBackend',
        'role_field': 'role'
    }

## Rights Backend

In `${PACKAGE}/settings.py`, set:

    AUTHORIZATION = {
        'backend': 'colibris.authorization.rights.RightsBackend',
        'model': 'yourproject.models.Right',
        'account_field': 'user',
        'resource_field': 'resource',
        'operation_field': 'operation'
    }
