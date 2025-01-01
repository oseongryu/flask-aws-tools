import os
import sys

import jwt
from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
)

from auth import token_required

routes_auth = Blueprint("routes_auth", __name__)


@routes_auth.route("/api/auth", methods=["POST"])
def auth():
    username = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        # return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
        return jsonify(message="Missing required query parameters"), 400
    if auth.username == username and auth.password == password:
        token = jwt.encode({"user": auth.username}, current_app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token})
        # return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
    return jsonify(message="Missing required query parameters"), 400


@routes_auth.route("/api/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello {current_user}!"})
