import json

# werkzeug 로거 비활성화
import logging
import os
import platform
import sys
from datetime import datetime
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    g,
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
from config import EnumDB, TemplateFolder
from module_linkview.models import db

# # before_request, after_request를 위해서 로깅 비활성화
# log = logging.getLogger("werkzeug")
# log.disabled = True

# import logging
# import sqlparse  # SQL 쿼리 포매팅 라이브러리

# class SQLAlchemySQLFormatter(logging.Formatter):
#     def format(self, record):
#         sql = sqlparse.format(record.getMessage(), keyword_case="upper", identifier_case="lower", truncate_strings=50, reindent=True).strip("")
#         sql = "\n\t\t| ".join([l for l in sql.split("\n")])
#         return sql

# sql_logger = logging.getLogger("sqlalchemy.engine.Engine")

# handler = logging.StreamHandler()
# handler.setFormatter(SQLAlchemySQLFormatter())

# sql_logger.addHandler(handler)

load_dotenv()

sys.path.append("./common")
sys.path.append("./service")

db_name = EnumDB.SQLITE.value
if platform.system() == "Windows":
    template_folder_name = TemplateFolder.VIEWS.value
elif platform.system() == "Darwin":
    template_folder_name = TemplateFolder.VIEWS.value
else:
    template_folder_name = TemplateFolder.DIST.value

views_folder = os.path.join(os.path.dirname(__file__), ".", template_folder_name)

if template_folder_name == TemplateFolder.VIEWS.value:
    app = Flask(__name__, template_folder=template_folder_name, static_url_path="/static", static_folder=f"{template_folder_name}/static")
else:
    app = Flask(__name__, template_folder=template_folder_name, static_url_path="/", static_folder=template_folder_name)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
import logging

# Load and parse the array from the .env file
routes_items = os.getenv("ROUTES_ITEM", "").split(",")


from module_auth.routes_auth import routes_auth
from module_common.routes_common import routes_common

app.register_blueprint(routes_common)
app.register_blueprint(routes_auth)


for routes_item in routes_items:
    if "shorts" in routes_item:
        cmmfun.make_folder(config.PRJ_AUTO_PATH)
        cmmfun.make_folder(config.PRJ_AUTO_LOG_PATH)
        logFileName = os.path.join(config.PRJ_AUTO_LOG_PATH, "shorts.log")
        log = CommonLogging(logFileName)
        app.logger = log.logger
        from module_shorts.routes_shorts import routes_shorts

        app.register_blueprint(routes_shorts)

    elif "aws" in routes_item:
        from module_aws.routes_aws import routes_aws

        app.register_blueprint(routes_aws)
    elif "linkview" in routes_item:
        import importlib

        targets = ["__init__.py", "models.py"]

        def register_linkview_routes():
            module_path = os.path.join(os.path.dirname(__file__), "module_linkview")
            for filename in os.listdir(module_path):
                if filename.endswith(".py") and any(condition in filename for condition in targets) == False:
                    module_name = f"module_linkview.{filename[:-3]}"
                    module = importlib.import_module(module_name)
                    blueprint = getattr(module, module_name.split(".")[-1])
                    app.register_blueprint(blueprint)

        register_linkview_routes()
        # def register_linkview_routes():
        #     modules = ["module_linkview.routes_device_v1", "module_linkview.routes_device_v2", "module_linkview.routes_linkview"]
        #     for module_name in modules:
        #         module = importlib.import_module(module_name)
        #         blueprint = getattr(module, module_name.split(".")[-1])
        #         app.register_blueprint(blueprint)

        # register_linkview_routes()

    elif "db" in routes_item:
        if db_name == EnumDB.MARIADB.value:
            from flask_mysqldb import MySQL

            MYSQL_HOST = os.getenv("MYSQL_HOST")
            MYSQL_PORT = os.getenv("MYSQL_PORT")
            MYSQL_USER = os.getenv("MYSQL_USER")
            MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
            MYSQL_DB = os.getenv("MYSQL_DB")
            app.config["MYSQL_HOST"] = MYSQL_HOST
            app.config["MYSQL_PORT"] = int(MYSQL_PORT)
            app.config["MYSQL_USER"] = MYSQL_USER
            app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
            app.config["MYSQL_DB"] = MYSQL_DB
            mysql = MySQL(app)
            # RuntimeError: Working outside of application context.
            app.app_context().push()
            connection = mysql.connection
            app.connection = connection

            app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            # app.config["SQLALCHEMY_ECHO"] = True  # SQL 쿼리 로깅 활성화
            db.init_app(app)
            with app.app_context():
                db.create_all()
            app.db = db

        else:
            import sqlite3

            SQLITE_DB_PATH = config.SQLITE_DB_PATH
            connection = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
            app.connection = connection

            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE_DB_PATH}"
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            # pip install sqlparse
            # app.config["SQLALCHEMY_ECHO"] = True  # SQL 쿼리 로깅 활성화
            db.init_app(app)
            with app.app_context():
                db.create_all()
            app.db = db


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

