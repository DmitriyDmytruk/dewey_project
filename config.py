import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    pass


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "database.db"
    )


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://dewey_user:dditeam@localhost/dewey_db"
    )


class TestConfig(Config):
    TESTDB = "test.db"
    TESTDB_PATH = os.path.join(basedir, TESTDB)
    TEST_DATABASE_URI = "sqlite:///" + TESTDB_PATH
    SECRET_KEY = "SECRET-KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
