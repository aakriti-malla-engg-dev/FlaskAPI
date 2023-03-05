from marshmallow import Schema, fields


class UserDetails(object):
    def __init__(self, name, mobile_no, city):
        self.name = name
        self.mobile_no = mobile_no
        self.city = city

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class UserSchema(Schema):
    name = fields.Str()
    mobile = fields.Str()
    city = fields.Str()
