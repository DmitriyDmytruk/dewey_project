from typing import Any, Dict, List

from flasgger import SwaggerView
from flask import jsonify, make_response, request

from webapp import db
from webapp.utils.decorators import login_required, permissions
from webapp.utils.error_responses import (
    acces_denied_response,
    login_failed_response,
)

from .helpers.xls_csv_to_dict import CSVReader, XLSReader
from .models import ArticleModel
from .schemas import ArticlePutPostSchema, ArticleSchema
from .swagger_docstrings import (
    article_create_docstring,
    article_update_docstring,
    articles_retrieve_docstring,
    file_upload_docstring,
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
    @permissions(["can_view_articles"])
    def get(self, article_id: str) -> Dict[str, Any]:
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


class UploadFileAPI(SwaggerView):
    """
    Read xls/csv file
    """

    ALLOWED_EXTENSIONS = ["xls", "csv"]

    @login_required
    @permissions(["can_view_articles"])
    def post(self):
        """
        xls/csv file upload
        """
        file = request.files["file"]
        request.form.get("data")
        file_extension = file.filename.split(".")[-1]
        response = {"status": "success", "message": "File uploaded."}
        if file_extension not in self.ALLOWED_EXTENSIONS:
            response = {
                "status": "fail",
                "message": "Extension of file not allowed",
            }
            return make_response(jsonify(response)), 400
        elif file_extension == "csv":
            CSVReader().to_dict(file)
            return make_response(jsonify(response)), 200
        XLSReader().to_dict(file)
        return make_response(jsonify(response)), 200


ArticleAPI.get.__doc__ = articles_retrieve_docstring
ArticleAPI.put.__doc__ = article_update_docstring
ArticleAPI.post.__doc__ = article_create_docstring
UploadFileAPI.post.__doc__ = file_upload_docstring
