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
