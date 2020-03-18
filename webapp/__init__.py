from flasgger import Swagger
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(object_name)

    from webapp.users import models  # pylint: disable=unused-import

    db.init_app(app)
    migrate.init_app(app, db)

    Swagger(app)

    from .users.views import users_blueprint
    from .auth.views import auth_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

from .users import models
