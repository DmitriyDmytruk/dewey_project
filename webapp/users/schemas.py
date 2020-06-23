from marshmallow import Schema, fields, validate


class PermissionSchema(Schema):
    """
    Permission schema
    """


class RoleSchema(Schema):
    """
    Role schema
    """

    id = fields.Int(dump_only=True)
    title = fields.String(validate=validate.Length(min=2))
    permissions = fields.List(fields.Nested(PermissionSchema), dump_only=True)


class UserSchema(Schema):
    """
    Base user schema
    """

    id = fields.Int(dump_only=True)
    email = fields.Email()
    first_name = fields.String(validate=validate.Length(min=2))
    last_name = fields.String(validate=validate.Length(min=2))
    password = fields.String(validate=validate.Length(min=8), load_only=True)
    created_at = fields.DateTime()
    role = fields.Nested(RoleSchema(only=("id", "title")))
