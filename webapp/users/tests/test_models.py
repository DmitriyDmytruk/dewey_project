import flask_bcrypt

from webapp.users.models import PermissionModel, RoleModel, UserModel


def test_create_new_role_permission(session):
    """
    Test for Role create
    """
    permission_title = "can_search_articles"
    role_title = "API User"
    permission = PermissionModel(permission_title)
    role = RoleModel(title=role_title, permissions=[permission])
    session.add(role)
    session.commit()
    assert role.title == role_title
    assert permission in role.permissions


def test_new_user(session):
    """
    Test for User create
    """
    role_title = "API User"
    role = RoleModel(title=role_title)
    session.add(role)
    session.commit()

    password = "test_password"

    password_hash = flask_bcrypt.generate_password_hash(password).decode(
        "utf8"
    )
    user = UserModel(
        email="patkennedy79@gmail.com",
        is_active=False,
        role_id=role.id,
        password=password_hash,
    )
    session.add(user)
    session.commit()

    assert user.email == "patkennedy79@gmail.com"
    assert not user.is_active
    assert user.role_id == role.id

    token = user.encode_auth_token()

    check_password = user.check_password(password)
    assert check_password

    check_password = user.check_password('some_password')
    assert not check_password


# def test_hash_password()
#
#     bcrypt.generate_password_hash(password, rounds=10).decode(
#         "utf-8"
#     )
