from marshmallow import Schema, fields, validate


class PermissionSchema(Schema):
    pass


class RoleSchema(Schema):
    id = fields.Int()
    title = fields.String(validate=validate.Length(min=2), required=True)
    permissions = fields.List(fields.Nested(PermissionSchema))


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email(required=True)
    first_name = fields.String(validate=validate.Length(min=2))
    last_name = fields.String(validate=validate.Length(min=2))
    created_at = fields.DateTime()
    role = fields.Nested(RoleSchema(only=('id', 'title')))
