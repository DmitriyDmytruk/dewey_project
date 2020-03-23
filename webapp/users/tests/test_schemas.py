from webapp.users.models import RoleModel, UserModel
from webapp.users.schemas import RoleSchema, UserSchema


def test_role_shema(session):
    """
    Testing [de]serialization with RoleSchema
    """
    role_data = {"title": "API User", "permissions": [], "id": 1}
    data = RoleSchema().load(role_data)
    assert data.get("title") == role_data.get("title")

    role = RoleModel(title="API User", permissions=[])
    data = RoleSchema().dump(role)
    assert data.get("title") == role.title


def test_user_shema(session):
    """
    Testing [de]serialization with UserSchema
    """
    user_data = {
        "email": "test@mail.com",
        "role": RoleSchema().load({"title": "API User", "id": 1}),
    }
    data = UserSchema().load(user_data)
    assert data.get("email") == user_data.get("email")
    assert data["role"].get("title") == "API User"

    user = UserModel(email="test@mail.com")
    data = UserSchema().dump(user)
    assert data.get("email") == user.email
