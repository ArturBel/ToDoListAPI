from .extensions import ma
from marshmallow import fields
from .models import User, Todo
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)


class TodoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True
        include_fk = True
    
    owner = fields.Nested(UserSchema, dump_only=True)