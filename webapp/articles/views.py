from typing import IO, Any, Dict, List, Optional, Tuple, Union

from flask import Response, current_app, request
from flask.views import MethodView

from webapp import db, es
from webapp.utils.decorators import has_permissions, login_required

from .helpers.export_to_xls import convert_to_xls
from .helpers.xls_csv_to_dict import CSVReader, XLSReader
from .models import ArticleModel, CategoryModel, TagModel
from .schemas import article_put_post_schema, articles_list_schema


class ArticleAPIView(MethodView):
    """Articles endpoints"""

    @login_required
    @has_permissions(["can_view_articles"])
    def get(self, article_id: str = None) -> Dict[str, Any]:
        """Retrieve articles"""
        if article_id is None:
            articles: List[ArticleModel] = ArticleModel.query.all()
            result = articles_list_schema.dump(articles)
            return {"articles": result, "message": "Articles retrieved"}
        return {}

    @login_required
    @has_permissions(["can_change_articles"])
    def put(self, article_id: int):
        """Article update"""
        json_data: dict = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        article: ArticleModel = ArticleModel.query.filter(
            ArticleModel.id == article_id
        ).first()
        if not article:
            return {"message": "Article not found."}, 404
        try:
            article_put_post_schema.load(
                data=json_data,
                instance=article,
                partial=True,
                session=db.session,
            )
            db.session.commit()
        except Exception as error:
            current_app.logger.error(error, exc_info=True)
            return {"message": str(error)}, 500
        return {"message": "Article updated"}

    @login_required
    @has_permissions(["can_add_articles"])
    def post(self):
        """Article create"""
        json_data: dict = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            article: ArticleModel = article_put_post_schema.load(
                data=json_data, partial=True, session=db.session
            )
            db.session.add(article)
            db.session.commit()
        except Exception as error:
            current_app.logger.error(error, exc_info=True)
            return {"message": str(error)}, 500
        return {"message": "Article created", "id": article.id}, 201


class ArticleSearchAPIView(MethodView):
    """Search articles using ElasticSearch"""

    @staticmethod
    def _usable_items(found: list, items: str) -> List[str]:
        """
        Generates list of usable items
        @param found: list
        @param items: str
        @return: list
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

    @staticmethod
    def _forming_query(
        state: Optional[str] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """
        Forming query for elasticsearch
        @param state: string | None
        @param categories: list | None
        @param tags: list | None
        @return: dict
        """
        query = {"bool": {"must": []}}
        if state:
            query["bool"]["must"].append({"term": {"state.keyword": state}})
        if categories:
            query["bool"]["must"].append(
                {"terms": {"categories.keyword": categories}}
            )
        if tags:
            query["bool"]["must"].append({"terms": {"tags.keyword": tags}})
        return query

    @staticmethod
    def _retrieve_articles(
        query: Optional[dict] = None, match_all: bool = False
    ) -> List:
        """
        Retrieve articles from request to elasticsearch
        @param query: dict | None
        @param match_all: bool
        @return: list
        """
        if match_all:
            query = {"match_all": {}}
        found = es.search(
            index=ArticleModel.__tablename__, body={"query": query},
        )["hits"].get("hits")

        return found

    @login_required
    @has_permissions(["can_view_articles"])
    def get(
        self,
    ) -> Union[
        Dict[str, Union[list, List[str]]],
        Tuple[Dict[str, str], int],
        Dict[str, Union[list, str]],
    ]:
        """
        Search article
        First request - with empty params
        """
        data = request.get_json()
        categories = tags = state = None
        result = "Articles not found."
        if data:
            categories = data.get("categories")
            tags = data.get("tags")
            state = data.get("state")

        if not categories and not tags and not state:
            found = self._retrieve_articles(match_all=True)
            if found:
                result = [article["_source"] for article in found]
                usable_categories = self._usable_items(found, "categories")
                usable_tags = self._usable_items(found, "tags")
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
            return {"response": result}, 404

        query = self._forming_query(state, categories, tags)
        found = self._retrieve_articles(query)
        if found:
            result = [article["_source"] for article in found]
        return {"response": result}


class DownloadArticleXLSView(MethodView):
    """Download article from database"""

    @login_required
    @has_permissions(["can_view_articles"])
    def get(self, article_id: int) -> Union[Tuple[Dict[str, str], int], IO]:
        """Converts exist article to .xls file"""
        article: Optional[ArticleModel] = ArticleModel.query.filter_by(
            id=article_id
        ).one_or_none()
        if article:
            book = convert_to_xls(article)
            return Response(
                book,
                mimetype="application/vnd.ms-excel",
                headers={
                    "Content-disposition": f"attachment; filename={article.title}.xls"  # pylint: disable
                },
            )
        return {"message": "Article not found."}, 404


class UploadFileAPIView(MethodView):
    """Read xls/csv file"""

    ALLOWED_EXTENSIONS = ["xls", "csv"]

    @login_required
    @has_permissions(["can_view_articles"])
    def post(self):
        """xls/csv file upload for article create"""
        file = request.files["file"]
        # request.form.get("data")
        file_extension = file.filename.split(".")[-1]
        response = {"status": "Successful", "message": "File uploaded."}

        if file_extension not in self.ALLOWED_EXTENSIONS:
            return (
                {
                    "status": "Failed",
                    "message": "Extension of file not allowed",
                },
                400,
            )
        if file_extension == "csv":
            data = CSVReader().to_dict(file)
        else:
            data = XLSReader().to_dict(file)

        for ind, article_data in enumerate(data):
            categories_list = []
            if article_data["categories"]:
                for category_data in article_data["categories"]:
                    category = CategoryModel.query.filter_by(
                        name=category_data["name"]
                    ).first()
                    if not category:
                        category = CategoryModel(name=category_data["name"])
                        db.session.add(category)
                        db.session.commit()
                    categories_list.append(category)
            article_data["categories"] = categories_list

            tags_list = []
            if article_data["tags"]:
                for tag_data in article_data["tags"]:
                    tag = TagModel.query.filter_by(
                        name=tag_data["name"]
                    ).first()
                    if not tag:
                        tag = TagModel(name=tag_data["name"])
                        db.session.add(tag)
                        db.session.commit()
                    tags_list.append(tag)
            article_data["tags"] = tags_list
            article_data["title"] = f"Article {ind}"
            article = ArticleModel(**article_data)
            db.session.add(article)
            db.session.commit()
        return response
