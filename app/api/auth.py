"""
from flask import jsonify, request
from app.api import bp

@bp.route('/auth', methods=['POST'])
def authRouteHandler():
    print(request.authorization["username"])
    print(request.authorization["password"])
    return "ok"
"""

from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_login import current_user
from app.data_models.User import User
from app.api.errors import error_response
from flask import jsonify, request
from app.api import bp

@bp.route('/login', methods=['POST'])
def authRouteHandler():
    """ uname = request.authorization["username"]
    passphrase = request.authorization["password"] """
    credentials = request.get_json(force=True)
    print("credentials: ", credentials)
    uname = credentials['username']
    passphrase = credentials['password']
    try:
        user = User.query.filter_by(username=uname).first()
        if user.check_password(str(passphrase)):
            user.get_token()
            g.current_user = user
            return jsonify({'username': user.username, 'token': user.token})
    except Exception as ex:
        return error_response(403, str(ex))
    return "not ok"

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)