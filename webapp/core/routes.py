from . import base_blueprint
from .views import index


base_blueprint.add_url_rule("/", view_func=index, methods=["GET"])
