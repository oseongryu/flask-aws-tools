import json
import os
import subprocess
import sys
import time

from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    render_template,
    request,
    send_file,
    send_from_directory,
)
from werkzeug.utils import secure_filename

import common.commonfunction as cmmfun
import config
from auth import token_required
from module_common.models import FileModel

from . import routes_common


@routes_common.route("/")
def index():
    return render_template("index.html")


@routes_common.route("/shorts/<location>/<filename>", methods=["GET"])
def download_shorts_file(location, filename):
    return send_from_directory(os.path.join(config.SHORTS_PATH, location), filename)


@routes_common.route("/load-type/<type>/<fileId>", methods=["GET"])
def load_type(type, fileId):
    return common_service_load_type(type, fileId)


@routes_common.route("/load-type/<depth1>/<depth2>/<fileId>", methods=["GET"])
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
    if fileId == "automation-init":
        fileId = config.AUTO_STATIC_SETTING_PATH
    return common_service_load_type(fileId, type)


@routes_common.route("/load-class-path", methods=["POST"])
@token_required
def load_class_path():
    param_map = request.json
    fileId = param_map.get("fileId")
    if fileId == "automation-popup":
        fileId = config.AUTO_POPUP_JSON_PATH
    return fileId


@routes_common.route("/api/common/upload-file", methods=["POST"])
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
        new_filename = request.values["index"] + ".webp"
        uploadPath = os.path.join(config.SHORTS_PATH, request.values["storyId"])
        os.makedirs(uploadPath, exist_ok=True)

        # Save the original file temporarily
        temp_path = os.path.join(uploadPath, filename)
        file.save(temp_path)

        # # pip install Pillow
        # from PIL import Image
        # # Convert the file to webp format
        # with Image.open(temp_path) as img:
        #     webp_path = os.path.join(uploadPath, new_filename)
        #     img.save(webp_path, "webp")

        # Remove the temporary file
        # os.remove(temp_path)

        return jsonify(message="File successfully uploaded and converted to webp"), 200


@routes_common.route("/api/common/select-file", methods=["POST"])
@token_required
def select_file_list():
    filePath = request.form.get("filePath")
    file_type = request.form.get("type")
    sort_key = request.form.get("sort_key")
    sort_order = request.form.get("sort_order")
    if sort_key is None or sort_key == "":
        sort_key = "file_dir"
    file_type = request.form.get("type")
    if file_type == "dir":
        filePath = config.PRJ_SCREENSHOT_PATH
    elif file_type == "fileName":
        filePath = filePath.replace("automation-screenshot", config.PRJ_SCREENSHOT_PATH).replace("\\\\", "/")

    subdirs = []
    cmmfun.sub_full_path_list(filePath, filePath, subdirs, file_type)

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
    sort_response_objects(response_objects, sort_key=sort_key, descending=(sort_order == "desc"))
    response_dicts = [response.to_dict() for response in response_objects]
    return response_dicts, 200


@routes_common.route("/api/common/run-command", methods=["POST"])
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
        return send_file(os.path.join(config.PRJ_SCREENSHOT_PATH, fileId, type), as_attachment=True)


@routes_common.route("/api/common/file-log", methods=["POST"])
def filelog():
    try:
        with open("/app/logs/shorts.log", "r") as log_file:
            log_contents = log_file.readlines()
        log_contents.reverse()
    except Exception as e:
        log_contents = [f"Error reading log file: {str(e)}"]
    return jsonify({"log_contents": log_contents})


@routes_common.route("/api/common/real-log")
def logs():
    return Response(generate_log(), mimetype="text/event-stream")


def generate_log():
    log_file_path = os.path.join(config.PRJ_AUTO_LOG_PATH, "shorts.log")
    with open(log_file_path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            yield f"data:{line}\n\n"


@routes_common.route("/api/common/python-exec", methods=["GET", "POST"])
# @token_required
def python_exec():
    if request.method == "GET":
        exec_type = request.args.get("type")
        args1 = request.args.get("args1")
        if not args1 or not type:
            return jsonify(message="Missing required query parameters"), 400
    else:
        param_map = request.json
        if not param_map:
            return jsonify(message="Missing required JSON parameters"), 400
        for key, value in param_map.items():
            if key == "type":
                exec_type = value
            elif key == "args1":
                args1 = value

    python_env_path = config.PYTHON_ENV_PATH_WIN

    if exec_type == "shorts":
        python_path = config.SHORTS_TTS_SCRIPT_PATH
    elif exec_type == "automation":
        python_path = config.AUTOMATION_SCRIPT_PATH
    elif exec_type == "automationclear":
        python_path = config.AUTOMATION_REMOVE_SCRIPT_PATH

    try:
        result = run_async_process(python_env_path, python_path, args1)
        return jsonify(message=f"{result}"), 200

    except Exception as e:
        return jsonify(message=f"Error executing script: {str(e)}"), 500


def run_process(python_env_path, python_path, args1):
    try:
        print(f"Executing script: {python_env_path} {python_path} {args1}")
        result = subprocess.run([python_env_path, python_path, args1], capture_output=True, text=True)
        return f"Script executed successfully {result.stdout} {result.stderr}"

    except Exception as e:
        return f"Error executing script: {str(e)}"


def run_async_process(python_env_path, python_path, args1, waiting=False):
    try:
        print(f"Executing script: {python_env_path} {python_path} {args1}")
        process = subprocess.Popen([python_env_path, python_path, args1], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if waiting:
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print("Command executed successfully")
                return "Output:" + stdout
            else:
                print("Command execution failed")
                return "Error:" + stderr
        else:
            return f"Started process with PID: {process.pid}"
    except Exception as e:
        return f"Error: executing script: {str(e)}"


def sort_response_objects(response_objects, sort_key="file_dir", descending=False):
    response_objects.sort(key=lambda x: getattr(x, sort_key), reverse=descending)
