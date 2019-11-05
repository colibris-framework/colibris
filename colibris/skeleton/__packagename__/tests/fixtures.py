import pytest

from __packagename__ import models


TEST_USER_PASSWORD = 'eyJzdWIiOiJ0ZXN0X3VzZXIifQ'


@pytest.fixture
def test_user():
    yield models.User.create(username='test_user', key='eyJzdWIiOiJ0ZXN0X3VzZXIifQ',
                             first_name='Test', last_name='User',
                             email='testuser@example.com')
