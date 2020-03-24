import functools
from typing import Dict

from flask import request

from webapp.auth.views import decode_auth_token
from webapp.users.models import UserModel


def get_fail_response(response: dict) -> Dict:
    """
    Generate response for login_required function
    :param response:
    :return: dict
    """
    return {"status": 401, "message": response.get("message")}


def login_required(f):
    """
    Checking user authorization by JWT Token
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            response = decode_auth_token(auth_token)
            if response.get("email") and response.get("status") == "success":
                user = UserModel.query.filter_by(
                    email=response.get("email")
                ).one_or_none()
                if user:
                    # TODO: Need to add permission checking
                    return f(*args, **kwargs)
            else:
                return get_fail_response(response)
        else:
            return get_fail_response(
                {"message": "Provide a valid auth token."}
            )
        return f(*args, **kwargs)

    return decorated_function
