from typing import IO, Any, Dict, List, Optional, Tuple, Union

from flask import Response, jsonify, request, make_response
from flask.views import MethodView

from webapp import db
from webapp.utils.decorators import login_required, permissions
from webapp.utils.error_responses import (
    acces_denied_response,
    login_failed_response,
)

from .helpers.export_to_xls import convert_to_xls
from .helpers.xls_csv_to_dict import CSVReader, XLSReader
from .models import ArticleModel
from .schemas import ArticlePutPostSchema, ArticleSchema


class ArticleAPIView(MethodView):
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
        ).first()
        if not article:
            return jsonify({"message": "Article does not exist."}), 404
        try:
            ArticlePutPostSchema().load(
                data=json_data,
                instance=article,
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


class UploadFileAPIView(MethodView):
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


class DownloadArticleXLSView(MethodView):
    """
    Download article from database
    """

    tags = ["articles"]

    @login_required
    @permissions(["can_view_articles"])
    def get(self, article_id: int) -> Union[Tuple[Dict[str, str], int], IO]:
        article: Optional[ArticleModel] = ArticleModel.query.filter_by(
            id=article_id
        ).one_or_none()
        if article:
            book = convert_to_xls(article)
            return Response(
                book,
                mimetype="application/vnd.ms-excel",
                headers={
                    "Content-disposition": f"attachment; filename={article.title}.xls"
                },
            )
        else:
            return jsonify({"message": "Article does not exist."}), 404
