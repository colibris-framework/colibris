
from colibris import persist


class User(persist.Model):
    id = persist.AutoField()
    username = persist.CharField(max_length=128, index=True, unique=True)
    password = persist.CharField(max_length=128)
    first_name = persist.CharField(max_length=64)
    last_name = persist.CharField(max_length=64)
    email = persist.CharField(max_length=128, null=True)
