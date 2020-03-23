import functools

import flask
from flask import request

from webapp.auth.views import decode_auth_token
from webapp.users.models import UserModel


def login_required(f):
    """
    Checking user authorization by JWT Token
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            if auth_token:
                email = decode_auth_token(auth_token)
                user = UserModel.query.filter_by(email=email).one_or_none()
                if user:
                    return f(*args, **kwargs)
            else:
                flask.abort(401)
        else:
            flask.abort(401)
        return f(*args, **kwargs)

    return decorated_function
