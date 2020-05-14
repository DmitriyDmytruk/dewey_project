from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView
from marshmallow import ValidationError

from webapp import db
from webapp.utils.mailing import sengrid_send_mail

from .models import RoleModel, UserModel
from .schemas import UserSchema
from .swagger_docstrings import login_docstring, user_create_docstring


users_blueprint = Blueprint("users", __name__, url_prefix="/users")


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):  # pylint: disable=C0116
        post_data = request.get_json()
        try:
            user = UserModel.query.filter_by(email=post_data["email"]).first()
            if user and user.check_password(post_data["password"]):
                auth_token = user.encode_auth_token()
                if auth_token:
                    responseObject = {
                        "status": "success",
                        "message": "Successfully logged in.",
                        "auth_token": auth_token.decode(),
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    "status": "fail",
                    "message": "User does not exist.",
                }
                return make_response(jsonify(responseObject)), 404
        except Exception:
            responseObject = {"status": "fail", "message": "Try again"}
            return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    Users endpoints
    """

    def get(self, user_id):
        """
        :param user_id:
        :return:
        """
        if user_id is None:
            # list view
            pass
        else:
            # detail view
            pass

    def post(self):  # pylint: disable=C0116
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            data = UserSchema(partial=True).load(json_data)
        except ValidationError as err:
            return err.messages, 422
        email, role_title = data["email"], data["role"]["title"]
        role = RoleModel.query.filter_by(title=role_title).one()
        # TODO: If role not exists?
        user = UserModel.query.filter_by(email=email).one_or_none()
        if user is None:
            user = UserModel(email=email, is_active=False, role_id=role.id)
            db.session.add(user)
            db.session.commit()

            content = "Hi there"
            content_type = "text/plain"
            subject = "Sending with SendGrid"
            sengrid_send_mail(email, subject, content, content_type)

            result = UserSchema.dump(UserModel.query.get(user.id))
            return {"message": "Created new user.", "user": result}

    def delete(self):
        """
        Delete user
        """
        ...

    def put(self):
        """
        Update user
        """
        ...


login_view = LoginAPI.as_view("login")
users_blueprint.add_url_rule("login", view_func=login_view, methods=["POST"])

user_view = UserAPI.as_view("users")

users_blueprint.add_url_rule(
    "", defaults={"user_id": None}, view_func=user_view, methods=["GET"]
)
users_blueprint.add_url_rule("", view_func=user_view, methods=["POST"])
users_blueprint.add_url_rule(
    "<int:user_id>", view_func=user_view, methods=["GET", "PUT", "DELETE"]
)

LoginAPI.post.__doc__ = login_docstring
UserAPI.post.__doc__ = user_create_docstring
