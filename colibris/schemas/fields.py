from marshmallow.fields import *

from colibris import authentication


class CurrentUserField(Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'load_only': True
        })

        super().__init__(*args, **kwargs)

    def deserialize(self, value, attr=None, data=None, **kwargs):
        return authentication.get_account(self.context['request'])

    def serialize(self, attr, obj, accessor=None, **kwargs):
        raise NotImplementedError()
