from . import articles_blueprint
from .views import ArticleAPIView


article_view = ArticleAPIView.as_view("articles")

articles_blueprint.add_url_rule(
    "", defaults={"article_id": None}, view_func=article_view, methods=["GET"]
)
articles_blueprint.add_url_rule("", view_func=article_view, methods=["POST"])
articles_blueprint.add_url_rule(
    "<int:article_id>", view_func=article_view, methods=["PUT"]
)
