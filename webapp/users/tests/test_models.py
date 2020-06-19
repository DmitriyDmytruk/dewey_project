from typing import Optional

import flask_bcrypt
import pytest
from sqlalchemy.exc import IntegrityError

from webapp.users.models import PermissionModel, RoleModel, UserModel


def test_create_new_role_permission(session):
    """
    Test for Role create
    """
    permission_title: str = "can_view_articles"
    role_title: str = "API User"
    permission: PermissionModel = PermissionModel(permission_title)
    role: RoleModel = RoleModel(title=role_title, permissions=[permission])
    session.add(role, permission)
    with pytest.raises(IntegrityError) as error:
        session.commit()
    assert error.typename == "IntegrityError"

    role_title: str = "Test User"
    permission: PermissionModel = PermissionModel(permission_title)
    role: RoleModel = RoleModel(title=role_title, permissions=[permission])
    session.add(role)
    assert role.title == role_title
    assert permission in role.permissions


def test_new_user(session):
    """
    Test for User create
    """
    role: RoleModel = session.query(RoleModel).filter_by(
        title="API User"
    ).one()

    password: str = "test_password"
    password_hash = flask_bcrypt.generate_password_hash(password).decode(
        "utf8"
    )
    user: UserModel = UserModel(
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

    user.encode_auth_token()

    check_password: Optional[bool]
    check_password = user.check_password(password)
    assert check_password
    check_password = user.check_password("some_password")
    assert not check_password


def test_delete_user(session):
    """
    Test for User delete
    """
    start_count: int = session.query(UserModel).count()
    user: UserModel = session.query(UserModel).first()
    session.delete(user)
    session.commit()
    assert start_count == UserModel.query.count() + 1


def test_delete_permission(session):
    """
    Test for Permission delete
    """
    start_count: int = session.query(PermissionModel).count()
    permission: PermissionModel = session.query(PermissionModel).first()
    session.delete(permission)
    session.commit()
    assert start_count == PermissionModel.query.count() + 1


def test_delete_role(session):
    """
    Test for Role delete
    """
    start_count: int = session.query(RoleModel).count()
    role: RoleModel = session.query(RoleModel).first()
    session.delete(role)
    session.commit()
    assert start_count == RoleModel.query.count() + 1


def test_update_user(session):
    """
    Test for User update
    """
    new_email: str = "update@gmail.com"
    user: UserModel = session.query(UserModel).first()
    user.email = new_email
    session.add(user)
    session.commit()
    assert user.email == new_email


def test_update_article(session):
    """
    Test for Permission update
    """
    new_title: str = "can_change"
    permission: PermissionModel = session.query(PermissionModel).first()
    permission.title = new_title
    session.add(permission)
    session.commit()
    assert permission.title == new_title


def test_update_role(session):
    """
    Test for Role update
    """
    new_title: str = "User"
    role: RoleModel = session.query(RoleModel).first()
    role.title = new_title
    session.add(role)
    session.commit()
    assert role.title == new_title
