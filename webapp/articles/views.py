from flasgger import SwaggerView
from flask import Blueprint

from webapp.utils.decorators import login_required

from .models import ArticleModel
from .schemas import ArticleSchema


articles_blueprint = Blueprint("articles", __name__, url_prefix="/articles")


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
