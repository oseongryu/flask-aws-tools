import os
import sys

from dotenv import load_dotenv
from flask import (
    Blueprint,
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

import aws_deploy
import aws_was_ip

app = Flask(__name__, template_folder="templates", static_url_path="/static", static_folder="static")

load_dotenv()


@app.route("/aws/")
def index():
    return render_template("aws/index.html")


@app.route("/aws/ip")
def ip():
    return render_template("aws/index.html")


@app.route("/aws/deploy")
def deploy():
    return render_template("aws/deploy.html")


@app.route("/aws/run_aws_ip", methods=["POST"])
def run_aws_ip():
    try:
        filter_value = request.json.get("filter_value")
        arrdev, arrprd = aws_was_ip.run_aws_ip()
        result = {"dev": arrdev, "prd": arrprd}
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "Script execution failed", "error": str(e)}), 500


@app.route("/aws/run_aws_deploy", methods=["POST"])
def run_aws_deploy():
    try:
        search_date = request.json.get("searchDate")
        result = aws_deploy.run_deploy(search_date)
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "Script execution failed", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8091)
