import os

import connexion
from connexion.resolver import MethodViewResolver
from elasticsearch import Elasticsearch
from flask import Blueprint, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
es = Elasticsearch()
session = Session()


def add_api(app: connexion.FlaskApp) -> connexion.FlaskApp:
    """
    Adding swagger specification files
    Endpoint CBV must end on "View"
    https://github.com/zalando/connexion/blob/master/examples/openapi3/methodresolver/app.py
    """
    app.add_api(
        "swagger.yml",
        resolver=MethodViewResolver("api"),
        strict_validation=True,
    )
    app.add_api(
        "swagger_articles.yml",
        resolver=MethodViewResolver("api"),
        strict_validation=True,
    )
    app.add_api(
        "swagger_users.yml",
        resolver=MethodViewResolver("api"),
        strict_validation=True,
    )
    return app


def redoc_initial(app: connexion.FlaskApp) -> Blueprint:
    """
    Inital ReDoc documentation on the `/redoc/` url
    https://github.com/zalando/connexion/issues/774#issuecomment-623877267
    """
    redoc_blueprint = Blueprint(
        "docs",
        __name__,
        url_prefix="/redoc",
        template_folder=os.path.dirname(__file__),
    )
    spec_path = "/redoc" + app.options.openapi_spec_path
    serve_redoc = lambda: render_template(
        "redoc.j2", openapi_spec_url=spec_path
    )
    redoc_blueprint.add_url_rule("/", __name__, serve_redoc)
    return redoc_blueprint


def create_app(object_name: str):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/")
    add_api(connexion_app)
    redoc_blueprint = redoc_initial(connexion_app)

    app = connexion_app.app
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
    session.init_app(app)

    from webapp.articles.routes import articles_blueprint
    from webapp.core.routes import base_blueprint
    from webapp.users.routes import users_blueprint

    app.register_blueprint(articles_blueprint)
    app.register_blueprint(base_blueprint)
    app.register_blueprint(redoc_blueprint)
    app.register_blueprint(users_blueprint)

    return app
