
import peewee


_database_proxy = peewee.DatabaseProxy()


class Model(peewee.Model):
    # This is currently necessary for aiohttp-apispec request data validation
    def __iter__(self):
        return ((k, v) for (k, v) in self.__data__.items())

    def update_fields(self, fields):
        for n, v in fields.items():
            setattr(self, n, v)

    class Meta:
        database = _database_proxy


def set_database(database):
    _database_proxy.initialize(database)
