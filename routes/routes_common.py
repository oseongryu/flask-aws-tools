import os

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
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


@routes_common.route("/view-file")
def view_file():
    subdir = request.args.get("subdir")
    filename = request.args.get("filename")
    return send_from_directory(os.path.join(current_app.SCREENSHOT_DIR, subdir), filename)
