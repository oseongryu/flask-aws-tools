import os
import subprocess
import sys

from flask import Blueprint, jsonify, render_template, request, send_from_directory

import config
from auth import token_required

routes_automation = Blueprint("routes_automation", __name__)


@routes_automation.route("/api/automation/python-exec", methods=["GET", "POST"])
@token_required
def python_exec():
    script_id = request.args.get("id") or request.form.get("id")
    type = request.args.get("type")

    if not script_id:
        return jsonify(message="Missing required query parameters"), 400

    if type == "shorts":
        python_path = config.PYTHON_SHORTS_TTS_PATH
        python_env_path = config.PYTHON_ENV_PATH_MAC
    else:
        python_path = config.PYTHON_AUTOMATION_PATH
        python_env_path = "python3"

    try:
        result = run_async_process(python_env_path, python_path, script_id)
        return jsonify(message=f"{result}"), 200

    except Exception as e:
        return jsonify(message=f"Error executing script: {str(e)}"), 500


def run_process(python_env_path, python_path, script_id):
    try:
        result = subprocess.run([python_env_path, python_path, script_id], capture_output=True, text=True)
        return f"Script executed successfully {result.stdout} {result.stderr}"

    except Exception as e:
        return f"Error executing script: {str(e)}"


def run_async_process(python_env_path, python_path, script_id, waiting=False):
    try:
        process = subprocess.Popen([python_env_path, python_path, script_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
