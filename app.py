import os
import sys
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    render_template,
    request,
    send_file,
    send_from_directory,
)

from routes.routes_auth import routes_auth
from routes.routes_common import routes_common
from routes.routes_render import routes_render

app = Flask(__name__, template_folder="templates", static_url_path="/static", static_folder="static")
app.register_blueprint(routes_common)
app.register_blueprint(routes_render)
app.register_blueprint(routes_auth)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

load_dotenv()

# Load and parse the array from the .env file
routes_items = os.getenv("ROUTES_ITEM", "").split(",")

db_name = "sqlite"
for routes_item in routes_items:
    if "shorts" in routes_item:

        from routes.routes_shorts import routes_shorts

        app.register_blueprint(routes_shorts)

        if db_name == "mysql":
            from flask_mysqldb import MySQL

            app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
            app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
            app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
            app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
            app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
            mysql = MySQL(app)
            db = mysql.connection
            app.db = db
        else:
            import sqlite3

            DATABASE = os.getenv("SQLITE_DB_PATH")
            db = sqlite3.connect(DATABASE, check_same_thread=False)
            app.db = db
    elif "aws" in routes_item:
        from routes.routes_aws import routes_aws

        app.register_blueprint(routes_aws)

    elif "automation" in routes_item:
        from routes.routes_automation import routes_automation

        app.register_blueprint(routes_automation)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8091)
