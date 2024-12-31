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

import config
from app_class import FileModel
from auth import token_required

routes_common = Blueprint("routes_common", __name__)


@routes_common.route("/background/<filename>", methods=["GET"])
@token_required
def download_background_file(filename):
    return send_from_directory(config.BACKGROUND_DIR, filename)


@routes_common.route("/shorts/<location>/<filename>", methods=["GET"])
@token_required
def download_shorts_file(location, filename):
    return send_from_directory(config.SHORTS_DIR + location, filename)


@routes_common.route("/file/upload-file", methods=["POST"])
@token_required
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
        uploadPath = config.SHORTS_DIR + request.values["storyId"]
        os.makedirs(uploadPath, exist_ok=True)
        file.save(os.path.join(uploadPath, filename))
        return jsonify(message="File successfully uploaded"), 200


@routes_common.route("/file/file-list", methods=["POST"])
@token_required
def select_file_list():
    file_download_dir = request.form.get("fileDownloadDir")
    file_type = request.form.get("type")
    if file_type == "dir":
        file_download_dir = config.SCREENSHOT_DIR
    elif file_type == "fileName":
        file_download_dir = file_download_dir.replace("screenshot", config.SCREENSHOT_DIR).replace("\\\\", "/")

    subdirs = []
    sub_full_path_list(file_download_dir, file_download_dir, subdirs, file_type)

    response_objects = [
        FileModel(
            file_id=index,
            file_name=subdir.file_name,
            file_path=subdir.file_path,
            file_dir=subdir.file_dir,
            file_parent_dir=subdir.file_parent_dir,
            file_custom_dir=subdir.file_custom_dir,
            depth1_dir=subdir.depth1_dir,
            depth2_dir=subdir.depth2_dir,
            depth3_dir=subdir.depth3_dir,
        )
        for index, subdir in enumerate(subdirs)
    ]
    response_objects.sort(key=lambda x: x.file_dir)
    response_dicts = [response.to_dict() for response in response_objects]
    return response_dicts, 200


@routes_common.route("/load-class-path", methods=["POST"])
@token_required
def load_class_path():
    param_map = request.json
    file_dir = param_map.get("fileDir")
    if file_dir == "automation-popup-setting-file-dir":
        file_dir = config.AUTOMATION_POPUP_SETTING
    return file_dir


@routes_common.route("/load-type/<type>/<fileId>", methods=["GET"])
@token_required
def load_type(type, fileId):
    return common_service_load_type(type, fileId)


@routes_common.route("/load-type/<depth1>/<depth2>/<fileId>", methods=["GET"])
@token_required
def load_type_depth(depth1, depth2, fileId):
    type = f"{depth1}/{depth2}"
    return common_service_load_type(type, fileId)


@routes_common.route("/load-type", methods=["POST"])
@token_required
def load_type_post():
    # response.headers["Content-Type"] = "application/octet-stream"
    param_map = request.json
    type = param_map.get("type")
    fileId = param_map.get("fileId")
    if fileId == "automation-setting-file-dir":
        fileId = config.AUTOMATION_SETTING

    return common_service_load_type(fileId, type)


@routes_common.route("/run-command", methods=["POST"])
@token_required
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
        return send_file(config.SCREENSHOT_DIR + "/" + fileId + "/" + type, as_attachment=True)


def list_subdir_files(filePath):
    included_extensions = {".webp", ".png", ".jepg", ".jpg", ".gif"}
    subdir_files = {}
    for root, dirs, files in os.walk(filePath):
        subdir = os.path.relpath(root, filePath)
        filtered_files = [file for file in files if any(file.endswith(ext) for ext in included_extensions)]
        if len(filtered_files) > 0:
            subdir_files[subdir] = filtered_files
    return subdir_files


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
                if not parent_dir == "fredit":
                    dto = FileModel(
                        file_id=row_idx,
                        file_name=file_name,
                        file_path=file_path,
                        file_dir=file_name,
                        file_parent_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                        file_custom_dir=os.path.basename(os.path.dirname(file_path)) + file_separator + file_name,
                        depth1_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                        depth2_dir=os.path.basename(os.path.dirname(file_path)),
                        depth3_dir=file_name,
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
                    depth3_dir=file_name,
                )
                result.append(dto)
            elif os.path.isdir(file_path):
                sub_full_path_list(original_file_dir, os.path.realpath(file_path), result, type)
    return result
