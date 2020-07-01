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
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PG_HOST = os.environ.get("PG_HOST", "db")
    PG_PORT = 5432
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://dewey_user:dditeam@{PG_HOST}:{PG_PORT}/dewey_db"
    )
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class TestConfig(Config):
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
    TESTDB = "test.db"
    TESTDB_PATH = os.path.join(basedir, TESTDB)
    TEST_DATABASE_URI = "sqlite:///" + TESTDB_PATH
    SECRET_KEY = "SECRET-KEY"
    SERVER_NAME = "localhost"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
