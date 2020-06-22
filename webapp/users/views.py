from typing import Optional, Union

from flask import request
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
                    return {
                        "message": "Successfully logged in.",
                        "auth_token": auth_token.decode(),
                    }
                return {"message": "Token not found",}, 401
            return {"message": "User not found."}, 404
        except Exception:
            return {"message": "Error. Try again"}, 500
