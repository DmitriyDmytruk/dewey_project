from . import articles_blueprint
from .views import ArticleAPI, ArticleSearchAPI, DownloadArticleXLS


article_view = ArticleAPI.as_view("articles")
articles_search_view = ArticleSearchAPI.as_view("articles-search")
download_article_view = DownloadArticleXLS.as_view("article-download")

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
