
import pytest

from __packagename__ import models

#
# @pytest.fixture
# def test_user():
#     yield models.User.create(username='test_user', password='test_password',
#                              first_name='Test', last_name='User',
#                              email='testuser@example.com')
#
#
# @pytest.fixture
# def write_right(test_user):
#     yield models.Right.create(user=test_user, resource='*', operations='w')
#
