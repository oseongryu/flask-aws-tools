# auth.py
from functools import wraps

# pip install pyjwt
import jwt
from flask import current_app, g, jsonify, request

EXPT_URLS = [
    ("/tb_code_info", "GET"),
    ("/tb_device_info", "POST"),
    ("/tb_unit_info", "POST"),
    ("/tb_user_info/count", "GET"),
    ("/tb_user_info", "POST"),
    ("/tb_user_info", "DELETE"),
    {"/common/image", "GET"},
]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["user"]
        except:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(*args, **kwargs)

    return decorated


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # auth 제외 url

        for path, method in EXPT_URLS:
            if path in request.path and method in request.method:
                return f(*args, **kwargs)

        else:
            if "x-access-tokens" in request.headers:
                token = request.headers["x-access-tokens"]
            elif "Authorization" in request.headers:
                auth_header = request.headers["Authorization"]
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
            if not token:
                return jsonify({"message": "Token is missing!"}), 401
            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                g.user = data
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token is invalid!"}), 401
            return f(*args, **kwargs)

    return decorated
