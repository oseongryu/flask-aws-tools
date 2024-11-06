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

from routes.routes_aws import routes_aws

app = Flask(__name__, template_folder="templates", static_url_path="/static", static_folder="static")

load_dotenv()

# Load and parse the array from the .env file
routes_item = os.getenv("routes_item", "").split(",")

if "shorts" in routes_item:
    from routes.routes_automation import routes_automation
    from routes.routes_common import routes_common
    from routes.routes_shorts import routes_shorts

    app.register_blueprint(routes_automation)
    app.register_blueprint(routes_common)
    app.register_blueprint(routes_shorts)

    from flask_mysqldb import MySQL

    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
    mysql = MySQL(app)
    app.mysql = mysql

app.register_blueprint(routes_aws)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8091)
