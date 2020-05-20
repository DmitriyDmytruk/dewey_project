from flasgger import SwaggerView

from webapp.utils.decorators import login_required, permissions

from .models import ArticleModel
from .schemas import ArticleSchema


class ArticleAPI(SwaggerView):
    """
    Articles endpoints
    """

    responses = {
        200: {"description": "Article retrieved", "schema": ArticleSchema}
    }
    tags = ["articles"]

    @login_required
    @permissions(["can_search_articles"])
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
