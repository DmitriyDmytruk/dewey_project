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
        """
        """

    def delete(self, user_id):
        pass

    def put(self, user_id):
        pass


user_view = UserAPI.as_view('users')

users_blueprint.add_url_rule('', defaults={'user_id': None},
                 view_func=user_view, methods=['GET'])
users_blueprint.add_url_rule('', view_func=user_view, methods=['POST'])
users_blueprint.add_url_rule('<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])
