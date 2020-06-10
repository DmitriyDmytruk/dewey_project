from . import articles_blueprint
from .views import ArticleAPI, DownloadArticleXLS


article_view = ArticleAPI.as_view("articles")

articles_blueprint.add_url_rule(
    "", defaults={"article_id": None}, view_func=article_view, methods=["GET"]
)
articles_blueprint.add_url_rule("", view_func=article_view, methods=["POST"])
articles_blueprint.add_url_rule(
    "<int:article_id>", view_func=article_view, methods=["PUT"]
)

download_article_view = DownloadArticleXLS.as_view("article")

articles_blueprint.add_url_rule(
    "/<int:article_id>/download",
    view_func=download_article_view,
    methods=["GET"],
)
