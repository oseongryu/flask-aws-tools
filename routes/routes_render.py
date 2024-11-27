import os
import sys

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from werkzeug.utils import secure_filename

import config

routes_render = Blueprint("routes_render", __name__)


@routes_render.route("/aws/")
def index():
    return render_template("aws/index.html")


@routes_render.route("/automation/")
def automationIndex():
    return render_template("automation/index.html")


@routes_render.route("/automation/list-images")
def list_images():
    images = [f for f in os.listdir(config.IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]
    return render_template("automation/list_images.html", images=images)


@routes_render.route("/automation/list-files")
def list_subdir_files():
    included_extensions = {".webp", ".png", ".jepg", ".jpg", ".gif"}
    subdir_files = {}
    for root, dirs, files in os.walk(config.SCREENSHOT_DIR):
        subdir = os.path.relpath(root, config.SCREENSHOT_DIR)
        filtered_files = [file for file in files if any(file.endswith(ext) for ext in included_extensions)]
        if len(filtered_files) > 0:
            subdir_files[subdir] = filtered_files
    return render_template("automation/list_files.html", subdir_files=subdir_files)
