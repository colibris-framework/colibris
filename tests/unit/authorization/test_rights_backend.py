
import pytest

from colibris.authorization.rights import RightsBackend
from colibris import persist


USERNAME1 = 'username1'
USERNAME2 = 'username2'

RESOURCE = 'resource'
OPERATION = 'operation'
PERMISSION = '{}:{}'.format(RESOURCE, OPERATION)


class User(persist.Model):
    username = persist.CharField()


class Right(persist.Model):
    user = persist.ForeignKeyField(User)
    resource = persist.CharField()
    operation = persist.CharField()


@pytest.fixture
def database(database_maker):
    return database_maker(models=[User, Right])


@pytest.fixture
def user1(database):
    return User.create(username=USERNAME1)


@pytest.fixture
def user2(database):
    return User.create(username=USERNAME2)


@pytest.fixture
def right(user1):
    return Right.create(user=user1, resource=RESOURCE, operation=OPERATION)


@pytest.fixture
def backend():
    return RightsBackend(model=Right, account_field='user',
                         resource_field='resource', operation_field='operation')


def test_allowed(backend, user1, right):
    assert backend.get_actual_permissions(account=user1, method='GET', path='/') == {PERMISSION}


def test_forbidden(backend, user2, right):
    assert backend.get_actual_permissions(account=user2, method='GET', path='/') == set()
