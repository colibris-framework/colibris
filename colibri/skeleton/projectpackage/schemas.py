
from marshmallow import Schema
from marshmallow import fields, validate, pre_load, post_dump

#
# Schema example:
#
# class UserSchema(Schema):
#     id = fields.Integer(dump_only=True)
#     username = fields.String(required=True,
#                              validate=validate.Length(min=6, max=128))
#     first_name = fields.String(required=True,
#                                validate=validate.Length(max=64))
#     last_name = fields.String(required=True,
#                               validate=validate.Length(max=64))
#     email = fields.String(validate=[validate.Email(error='Invalid email address.'),
#                                     validate.Length(max=128)])
#
#     @pre_load
#     def process_input(self, data):
#         data['email'] = data['email'].lower().strip()
#
#         return data
#
#     @post_dump(pass_many=True)
#     def wrap(self, data, many):
#         key = 'users' if many else 'user'
#
#         return {
#             key: data
#         }
#
