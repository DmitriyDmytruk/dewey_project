from typing import Dict, Optional, Union

from flask import jsonify, make_response, request
from flask.views import MethodView
from marshmallow import ValidationError

from webapp import db
from webapp.utils.mailing import sengrid_send_mail

from .models import RoleModel, UserModel
from .schemas import UserSchema


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
                    response_object: Dict[str, str] = {
                        "status": "success",
                        "message": "Successfully logged in.",
                        "auth_token": auth_token.decode(),
                    }
                    return make_response(jsonify(response_object)), 200
                response_object: Dict[str, str] = {
                    "status": "success",
                    "message": "Sign In failed",
                }
                return make_response(jsonify(response_object)), 200
            response_object: Dict[str, str] = {
                "status": "fail",
                "message": "User does not exist.",
            }
            return make_response(jsonify(response_object)), 404
        except Exception:
            response_object: Dict[str, str] = {
                "status": "fail",
                "message": "Try again",
            }
            return make_response(jsonify(response_object)), 500


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
            data = UserSchema(partial=True).load(json_data)
        except ValidationError as err:
            return err.messages, 422
        email, role_title = data["email"], data["role"]["title"]
        role: RoleModel = RoleModel.query.filter_by(title=role_title).one()
        # TODO: If role not exists?
        user: Optional[UserModel] = UserModel.query.filter_by(
            email=email
        ).one_or_none()
        if user is None:
            user: UserModel = UserModel(email=email, role_id=role.id)
            db.session.add(user)
            db.session.commit()

            content: str = "Hi there"
            content_type: str = "text/plain"
            subject: str = "Sending with SendGrid"
            sengrid_send_mail(email, subject, content, content_type)

            result = UserSchema().dump(user)
            return {"message": "Created new user.", "user": result}, 201
        return {"message": "Fail"}, 400
