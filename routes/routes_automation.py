import os
import subprocess
import sys

from flask import Blueprint, jsonify, render_template, request, send_from_directory

# sys.path.append(os.path.expanduser("~") + '/git/python-selenium/shorts')
# import tts_story
# sys.path.append(os.path.expanduser("~") + '/git/python-selenium/selenium')
# import service

routes_automation = Blueprint("routes_automation", __name__)

# @routes_automation.route('/run-tts-story', methods=['GET'])
# def run_tts_story():
#     # story_id = request.json.get('story_id', 1)
#     # story_name = request.json.get('story_name', 'shorts')
#     story_id = '5'
#     story_name = 'shorts'
#     try:
#         result = tts_story.run_tts_story(story_id, story_name)
#         return jsonify({"message": "Script executed successfully", "output": result})
#     except Exception as e:
#         return jsonify({"message": "Script execution failed", "error": str(e)}), 500


# @routes_automation.route('/run-automation', methods=['GET'])
# def run_automation():

#     init_number = request.args.get('no')
#     # site_name = request.args.get('siteName')
#     site_name = 'fredit'
#     try:
#         result = service.run_script(init_number, site_name)
#         # return jsonify({"message": "Script executed successfully", "output": result})
#     except Exception as e:
#         return jsonify({"message": "Script execution failed", "error": str(e)}), 500


@routes_automation.route("/api/automation/python-exec", methods=["GET", "POST"])
def python_exec():
    script_id = request.args.get("id") or request.form.get("id")
    python_path = request.args.get("pythonPath")
    python_env_path = request.args.get("pythonEnvPath")
    if python_env_path == None:
        python_env_path = "python3"
    if python_path == None:
        python_path = os.path.expanduser("~") + "/git/python-selenium/selenium/service.py"

    if not script_id or not python_path or not python_env_path:
        return jsonify(message="Missing required query parameters"), 400

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
