import jwt
from flask import Blueprint


auth_blueprint = Blueprint("auth", __name__)

# class LoginAPI(MethodView):
#     """
#     User Login Resource
#     """
#     def post(self):
#         # get the post data
#         post_data = request.get_json()
#         try:
#             # fetch the user data
#             user = User.query.filter_by(
#                 email=post_data.get('email')
#               ).first()
#             auth_token = user.encode_auth_token(user.id)
#             if auth_token:
#                 responseObject = {
#                     'status': 'success',
#                     'message': 'Successfully logged in.',
#                     'auth_token': auth_token.decode()
#                 }
#                 return make_response(jsonify(responseObject)), 200
#         except Exception as e:
#             print(e)
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'Try again'
#             }
#             return make_response(jsonify(responseObject)), 500


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"))
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
