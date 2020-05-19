from flasgger import SwaggerView
from flask import Blueprint, jsonify, make_response, request

from webapp.utils.decorators import login_required, permissions

from .helpers.xls_csv_to_dict import csv_read, xls_read
from .models import ArticleModel
from .schemas import ArticleSchema
from .swagger_docstrings import file_upload_docstring


articles_blueprint = Blueprint("articles", __name__, url_prefix="/articles")


class ArticleAPI(SwaggerView):
    """
    Articles endpoints
    """

    responses = {
        200: {"description": "Article retrieved", "schema": ArticleSchema}
    }

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


class UploadFileAPI(SwaggerView):
    """
    Read xls/csv file
    """

    ALLOWED_EXTENSIONS = ["xls", "csv"]

    def post(self):  # pylint: disable=C0116
        file = request.files["file"]
        request.form.get("data")
        file_extension = file.filename.split(".")[-1]
        responseObject = {"status": "success", "message": "File uploaded."}
        if file_extension not in self.ALLOWED_EXTENSIONS:
            responseObject = {
                "status": "fail",
                "message": "Extension of file not allowed",
            }
            return make_response(jsonify(responseObject)), 400
        elif file_extension == "csv":
            csv_read(file)
            return make_response(jsonify(responseObject)), 200
        xls_read(file)
        return make_response(jsonify(responseObject)), 200


article_view = ArticleAPI.as_view("articles")
upload_view = UploadFileAPI.as_view("upload")
articles_blueprint.add_url_rule(
    "", defaults={"article_id": None}, view_func=article_view, methods=["GET"]
)
articles_blueprint.add_url_rule(
    "upload", view_func=upload_view, methods=["POST"]
)

UploadFileAPI.post.__doc__ = file_upload_docstring
