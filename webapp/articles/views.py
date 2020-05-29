from typing import Any, Dict, List

from flasgger import SwaggerView
from flask import jsonify, request

from webapp import db
from webapp.utils.decorators import login_required, permissions

from .models import ArticleModel
from .schemas import ArticlePutPostSchema, ArticleSchema


class ArticleAPI(SwaggerView):
    """
    Articles endpoints
    """

    tags = ["articles"]
    definitions = {
        "ArticleSchema": ArticleSchema,
        "ArticlePutPostSchema": ArticlePutPostSchema,
    }

    @login_required
    @permissions(["can_search_articles"])
    def get(self, article_id: str = None) -> Dict[str, Any]:
        """
        Retrieve Articles list
        :param article_id:str
        :return: ArticleSchema
        """
        if article_id is None:
            articles_schema = ArticleSchema(many=True)
            articles: List[ArticleModel] = ArticleModel.query.all()
            result = articles_schema.dump(articles)
            return {"articles": result}

    @login_required
    @permissions(["can_change_articles"])
    def put(self, article_id: str):
        """
        Update article
        ---
        parameters:
          - in: body
            name: data
            schema:
              $ref: '#/definitions/ArticlePutPostSchema'
          - in: path
            name: article_id
            type: string
            required: true
        responses:
          200:
            description: Article updated
            schema:
              id: Successful
              properties:
                message:
                  type: string
                  default: Article updated
          400:
            description: Invalid request
            schema:
              id: Invalid
              properties:
                message:
                  type: string
                  default: Invalid request
          404:
            description: Not exist
            schema:
              id: NotExist
              properties:
                message:
                  type: string
                  default: Article does not exist.
          500:
            description: Fail
            schema:
              id: Fail
              properties:
                message:
                  type: string
        """
        json_data: dict = request.get_json()
        if not json_data:
            return jsonify({"message": "Invalid request"}), 400
        article: ArticleModel = ArticleModel.query.filter(
            ArticleModel.id == article_id
        )
        if not article:
            return jsonify({"message": "Article does not exist."}), 404
        try:
            ArticlePutPostSchema().load(
                data=json_data,
                instance=article.first(),
                partial=True,
                session=db.session,
            )
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        return jsonify({"message": "Article updated"}), 200

    @login_required
    @permissions(["can_add_articles"])
    def post(self):
        """
        Create article
        ---
        parameters:
          - in: body
            name: data
            schema:
              $ref: '#/definitions/ArticlePutPostSchema'
        responses:
          200:
            description: Article created
            schema:
              id: Successful created
              properties:
                message:
                  type: string
                  default: Article created.
                id:
                  type: integer
          400:
            description: Invalid request
            schema:
              id: Invalid
              properties:
                message:
                  type: string
                  default: Invalid request
          500:
            description: Fail
            schema:
              id: Fail
              properties:
                message:
                  type: string
        """
        json_data: dict = request.get_json()
        if not json_data:
            return jsonify({"message": "Invalid request"}), 400
        try:
            article: ArticleModel = ArticlePutPostSchema().load(
                data=json_data, partial=True, session=db.session
            )
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        return jsonify({"message": "Article created", "id": article.id}), 200
