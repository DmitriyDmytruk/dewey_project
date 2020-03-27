import os

import pytest

from config import basedir
from webapp import create_app
from webapp import db as _db
from webapp.users.models import PermissionModel, RoleModel, UserModel


TESTDB = "test.db"
TESTDB_PATH = os.path.join(basedir, TESTDB)


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app("config.TestConfig")

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

    permission = PermissionModel(title="can_search_articles")
    role = RoleModel(title="API User", permissions=[permission])
    _db.session.add_all([role, permission])
    _db.session.commit()

    user1 = UserModel(email="test@gmail.com", role_id=role.id)
    user2 = UserModel(email="test2@gmail.com")
    _db.session.add_all([user1, user2])

    _db.session.commit()

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
