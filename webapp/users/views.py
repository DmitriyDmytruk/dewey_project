from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError

from webapp import db

# from .models import UserModel, RoleModel
from .schemas import UserSchema


users_blueprint = Blueprint("users", __name__, url_prefix="/users")


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

    def post(self):
        """
        Create a new user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: data
            schema:
              id: UserModel
              required:
                - email
                - role
              properties:
                email:
                  type: string
                  description: email for user
                role:
                  schema:
                    id: RoleModel
                    required:
                      - title
                    properties:
                      title:
                        type: string
                        description: title of role
        responses:
          201:
            description: User created
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            data = UserSchema(partial=True).load(json_data)
        except ValidationError as err:
            return err.messages, 422
        email, role_title = data["email"], data["role"]["title"]
        role = RoleModel.query.get(title=role_title)
        user = UserModel.query.filter_by(email=email).first()
        if user is None:
            user = UserModel(email=email, is_active=False, role_id=role.id)
            db.session.add(user)
            db.session.commit()
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


user_view = UserAPI.as_view("users")

users_blueprint.add_url_rule(
    "", defaults={"user_id": None}, view_func=user_view, methods=["GET"]
)
users_blueprint.add_url_rule("", view_func=user_view, methods=["POST"])
users_blueprint.add_url_rule(
    "<int:user_id>", view_func=user_view, methods=["GET", "PUT", "DELETE"]
)
