from marshmallow import fields, Schema, validate


class PermissionSchema(Schema):
    pass


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.String(validate=validate.Length(min=2))
    permissions = fields.List(fields.Nested(PermissionSchema))


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    first_name = fields.String(validate=validate.Length(min=2), dump_only=True)
    last_name = fields.String(validate=validate.Length(min=2), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Nested(RoleSchema(only=('id', 'title')))
