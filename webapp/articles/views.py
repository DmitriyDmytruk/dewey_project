from typing import Any, Dict, List

from flasgger import SwaggerView
from flask import jsonify, request

from webapp import db
from webapp.utils.decorators import login_required, permissions

from .models import ArticleModel, CategoryModel, TagModel
from .schemas import ArticlePutPostSchema, ArticleSchema


class ArticleAPI(SwaggerView):
    """
    Articles endpoints
    """

    # schemes = [ArticleSchema]
    responses = {
        200: {"description": "Article retrieved", "schema": ArticleSchema}
    }
    tags = ["articles"]
    definitions = {
        "ArticleSchema": ArticleSchema,
        "ArticlePutPostSchema": ArticlePutPostSchema,
    }

    # @login_required
    # @permissions(["can_search_articles"])
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

    # @login_required
    # @permissions(["can_edit_articles"])
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
                  default: Article updated.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "Invalid request"}), 400
        data = ArticlePutPostSchema().load(data=json_data, partial=True)
        data["categories"] = list(
            CategoryModel.query.filter(
                CategoryModel.id.in_(data["categories"])
            )
        )
        data["tags"] = list(
            TagModel.query.filter(TagModel.id.in_(data["tags"]))
        )

        article = ArticleModel.query.filter(
            ArticleModel.id == article_id
        ).first_or_404()
        for k, v in data.items():
            setattr(article, k, v)
        db.session.commit()
        return jsonify(), 200

    @login_required
    @permissions(["can_create_articles"])
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
              id: Successful
              properties:
                message:
                  type: string
                  default: Article created.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "Invalid request"}), 400
        data = ArticlePutPostSchema().load(data=json_data, partial=True)
        data["categories"] = list(
            CategoryModel.query.filter(
                CategoryModel.id.in_(data["categories"])
            )
        )
        data["tags"] = list(
            TagModel.query.filter(TagModel.id.in_(data["tags"]))
        )
        article = ArticleModel(**data)
        db.session.add(article)
        db.session.commit()

        return jsonify(), 200
