import datetime

import jwt
from flask import current_app

from .. import bcrypt, db


class UserModel(db.Model):
    """
    User Model
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    # def __init__(self, data):
    #     self.email = data.get("email")
    #     self.first_name = data.get("first_name")
    #     self.last_name = data.get("last_name")
    #     self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return "<User {}>".format(self.username)

    def update(self, data):
        """
        :param data:
        :return: key.item
        """
        for key, item in data.items():
            setattr(self, key, item)

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                # fmt: off
                "exp": datetime.datetime.utcnow()
                       + datetime.timedelta(days=0, seconds=5),
                # fmt: on
                "iat": datetime.datetime.utcnow(),
                "sub": self.email,
            }
            return jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm="HS256",
            )
        except Exception as err:  # pylint: disable=broad-except
            return err

    @staticmethod
    def __hash_password(password):
        return bcrypt.generate_password_hash(password, rounds=10).decode(
            "utf-8"
        )

    def check_password(self, password):
        """
        Check user password
        :param password:
        :return: boolean | None
        """
        return bcrypt.check_password_hash(self.password, password)


role_permissions = db.Table(
    "role_permissions",
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permissions.id"),
        primary_key=True,
    ),
    db.Column(
        "role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True
    ),
)


class RoleModel(db.Model):
    """
    User Role Model
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    permissions = db.relationship(
        "PermissionModel", secondary=role_permissions
    )


class PermissionModel(db.Model):
    """
    User Permission Model
    """

    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, nullable=False)

    def __init__(self, title):
        self.title = title

    def save(self):
        """
        Save permission
        :return:
        """
        db.session.add(self)
        db.session.commit()
