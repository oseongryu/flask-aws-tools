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

# sys.path.append(os.path.join(os.path.dirname(__file__), "aws"))
# sys.path.append(os.path.join(os.path.dirname(__file__), "common"))


app = Flask(__name__, template_folder="templates", static_url_path="/static", static_folder="static")

load_dotenv()
app.register_blueprint(routes_aws)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8091)
