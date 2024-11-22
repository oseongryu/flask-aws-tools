import os
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from routes.routes_common import routes_common
from routes.routes_render import routes_render

SCREENSHOT_DIR = os.path.expanduser("~") + "/git/python-selenium/app/fredit/screenshot"
SHORTS_DIR = os.path.expanduser("~") + "/DEV/shorts/"
BACKGROUND_DIR = os.path.expanduser("~") + "/DEV/shorts/background"
IMAGE_DIR = os.path.expanduser("~") + "/git/python-selenium/app/fredit/screenshot/41_simple_card_basic/20241121_012025"


app = Flask(__name__, template_folder="templates", static_url_path="/static", static_folder="static")
app.register_blueprint(routes_common)
app.register_blueprint(routes_render)

app.SCREENSHOT_DIR = SCREENSHOT_DIR
app.SHORTS_DIR = SHORTS_DIR
app.BACKGROUND_DIR = BACKGROUND_DIR
app.IMAGE_DIR = IMAGE_DIR

load_dotenv()

# Load and parse the array from the .env file
routes_item = os.getenv("routes_item", "").split(",")


if "shorts" in routes_item:
    from flask_mysqldb import MySQL

    from routes.routes_shorts import routes_shorts

    app.register_blueprint(routes_shorts)

    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
    mysql = MySQL(app)
    app.mysql = mysql


if "aws" in routes_item:
    from routes.routes_aws import routes_aws

    app.register_blueprint(routes_aws)

if "automation" in routes_item:
    from routes.routes_automation import routes_automation

    app.register_blueprint(routes_automation)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8091)
