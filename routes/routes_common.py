import os

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    send_file,
    send_from_directory,
)
from werkzeug.utils import secure_filename

routes_common = Blueprint("routes_common", __name__)


@routes_common.route("/background/<filename>", methods=["GET"])
def download_background_file(filename):
    return send_from_directory(current_app.BACKGROUND_DIR, filename)


@routes_common.route("/shorts/<location>/<filename>", methods=["GET"])
def download_shorts_file(location, filename):
    return send_from_directory(current_app.SHORTS_DIR + location, filename)


@routes_common.route("/file/upload-file", methods=["POST"])
def upload_file():
    if "uploadFile" not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files["uploadFile"]
    if file.filename == "":
        return jsonify(message="No selected file"), 400
    if file:
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]
        filename = request.values["index"] + file_extension
        uploadPath = request.values["uploadPath"]
        os.makedirs(uploadPath, exist_ok=True)
        file.save(os.path.join(uploadPath, filename))
        return jsonify(message="File successfully uploaded"), 200


@routes_common.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(current_app.IMAGE_DIR, filename)


@routes_common.route("/js/<path>/<filename>")
def serve_js(path, filename):
    return send_from_directory(os.path.join(current_app.JS_DIR), filename)


@routes_common.route("/view-file")
def view_file():
    subdir = request.args.get("subdir")
    filename = request.args.get("filename")
    return send_from_directory(os.path.join(current_app.SCREENSHOT_DIR, subdir), filename)


@routes_common.route("/load-class-path", methods=["POST"])
def load_class_path():
    param_map = request.json
    file_dir = param_map.get("fileDir")
    if file_dir == "automation-popup-setting-file-dir":
        file_dir = current_app.AUTOMATION_POPUP_SETTING
    elif file_dir == "dynamo-popup-setting-file-dir":
        file_dir = current_app.DYNAMO_POPUP_SETTING
    return file_dir


@routes_common.route("/load-type/<type>/<fileId>", methods=["GET"])
def load_type(type, fileId):
    return common_service_load_type(type, fileId)


@routes_common.route("/load-type/<depth1>/<depth2>/<fileId>", methods=["GET"])
def load_type_depth(depth1, depth2, fileId):
    type = f"{depth1}/{depth2}"
    return common_service_load_type(type, fileId)


@routes_common.route("/load-type", methods=["POST"])
def load_type_post():
    # response.headers["Content-Type"] = "application/octet-stream"

    param_map = request.json
    type = param_map.get("type")
    fileId = param_map.get("fileId")
    if fileId == "automation-setting-file-dir":
        fileId = current_app.AUTOMATION_SETTING

    return common_service_load_type(fileId, type)


def common_service_load_type(fileId, type):
    return send_file(fileId, as_attachment=True)
