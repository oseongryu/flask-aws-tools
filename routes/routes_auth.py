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
from werkzeug.utils import secure_filename

import aws.aws_deploy as aws_deploy
import aws.aws_was_ip as aws_was_ip
from auth import token_required

routes_auth = Blueprint("routes_auth", __name__)


@routes_auth.route("/login", methods=["POST"])
def login():
    username = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
    if auth.username == username and auth.password == password:
        token = jwt.encode({"user": auth.username}, current_app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token})
    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})


@routes_auth.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello {current_user}!"})
