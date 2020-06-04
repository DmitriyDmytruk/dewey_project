from typing import IO, Any, Dict, List, Optional, Tuple, Union

from flasgger import SwaggerView
from flask import Response, jsonify

from webapp.utils.decorators import login_required, permissions

from .helpers.export_to_xls import convert_to_xls
from .models import ArticleModel
from .schemas import ArticleSchema


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
