from . import articles_blueprint
from .views import ArticleAPI, ArticleSearchAPIView, DownloadArticleXLS, UploadFileAPIView


article_view = ArticleAPIView.as_view("articles")
articles_search_view = ArticleSearchAPIView.as_view("articles-search")
download_article_view = DownloadArticleXLSView.as_view("article")
upload_view = UploadFileAPIView.as_view("upload")

articles_blueprint.add_url_rule(
    "", defaults={"article_id": None}, view_func=article_view, methods=["GET"]
)
articles_blueprint.add_url_rule("", view_func=article_view, methods=["POST"])
articles_blueprint.add_url_rule(
    "<int:article_id>", view_func=article_view, methods=["PUT"]
)
articles_blueprint.add_url_rule(
    "search", view_func=articles_search_view, methods=["GET"]
)
articles_blueprint.add_url_rule(
    "/<int:article_id>/download",
    view_func=download_article_view,
    methods=["GET"],
)
articles_blueprint.add_url_rule(
    "upload", view_func=upload_view, methods=["POST"],
)
