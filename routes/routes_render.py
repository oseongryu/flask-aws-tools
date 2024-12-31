import os
import sys

from flask import Blueprint, render_template

routes_render = Blueprint("routes_render", __name__)


@routes_render.route("/")
def index():
    return render_template("aws/index.html")


@routes_render.route("/aws/")
def aws_index():
    return render_template("aws/index.html")


@routes_render.route("/automation/")
def automation_index():
    return render_template("automation/index.html")


@routes_render.route("/auth/")
def auth_index():
    return render_template("auth/index.html")
