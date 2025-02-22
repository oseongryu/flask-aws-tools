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

import common.commonfunction as cmmfun
import config
from common.commonlogging import CommonLogging

load_dotenv()

sys.path.append("./common")
sys.path.append("./service")

template_folder_name = "dist" # # views, dist
db_name = "sqlite"
views_folder = os.path.join(os.path.dirname(__file__), ".", template_folder_name)

if template_folder_name == "views":
    app = Flask(__name__, template_folder=template_folder_name, static_url_path="/static", static_folder="views/static")
else:
    app = Flask(__name__, template_folder="dist", static_url_path="/v3-admin-vite", static_folder="dist")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
cmmfun.make_folder(config.PRJ_AUTO_PATH)
cmmfun.make_folder(config.PRJ_AUTO_LOG_PATH)
logFileName = os.path.join(config.PRJ_AUTO_LOG_PATH, "shorts.log")
# log = CommonLogging(logFileName)
# app.logger = log.logger


# Load and parse the array from the .env file
routes_items = os.getenv("ROUTES_ITEM", "").split(",")


from module_auth.routes_auth import routes_auth
from module_common.routes_common import routes_common
app.register_blueprint(routes_common)
app.register_blueprint(routes_auth)

for routes_item in routes_items:
    if "shorts" in routes_item:

        from module_shorts.routes_shorts import routes_shorts

        app.register_blueprint(routes_shorts)

        if db_name == "mysql":
            from flask_mysqldb import MySQL

            app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
            app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
            app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
            app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
            app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
            mysql = MySQL(app)
            # RuntimeError: Working outside of application context.
            app.app_context().push()
            db = mysql.connection
            app.db = db
        else:
            import sqlite3

            DATABASE = config.SHORTS_DB_PATH
            db = sqlite3.connect(DATABASE, check_same_thread=False)
            app.db = db
    elif "aws" in routes_item:
        from module_aws.routes_aws import routes_aws

        app.register_blueprint(routes_aws)


def create_routes():
    for root, dirs, files in os.walk(views_folder):
        for file in files:
            if file.endswith(".html"):
                relative_path = os.path.relpath(os.path.join(root, file), views_folder)
                route_path = "/" + os.path.splitext(relative_path)[0].replace("\\", "/")

                def route_func(data=route_path + ".html"):
                    return render_template(data)

                if "/includes" not in route_path:
                    app.add_url_rule(route_path, route_path, route_func)

create_routes()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8091)
