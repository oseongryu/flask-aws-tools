import os
import sys

from flask import Blueprint, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

import aws.aws_deploy as aws_deploy
import aws.aws_was_ip as aws_was_ip
from auth import token_required

routes_aws = Blueprint("routes_aws", __name__)


@routes_aws.route("/api/aws/run-aws-ip", methods=["POST"])
@token_required
def run_aws_ip():
    try:
        filter_value = request.json.get("filter_value")
        result = aws_was_ip.run_aws_ip()
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500


@routes_aws.route("/api/aws/run-aws-deploy", methods=["POST"])
@token_required
def run_aws_deploy():
    try:
        search_date = request.json.get("searchDate")
        result = aws_deploy.run_deploy(search_date)
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500


@routes_aws.route("/api/aws/run-aws-alb", methods=["POST"])
@token_required
def run_aws_alb():
    try:
        result = request.form.getlist("hours")
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500
