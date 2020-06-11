import connexion
from connexion.resolver import MethodViewResolver
from flasgger import Swagger
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_session import Session


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
swagger = Swagger()
es = Elasticsearch()
session = Session()


def create_app(object_name: str):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = connexion.FlaskApp(__name__, specification_dir="openapi/")
    app.add_api(
        "swagger.yml",
        resolver=MethodViewResolver("api"),
        strict_validation=True,
    )
    app.add_api(
        "swagger_users.yml",
        resolver=MethodViewResolver("api"),
        strict_validation=True,
    )
    app = app.app
    app.config.from_object(object_name)
    app.secret_key = app.config["SECRET_KEY"]
    app.config["SESSION_TYPE"] = "filesystem"
    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)
    session.init_app(app)

    from .core.routes import base_blueprint
    from .users.routes import users_blueprint
    from .articles.routes import articles_blueprint

    app.register_blueprint(base_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(articles_blueprint)

    return app


from .users import models  # pylint: disable=wrong-import-position
from .articles import models  # pylint: disable=wrong-import-position
