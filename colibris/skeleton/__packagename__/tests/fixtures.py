import pytest

from __packagename__ import models
from __packagename__ import constants


TEST_USER_PASSWORD = 'eyJzdWIiOiJ0ZXN0X3VzZXIifQ'


@pytest.fixture
def test_user():
    yield models.User.create(name='test_user', key=TEST_USER_PASSWORD,
                             email='testuser@example.com', role=constants.ROLE_ADMIN)
