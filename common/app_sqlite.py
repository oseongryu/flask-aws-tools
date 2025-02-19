from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# SQLite
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
# No module named 'mysql'
# pip install mysql-connector-python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:1234@localhost:3306/testdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class OriginInfo(db.Model):
    story_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    origin_content = db.Column(db.Text, nullable=True)
    origin_title = db.Column(db.String(255), nullable=True)
    origin_url = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.String(255), nullable=True)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    no = db.Column(db.String(255), nullable=True)
    sound_path = db.Column(db.String(255), nullable=True)
    story_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.String(255), nullable=True)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/origininfo", methods=["POST"])
def create_origininfo():
    data = request.get_json()
    new_origininfo = OriginInfo(story_id=data["story_id"], content=data["content"], origin_content=data["origin_content"], origin_title=data["origin_title"], origin_url=data["origin_url"], title=data["title"])
    db.session.add(new_origininfo)
    db.session.commit()
    return jsonify({"message": "OriginInfo created"}), 201


@app.route("/origininfo/<int:story_id>", methods=["GET"])
def get_origininfo(story_id):
    origininfos = OriginInfo.query.filter_by(story_id=story_id).all()
    return jsonify(
        [
            {"story_id": origininfo.story_id, "content": origininfo.content, "origin_content": origininfo.origin_content, "origin_title": origininfo.origin_title, "origin_url": origininfo.origin_url, "title": origininfo.title}
            for origininfo in origininfos
        ]
    )


@app.route("/origininfo/<int:story_id>", methods=["DELETE"])
def delete_origininfo(story_id):
    origininfo = OriginInfo.query.get_or_404(story_id)
    db.session.delete(origininfo)
    db.session.commit()
    return jsonify({"message": "OriginInfo deleted"})


@app.route("/stories", methods=["POST"])
def create_story():
    data = request.get_json()
    new_story = Story(content=data["content"], height=data["height"], image_path=data["image_path"], no=data["no"], sound_path=data["sound_path"], story_id=data["story_id"])
    db.session.add(new_story)
    db.session.commit()
    return jsonify({"message": "Story created"}), 201


@app.route("/stories/<int:story_id>", methods=["GET"])
def get_story(story_id):
    stories = Story.query.filter_by(story_id=story_id).all()
    return jsonify([{"id": story.id, "content": story.content, "height": story.height, "image_path": story.image_path, "no": story.no, "sound_path": story.sound_path, "story_id": story.story_id} for story in stories])


@app.route("/stories/<int:story_id>", methods=["DELETE"])
def delete_story(story_id):
    story = Story.query.filter_by(story_id=story_id).first_or_404()
    db.session.delete(story)
    db.session.commit()
    return jsonify({"message": "Story deleted"})


if __name__ == "__main__":
    # app.app_context().push()

    with app.app_context():
        db.create_all()
    app.run(debug=True)
