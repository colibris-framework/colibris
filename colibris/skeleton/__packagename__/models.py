from colibris import persist


# Here are some examples of models. Just remove what you don't need.
from __packagename__ import constants


class User(persist.Model):
    id = persist.AutoField()
    username = persist.CharField(max_length=128, index=True, unique=True)
    password = persist.CharField(max_length=128)
    first_name = persist.CharField(max_length=64)
    last_name = persist.CharField(max_length=64)
    email = persist.CharField(max_length=128, null=True)
    role = persist.CharField(max_length=10, choices=constants.ROLES)
