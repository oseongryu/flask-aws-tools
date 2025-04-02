import json
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

from . import routes_auth


@routes_auth.route("/api/auth", methods=["POST"])
def auth():
    username = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    print(username, password)
    auth = request.authorization
    print(auth.username, auth.password)
    if not auth or not auth.username or not auth.password:
        # return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
        return jsonify(message="Missing required query parameters"), 400
    if auth.username == username and auth.password == password:
        token = jwt.encode({"user": auth.username}, current_app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token}), 200
        # return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
    return jsonify(message="Missing required query parameters"), 400


@routes_auth.route("/api/token-test", methods=["GET"])
@token_required
def protected_route():
    param1 = request.args.get("param1")
    return jsonify({"message": f"Hello! {param1}"}), 200
