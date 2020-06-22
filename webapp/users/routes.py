from . import users_blueprint
from .views import LoginAPIView


login_view = LoginAPIView.as_view("login")
users_blueprint.add_url_rule("login", view_func=login_view, methods=["POST"])
