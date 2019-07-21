# Tests

## The `pytest` Framework

Colibris uses [pytest](https://docs.pytest.org/) to provide an integrated testing framework. All features, plugins and
common practices available with `pytest` are available with Colibris as well.

## Writing Tests

One should simply place tests in the `${PACKAGE}/tests` package. The `pytest` discovery mechanism will recursively look
for modules starting with `test_` and will run any function that starts with `test_` or ends with `_test`.

The following functions, placed in a file named e.g. `test_health.py` will test the health status API endpoint:

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

## Testing Utilities & Fixtures

`pytest` recommends building tests around *fixtures*. Colibris provides the `web_app_client` fixture which wraps the
`aiohttp_client` fixture and allows simulating HTTP requests "directly", bypassing any network layer.

Other testing utilities can be found in the `utils` module:

    from colibris.test import utils 

For validating enveloped API responses, one can then use `utils.assert_is_envelope`:

    resp = await web_app_client.get('/users')
    assert resp.status == 200
    
    j = await resp.json()
    utils.assert_is_envelope(j, count=2)

## The `test` Management Command

Running the tests is achieved by running the `test` management command:

    ./${PACKAGE}/manage.py test

Any arguments passed to this command are passed internally to `pytest`. Running `pytest` directly is not recommended and
will probably fail.

## Test Database

Colibris will use the `TEST_DATABASE` setting for persistence when running tests. In the absence of a field in this
setting (which is by default), corresponding fields from `DATABASE` setting will be used, but `name` will be prefixed
with `test_`.

The test database is created at the setup phase of each test and dropped at the teardown phase. Its structure is created
using migration scripts. Populating it with data is the responsibility of the test writer.

## The `fixtures` Module

The `./${PACKAGE}/tests/fixtures.py` module can be used to define project-specific testing fixtures as well as
constants. Here's an example of a fixture that creates a test user in the database:

    @pytest.fixture
    def test_user():
        yield models.User.create(username='test_user', password='test_password',
                                 first_name='Test', last_name='User',
                                 email='testuser@example.com')
