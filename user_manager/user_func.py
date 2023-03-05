from marshmallow import post_load

from UserClass import UserSchema, UserDetails


class User(UserDetails):
    def __init__(self, name, mobile_no, city):
        super(User, self).__init__(name, mobile_no, city)

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class Userschema(UserSchema):
    @post_load
    def make_income(self, data, **kwargs):
        return User(**data)
