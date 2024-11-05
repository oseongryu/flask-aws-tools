import os
import sys

from flask import Blueprint, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

import aws.aws_deploy as aws_deploy
import aws.aws_was_ip as aws_was_ip

routes_aws = Blueprint("routes_aws", __name__)


@routes_aws.route("/aws/")
def index():
    return render_template("aws/index.html")


@routes_aws.route("/aws/ip")
def ip():
    return render_template("aws/index.html")


@routes_aws.route("/aws/deploy")
def deploy():
    return render_template("aws/deploy.html")


@routes_aws.route("/aws/run_aws_ip", methods=["POST"])
def run_aws_ip():
    try:
        filter_value = request.json.get("filter_value")
        arrdev, arrprd = aws_was_ip.run_aws_ip()
        result = {"dev": arrdev, "prd": arrprd}
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "Script execution failed", "error": str(e)}), 500


@routes_aws.route("/aws/run_aws_deploy", methods=["POST"])
def run_aws_deploy():
    try:
        search_date = request.json.get("searchDate")
        result = aws_deploy.run_deploy(search_date)
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "Script execution failed", "error": str(e)}), 500
