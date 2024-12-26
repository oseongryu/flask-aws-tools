import json
import os
import subprocess

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
from app_class import FileModel

import config

routes_common = Blueprint("routes_common", __name__)


@routes_common.route("/background/<filename>", methods=["GET"])
def download_background_file(filename):
    return send_from_directory(config.BACKGROUND_DIR, filename)


@routes_common.route("/shorts/<location>/<filename>", methods=["GET"])
def download_shorts_file(location, filename):
    return send_from_directory(config.SHORTS_DIR + location, filename)


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


@routes_common.route("/api/file/select-file-list", methods=["POST"])
def select_file_list():
    file_download_dir = request.form.get("fileDownloadDir")
    file_type = request.form.get("type")
    if file_type == "dir":
        file_download_dir = config.SCREENSHOT_DIR
    elif file_type == "fileName":
        file_download_dir = file_download_dir.replace("screenshot", config.SCREENSHOT_DIR).replace("\\\\", "/")

    subdirs = []
    sub_full_path_list(file_download_dir, file_download_dir, subdirs, file_type)

    response_objects = [FileModel(file_id=i, file_name=subdir.file_name, file_path=subdir.file_path, file_dir=subdir.file_dir, file_parent_dir=subdir.file_parent_dir, file_custom_dir=subdir.file_custom_dir, depth1_dir=subdir.depth1_dir, depth2_dir=subdir.depth2_dir, depth3_dir=subdir.depth3_dir) for i, subdir in enumerate(subdirs)]
    response_objects.sort(key=lambda x: x.file_dir)
    response_dicts = [response.to_dict() for response in response_objects]
    return response_dicts, 200


@routes_common.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(config.IMAGE_DIR, filename)


@routes_common.route("/js/<path>/<filename>")
def serve_js(path, filename):
    return send_from_directory(os.path.join(config.JS_DIR), filename)


@routes_common.route("/view-file")
def view_file():
    subdir = request.args.get("subdir")
    filename = request.args.get("filename")
    return send_from_directory(os.path.join(config.SCREENSHOT_DIR, subdir), filename)


@routes_common.route("/load-class-path", methods=["POST"])
def load_class_path():
    param_map = request.json
    file_dir = param_map.get("fileDir")
    if file_dir == "automation-popup-setting-file-dir":
        file_dir = config.AUTOMATION_POPUP_SETTING
    elif file_dir == "dynamo-popup-setting-file-dir":
        file_dir = config.DYNAMO_POPUP_SETTING
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
        fileId = config.AUTOMATION_SETTING

    return common_service_load_type(fileId, type)


@routes_common.route("/run-command", methods=["POST"])
def run_command():
    try:
        command = request.json.get("command")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500


def common_service_load_type(fileId, type):
    if type == "project":
        return send_file(fileId, as_attachment=True)
    else:
        return send_file(os.path.expanduser("~") + "/git/python-selenium/app/fredit/screenshot/" + fileId + "/" + type, as_attachment=True)


def sub_full_path_list(original_file_dir, file_dir, result, type):
    file_separator = os.sep
    file_list = os.listdir(file_dir)
    for row_idx, file_name in enumerate(file_list):
        file_path = os.path.join(file_dir, file_name)
        if type == "dir":
            if os.path.isfile(file_path):
                continue
            elif os.path.isdir(file_path):
                parent_dir = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
                if not parent_dir == 'fredit':
                    dto = FileModel(
                        file_id=row_idx,
                        file_name=file_name,
                        file_path=file_path,
                        file_dir=file_name,
                        file_parent_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                        file_custom_dir=os.path.basename(os.path.dirname(file_path)) + file_separator + file_name,
                        depth1_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                        depth2_dir=os.path.basename(os.path.dirname(file_path)),
                        depth3_dir=file_name
                    )
                    result.append(dto)
                sub_full_path_list(original_file_dir, os.path.realpath(file_path), result, type)
        else:
            if os.path.isfile(file_path):
                dto = FileModel(
                    file_id=row_idx,
                    file_name=file_name,
                    file_path=file_path,
                    file_dir=file_name,
                    file_parent_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                    file_custom_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))) + file_separator + os.path.basename(os.path.dirname(file_path)) + file_separator + file_name,
                    depth1_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                    depth2_dir=os.path.basename(os.path.dirname(file_path)),
                    depth3_dir=file_name
                )
                result.append(dto)
            elif os.path.isdir(file_path):
                sub_full_path_list(original_file_dir, os.path.realpath(file_path), result, type)
    return result
