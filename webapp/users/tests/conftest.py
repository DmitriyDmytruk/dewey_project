import os

import pytest

from config import basedir
from webapp import create_app, db
from webapp.users.models import PermissionModel, RoleModel, UserModel


TESTDB = "test.db"
TESTDB_PATH = os.path.join(basedir, TESTDB)


def prepare_data(session):
    permission: PermissionModel = PermissionModel(title="can_view_articles")
    role: RoleModel = RoleModel(title="API User", permissions=[permission])
    session.add_all([role, permission])
    session.commit()

    user1: UserModel = UserModel(email="test@gmail.com", role_id=role.id)
    user2: UserModel = UserModel(email="test2@gmail.com")
    session.add_all([user1, user2])

    session.commit()


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app("config.TestConfig")
    with app.app_context() as ctx:
        ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def session(app):
    """Creates a new database session for a test."""
    db.app = app
    db.create_all()

    with db.engine.connect() as connection:
        with connection.begin() as transaction:
            options = dict(bind=connection, binds={})
            session = db.create_scoped_session(options=options)
            db.session = session
            prepare_data(session)

        yield session

        transaction.rollback()
        db.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context() as ctx:
            ctx.push()
        yield client
    ctx.pop()
