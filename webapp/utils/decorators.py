import functools
from typing import Dict, List, Optional, Union

from flask import request, session

from webapp.auth.views import decode_auth_token
from webapp.users.models import RoleModel, UserModel


def get_fail_response(status: int, response: dict) -> Dict:
    """
    Generate response for login_required function
    :param status:int
    :param response:dict
    :return: dict
    """
    return {"status": status, "message": response.get("message")}


def get_user_by_token() -> Optional[Dict[str, Union[int, str]]]:
    """
    Get user from jwt token
    :return: dict|None
    """
    auth_header = request.headers.get("Authorization")
    session["user"] = None
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        response = decode_auth_token(auth_token)
        if response.get("email") and response.get("status") == "success":
            user = UserModel.query.filter_by(
                email=response.get("email")
            ).one_or_none()
            if user:
                session["user"] = user
        else:
            return get_fail_response(401, response)
    else:
        return get_fail_response(
            401, {"message": "Provide a valid auth token."}
        )


def check_user_permissions(permissions: List[str]) -> bool:
    """
    Check user permissions
    :param permissions:
    :return: bool
    """
    res = False
    user = session.get("user")
    if user:
        user_role = RoleModel.query.filter_by(id=user.role_id).one_or_none()
        if user_role:
            check_perm = any(
                p.title in permissions for p in user_role.permissions
            )
            if check_perm:
                res = True
    return res


def login_required(f):
    """
    Checking user authorization by JWT Token
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        user_by_token = get_user_by_token()
        if session.get("user"):
            return f(*args, **kwargs)
        else:
            return user_by_token

    return decorated_function


def permissions(*permissions):
    """
    Checking user permission
    """

    def decorated_function(f):
        def new_f(*args, **kwargs):
            user = session.get("user")
            if not user:
                get_user_by_token()
                user = session.get("user")
            if not user:
                return get_fail_response(401, {"message": "User not found."})
            check_perm = check_user_permissions(*permissions)
            if not check_perm:
                return get_fail_response(403, {"message": "Access denied."})
            return f(*args, **kwargs)

        new_f.__name__ = f.__name__
        return new_f

    return decorated_function
