from . import users_blueprint
from .views import LoginAPIView, UserAPIView


login_view = LoginAPIView.as_view("login")
users_blueprint.add_url_rule("login", view_func=login_view, methods=["POST"])

user_view = UserAPIView.as_view("users")

users_blueprint.add_url_rule(
    "", defaults={"user_id": None}, view_func=user_view, methods=["GET"]
)
users_blueprint.add_url_rule("", view_func=user_view, methods=["POST"])
users_blueprint.add_url_rule(
    "<int:user_id>", view_func=user_view, methods=["GET", "PUT", "DELETE"]
)
