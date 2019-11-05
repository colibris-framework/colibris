from colibris import persist


# Here are some examples of models. Just remove what you don't need.
from __packagename__ import constants


class User(persist.Model):
    id = persist.AutoField()
    name = persist.CharField(max_length=128, index=True, unique=True)
    key = persist.CharField(max_length=128)
    email = persist.CharField(max_length=128, null=True)
    role = persist.CharField(max_length=10, choices=[(r, r) for r in constants.ROLES])
