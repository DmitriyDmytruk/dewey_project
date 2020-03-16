from marshmallow import fields, Schema, validate

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    first_name = fields.String(validate=validate.Length(min=2))
    last_name = fields.String(validate=validate.Length(min=2))
    created_at = fields.DateTime()
    role = fields.Nested(RoleSchema(only=("id", "title")))


class RoleSchema(Schema):
    id = fields.Int()
    title = fields.String(validate=validate.Length(min=2))
    permissions = fields.List(fields.Nested(PermissionSchema))


class PermissionSchema(Schema):
    pass