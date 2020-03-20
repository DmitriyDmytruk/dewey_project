import os

import pytest

from config import basedir
from webapp import create_app
from webapp import db as _db
from webapp.users.models import PermissionModel, RoleModel, UserModel


TESTDB = "test.db"
TESTDB_PATH = os.path.join(basedir, TESTDB)
TEST_DATABASE_URI = "sqlite:///" + TESTDB_PATH


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
    }
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        try:
            os.unlink(TESTDB_PATH)
        except FileNotFoundError:
            pass

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


def test_new_permission(session):
    """
    Permission fixture
    """
    permission_title = "can_search_articles"
    permission = PermissionModel(permission_title)
    session.add(permission)
    session.commit()

    assert permission.title == permission_title


def test_create_new_role(session):
    """
    Test for Role create
    """
    role_title = "API User"
    role = RoleModel(title=role_title, permissions=[])
    session.add(role)
    session.commit()
    assert role.title == role_title
    assert False


def test_new_user():
    """
    Test for User create
    """
    new_user = UserModel(email="patkennedy79@gmail.com", is_active=False)

    assert new_user.email == "patkennedy79@gmail.com"
    assert not new_user.is_active
