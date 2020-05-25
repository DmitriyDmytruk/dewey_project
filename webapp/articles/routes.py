from . import articles_blueprint
from .views import ArticleAPI, UploadFileAPI


article_view = ArticleAPI.as_view("articles")
articles_blueprint.add_url_rule(
    "", defaults={"article_id": None}, view_func=article_view, methods=["GET"]
)

upload_view = UploadFileAPI.as_view("")
articles_blueprint.add_url_rule(
    "upload", view_func=upload_view, methods=["POST"],
)
