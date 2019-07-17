
from colibris.schemas import ModelSchema
from colibris.schemas import fields, validate, pre_load

from __packagename__ import models


class UserSchema(ModelSchema):
    email = fields.String(validate=[validate.Email(error='Invalid email address.'),
                                    validate.Length(max=128)])

    @pre_load
    def process_input(self, data, **kwargs):
        data['email'] = data['email'].lower().strip()

        return data

    class Meta:
        model = models.User
        name = 'user'
        name_plural = 'users'