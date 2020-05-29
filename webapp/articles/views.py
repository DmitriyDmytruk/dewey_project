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

    responses = {
        200: {"description": "Article retrieved", "schema": ArticleSchema}
    }
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
                  default: Article updated.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "Invalid request"}), 400
        ArticlePutPostSchema().load(
            data=json_data,
            instance=ArticleModel.query.filter(
                ArticleModel.id == article_id
            ).first_or_404(),
            partial=True,
            session=db.session,
        )
        db.session.commit()
        return jsonify(), 200

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
              id: Successful
              properties:
                message:
                  type: string
                  default: Article created.
        """
        json_data = request.get_json()
        print(json_data)
        if not json_data:
            return jsonify({"message": "Invalid request"}), 400
        article = ArticlePutPostSchema().load(
            data=json_data, partial=True, session=db.session
        )
        db.session.add(article)
        db.session.commit()

        return jsonify(), 200
