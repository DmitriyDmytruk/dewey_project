from typing import Any, Dict, List

from flasgger import SwaggerView
from flask import jsonify, make_response, request

from webapp.utils.decorators import login_required, permissions

from .helpers.xls_csv_to_dict import CSVReader, XLSReader
from .models import ArticleModel
from .schemas import ArticleSchema
from .swagger_docstrings import file_upload_docstring


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
            CSVReader().to_dict(file)
            return make_response(jsonify(responseObject)), 200
        XLSReader().to_dict(file)
        return make_response(jsonify(responseObject)), 200


UploadFileAPI.post.__doc__ = file_upload_docstring