# fmt: off
include_url = [
    {"url": "tb_device_info", "methods": ["POST", "PUT", "DELETE"]},
    {"url": "tb_unit_info", "methods": ["POST", "PUT", "DELETE"]},
    {"url": "tb_port_info", "methods": ["POST", "PUT", "DELETE"]},
]
# fmt: on


@app.before_request
def before_request():
    if request.is_json:
        method_name = request.method.upper()
        if method_name in ["POST", "PUT"]:
            data_json = request.get_json()
            data_snake = {cmmfun.camel_to_snake(k): v for k, v in data_json.items()}
            g.data = data_snake
        elif method_name == "GET":
            data_snake = {cmmfun.camel_to_snake(key): value for key, value in request.args.items()}
            g.data = data_snake
        elif method_name == "DELETE":
            data_json = request.get_json()
            data_snake = {cmmfun.camel_to_snake(k): v for k, v in data_json.items()}
            g.data = data_snake
        # for item in include_url:
        #     if item["url"] in str(request.url) and request.method in item["methods"]:
        #         try:
        #             request_data = request.get_json()
        #             print(f"{datetime.now()} [{request.method}] {request.url.replace(request.host_url, "")}")
        #             print(json.dumps(request_data, indent=2, ensure_ascii=False))
        #         except json.JSONDecodeError:
        #             print(f"Invalid JSON response for URL: {request.url}")
        #             pass


@app.after_request
def after_request(response):

    if response.is_json:
        response_data = response.get_json()
        if "data" in response_data:
            if type(response_data["data"]) != list:
                response_data["data"] = {cmmfun.snake_to_camel(k): v for k, v in response_data["data"].items()}

                if type(response_data["data"].get("list")) == list:
                    response_data["data"]["list"] = [{cmmfun.snake_to_camel(k): v for k, v in item.items()} for item in response_data["data"]["list"]]
                    response_date_list = response_data["data"]["list"]
                    for idx, item in enumerate(response_date_list, 0):
                        item_val = {cmmfun.snake_to_camel(k): v for k, v in item.items()}
                        if "frontDeviceIdInfo" in item_val:
                            item_val["frontDeviceIdInfo"] = {cmmfun.snake_to_camel(k): v for k, v in item_val["frontDeviceIdInfo"].items()}
                            response_date_list[idx] = item_val

                response.set_data(json.dumps(response_data))
            else:
                response_data["data"] = [{cmmfun.snake_to_camel(k): v for k, v in item.items()} for item in response_data["data"]]
                response.set_data(json.dumps(response_data))

    # for item in include_url:
    #     if item["url"] in str(request.url) and request.method in item["methods"]:
    #         try:
    #             response_data = response.get_json()
    #             print(f"Method: {request.method}, URL: {request.url}")
    #             print(json.dumps(response_data.get("data"), indent=2, ensure_ascii=False))
    #         except json.JSONDecodeError:
    #             print(f"Invalid JSON response for URL: {request.url}")
    #             pass
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
