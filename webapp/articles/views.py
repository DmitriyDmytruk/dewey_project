from flasgger import SwaggerView
from flask import Blueprint, redirect, url_for
from flask_login import login_required

from webapp import login_manager
from webapp.users.models import UserModel

from .models import ArticleModel
from .schemas import ArticleSchema


articles_blueprint = Blueprint("articles", __name__, url_prefix="/articles")


@login_manager.unauthorized_handler
def unauthorized_callback():
    """
    Redirect to login page
    """
    # TODO: Redirect to login page
    return redirect(url_for("login"))


# Maybe request_loader - https://flask-login.readthedocs.io/en/latest/#custom-login-using-request-loader
@login_manager.user_loader
def load_user(id):  # pylint: disable=redefined-builtin
    """
    Get user
    """
    u = UserModel.query.get(id)
    return u


class ArticleAPI(SwaggerView):
    """
    Articles endpoints
    """

    responses = {
        200: {"description": "Article retrieved", "schema": ArticleSchema}
    }

    @login_required
    def get(self, article_id):
        """
        Retrieve Articles list
        :param article_id:
        :return: ArticleSchema
        """
        if article_id is None:
            articles_schema = ArticleSchema(many=True)
            articles = ArticleModel.query.all()
            result = articles_schema.dump(articles)
            return {"articles": result}


article_view = ArticleAPI.as_view("articles")

articles_blueprint.add_url_rule(
    "", defaults={"article_id": None}, view_func=article_view, methods=["GET"]
)
