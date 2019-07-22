# Cache

The caching mechanism is configured via the `CACHE` variable in `${PACKAGE}/settings.py`. Caching is disabled by
default.

## Usage

To use the caching mechanism, just import it wherever you need it:

    from colibris import cache
    
To set a value, use `set`:

    cache.set('my_key', my_value, lifetime=300)

Later, you can get your value back:

    my_value = cache.get('my_key', default='some_default')

You can invalidate a key using `delete`:

    cache.delete('my_key')

## Redis Backend

Make sure to have the `redis` python package installed.

In `${PACKAGE}/settings.py`, set:

    CACHE = {
        'backend': 'colibris.cache.redis.RedisBackend',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': 'yourpassword'
    }
