from typing import Optional, Union

from flask import current_app, request
from flask.views import MethodView
from marshmallow import ValidationError

from webapp import db

from .models import RoleModel, UserModel
from .schemas import user_schema


# from webapp.utils.mailing import sengrid_send_mail


class LoginAPIView(MethodView):
    """
    User Login Resource
    """

    def post(self):
        """
        User login
        """
        post_data = request.get_json()
        try:
            user: UserModel = UserModel.query.filter_by(
                email=post_data["email"]
            ).first()
            if (
                user
                and user.is_active
                and user.check_password(post_data["password"])
            ):
                auth_token: Union[str, bytes] = user.encode_auth_token()
                if auth_token:
                    return {
                        "message": "Successfully logged in.",
                        "auth_token": auth_token.decode(),
                    }
                return {"message": "Token not found"}, 401
            return {"message": "User not found."}, 404
        except Exception as error:
            current_app.logger.error(error, exc_info=True)
            return {"message": "Error. Try again"}, 500


class UserAPIView(MethodView):
    """
    Users endpoints
    """

    def post(self):
        """
        User create
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            user_schema.partial = True
            data = user_schema.load(json_data)
        except ValidationError as error:
            current_app.logger.error(error, exc_info=True)
            return {"messages": error.messages}, 422
        email, role_title, password = (
            data["email"],
            data["role"]["title"],
            data["password"],
        )
        role: RoleModel = RoleModel.query.filter_by(
            title=role_title
        ).one_or_none()
        # TODO: If role not exists?
        user: Optional[UserModel] = UserModel.query.filter_by(
            email=email
        ).one_or_none()
        if user is None:
            user: UserModel = UserModel(email=email, password=password)
            if role:
                user.role = role
            user.password = user._hash_password(user.password)
            db.session.add(user)
            db.session.commit()

            # content: str = "Hi there"
            # content_type: str = "text/plain"
            # subject: str = "Sending with SendGrid"
            # sengrid_send_mail(email, subject, content, content_type)

            result = user_schema.dump(user)
            return {"message": "User created", "user": result}, 201
        return {"message": "User with this email address already exists"}, 422
