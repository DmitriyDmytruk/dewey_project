from typing import IO, Any, Dict, List, Optional, Tuple, Union

from flasgger import SwaggerView
from flask import jsonify, request
from flask import Response, jsonify

from webapp import db
from webapp.utils.decorators import login_required, permissions
from webapp.utils.error_responses import (
    acces_denied_response,
    login_failed_response,
)

from .helpers.export_to_xls import convert_to_xls
from .models import ArticleModel
from .schemas import ArticlePutPostSchema, ArticleSchema
from .swagger_docstrings import (
    article_create_docstring,
    article_update_docstring,
    articles_retrieve_docstring,
)


class ArticleAPI(SwaggerView):
    """
    Articles endpoints
    """

    tags = ["articles"]
    definitions = {
        "ArticleSchema": ArticleSchema,
        "ArticlePutPostSchema": ArticlePutPostSchema,
    }
    responses = {401: login_failed_response, 403: acces_denied_response}

    @login_required
    @permissions(["can_search_articles"])
    def get(self, article_id: str = None) -> Dict[str, Any]:
        if article_id is None:
            articles_schema = ArticleSchema(many=True)
            articles: List[ArticleModel] = ArticleModel.query.all()
            result = articles_schema.dump(articles)
            return {"articles": result}

    @login_required
    @permissions(["can_change_articles"])
    def put(self, article_id: str):
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


ArticleAPI.get.__doc__ = articles_retrieve_docstring
ArticleAPI.put.__doc__ = article_update_docstring
ArticleAPI.post.__doc__ = article_create_docstring


class DownloadArticleXLS(SwaggerView):
    """
    Download article from database
    """

    responses = {200: {"download_link": ""}}
    tags = ["articles"]

    def get(self, article_id: int) -> Union[Tuple[Dict[str, str], int], IO]:
        """
        Download article
        ---
        parameters:
          - in: path
            name: article_id
            type: string
            required: true
        responses:
          200:
            description: Download file
            schema:
              id: Successful
              properties:
                file:
                  type: file
                  description: .xls file
          404:
            description: Not exist
            schema:
              id: NotExist
              properties:
                message:
                  type: string
                  default: Article does not exist.
        """
        article: Optional[ArticleModel] = ArticleModel.query.filter_by(
            id=article_id
        ).one_or_none()
        if article:
            book = convert_to_xls(article)
            print(type(book))
            return Response(
                book,
                mimetype="application/vnd.ms-excel",
                headers={
                    "Content-disposition": f"attachment; filename={article.title}.xls"
                },
            )
        else:
            return jsonify({"message": "Article does not exist."}), 404
