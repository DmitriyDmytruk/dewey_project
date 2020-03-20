import pytest

from webapp.users.models import PermissionModel, RoleModel, UserModel


@pytest.fixture(scope="module")
def create_new_permission():
    """
    Permission fixture
    """
    permission_title = "can_search_articles"
    permission = PermissionModel(permission_title)
    assert permission.title == permission_title
    return permission


def create_new_role(create_new_permission):
    """
    Test for Role create
    """
    role_title = "API User"
    role = RoleModel(title=role_title, permissions=[create_new_permission])
    assert role.title == role_title
    assert create_new_permission in role.permissions


def test_new_user():
    """
    Test for User create
    """
    new_user = UserModel(email="patkennedy79@gmail.com", is_active=False)
    assert new_user.email == "patkennedy79@gmail.com"
    assert not new_user.is_active
