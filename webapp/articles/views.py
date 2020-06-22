from typing import Any, Dict, List

from flask import request
from flask.views import MethodView

from webapp import db
from webapp.utils.decorators import has_permissions, login_required

from .models import ArticleModel
from .schemas import ArticlePutPostSchema, ArticleSchema


class ArticleAPIView(MethodView):
    """
    Articles endpoints
    """

    @login_required
    @has_permissions(["can_view_articles"])
    def get(self, article_id: str = None) -> Dict[str, Any]:
        """
        Retrieve articles
        """
        if article_id is None:
            articles_schema = ArticleSchema(many=True)
            articles: List[ArticleModel] = ArticleModel.query.all()
            result = articles_schema.dump(articles)
            return {"articles": result, "message": "Articles retrieved"}
        return {}

    @login_required
    @has_permissions(["can_change_articles"])
    def put(self, article_id: int):
        """
        Article update
        """
        json_data: dict = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        article: ArticleModel = ArticleModel.query.filter(
            ArticleModel.id == article_id
        ).first()
        if not article:
            return {"message": "Article not found."}, 404
        try:
            ArticlePutPostSchema().load(
                data=json_data,
                instance=article,
                partial=True,
                session=db.session,
            )
            db.session.commit()
        except Exception as error:
            return {"message": str(error)}, 500
        return {"message": "Article updated"}
