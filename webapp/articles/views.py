from typing import IO, Any, Dict, List, Optional, Tuple, Union

from elasticsearch_dsl import Q, Search
from flask import Response, jsonify, make_response, request
from flask.views import MethodView

from webapp import db, es
from webapp.utils.decorators import login_required, permissions

from .helpers.export_to_xls import convert_to_xls
from .helpers.xls_csv_to_dict import CSVReader, XLSReader
from .models import ArticleModel
from .schemas import ArticlePutPostSchema, ArticleSchema


class ArticleAPIView(MethodView):
    """
    Articles endpoints
    """

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


class ArticleSearchAPIView(MethodView):
    """
    Search articles using ElasticSearch
    """

    @staticmethod
    def filter_create(queries: List[Q]) -> Q:
        """
        Creates Q.OR filter
        """
        query = queries.pop()
        for item in queries:
            query |= item
        return query

    @staticmethod
    def usable_items(found: list, items: str) -> List[str]:
        """
        Generates list of usable items
        """
        return sorted(
            list(
                set(
                    item
                    for article in found
                    for item in article["_source"][items]
                )
            )
        )

    @login_required
    @permissions(["can_view_articles"])
    def get(self) -> dict:
        data = request.get_json()
        categories = tags = state = None
        result = "Articles not found."
        if data:
            categories = data.get("categories")
            tags = data.get("tags")
            state = data.get("state")
        search = Search(using=es, index=ArticleModel.__tablename__)

        if not categories and not tags and not state:
            found = search.execute().to_dict()["hits"].get("hits")
            if found:
                result = [article["_source"] for article in found]
                usable_categories = self.usable_items(found, "categories")
                usable_tags = self.usable_items(found, "tags")
                return {
                    "response": result,
                    "categories": usable_categories,
                    "tags": usable_tags,
                    "states": sorted(
                        list(
                            set(
                                article["_source"]["state"]
                                for article in found
                            )
                        )
                    ),
                }
            return {"response": result}

        state_filter = categories_filter = tags_filter = Q()

        if state:
            state_filter = Q("match", state=state)

        if categories:
            queries = [Q("match", categories=value) for value in categories]
            categories_filter = self.filter_create(queries)

        if tags:
            queries = [Q("match", tags=value) for value in tags]
            tags_filter = categories_filter = self.filter_create(queries)

        combined_filter = state_filter & categories_filter & tags_filter
        found = (
            search.filter(combined_filter)
            .execute()
            .to_dict()["hits"]
            .get("hits")
        )

        if found:
            result = [article["_source"] for article in found]
        return {"response": result}


class DownloadArticleXLSView(MethodView):
    """
    Download article from database
    """

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
