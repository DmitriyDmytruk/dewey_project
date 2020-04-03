from webapp.users.models import RoleModel, UserModel
from webapp.users.schemas import RoleSchema, UserSchema


def test_role_shema(session):
    """
    Testing [de]serialization with RoleSchema
    """
    role_data = {"title": "API User", "permissions": [], "id": 1}
    data = RoleSchema().load(role_data)
    assert data.get("title") == role_data.get("title")

    role = session.query(RoleModel).filter_by(title="API User").one()
    data = RoleSchema().dump(role)
    assert data.get("title") == role.title


def test_user_shema(session):
    """
    Testing [de]serialization with UserSchema
    """
    role = session.query(RoleModel).filter_by(title="API User").one()
    user_data = {
        "email": "test@mail.com",
        "role": RoleSchema(only=["id", "title"]).dump(role),
    }
    data = UserSchema().load(user_data)
    assert data.get("email") == user_data.get("email")
    assert data["role"].get("title") == "API User"

    user = session.query(UserModel).filter_by(email="test@gmail.com").one()
    data = UserSchema().dump(user)
    assert data.get("email") == user.email
