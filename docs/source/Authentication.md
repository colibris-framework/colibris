# Authentication

Choose a backend for the authentication by setting the `AUTHENTICATION` variable in `${PACKAGE}/settings.py`. By
default, a null backend is used which associates each request with a dummy account.

## JWT Backend

Make sure to have the `pyjwt` python package installed. 

In `${PACKAGE}/settings.py`, set:

    AUTHENTICATION = {
        'backend': 'colibris.authentication.jwt.JWTBackend',
        'model': 'yourproject.models.User',
        'identity_claim': 'sub',
        'identity_field': 'username',
        'secret_field': 'password',
        'cookie_name': 'auth_token',
        'cookie_domain': 'example.com',
        'validity_seconds': 3600 * 24 * 30
    }
    
The `cookie_name` property is optional and tells the backend to look for the token in cookies as well, in addition to
the `Authorization` header.

The `cookie_domain` property is optional and configures the cookie domain.

The `validity_seconds` property is optional and configures the given validity for the token.

## API Key Backend

In `${PACKAGE}/settings.py`, set:

    AUTHENTICATION = {
        'backend': 'colibris.authentication.apikey.APIKeyBackend',
        'model': 'yourproject.models.User',
        'key_field': 'secret',
    }
