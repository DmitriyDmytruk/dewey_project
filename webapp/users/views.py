from flask import Blueprint
from flask.views import MethodView

users_blueprint = Blueprint('users', __name__, url_prefix="/users")


class UserAPI(MethodView):

    def get(self, user_id):
        if user_id is None:
            # list view
            pass
        else:
            # detail view
            pass

    def post(self):
        # create view
        pass

    def delete(self, user_id):
        pass

    def put(self, user_id):
        pass

user_view = UserAPI.as_view()