from typing import Dict, Union

from webapp.users.models import RoleModel, UserModel
from webapp.users.schemas import (
    role_schema,
    role_schema_only_title,
    user_schema,
)


def test_role_shema(session):
    """
    Testing [de]serialization with RoleSchema
    """
    role_data: Dict[str, Union[str, list, int]] = {
        "title": "API User",
    }
    data = role_schema.load(role_data)
    assert data.get("title") == role_data.get("title")

    role = session.query(RoleModel).filter_by(title="API User").one()
    data = role_schema.dump(role)
    assert data.get("title") == role.title


def test_user_shema(session):
    """
    Testing [de]serialization with UserSchema
    """
    role: RoleModel = session.query(RoleModel).filter_by(
        title="API User"
    ).one()
    user_data: Dict[str, Union[str, dict]] = {
        "email": "test@mail.com",
        "role": role_schema_only_title.dump(role),
    }
    data = user_schema.load(user_data)
    assert data.get("email") == user_data.get("email")
    assert data["role"].get("title") == "API User"

    user: UserModel = session.query(UserModel).filter_by(
        email="test@gmail.com"
    ).one()
    data = user_schema.dump(user)
    assert data.get("email") == user.email
