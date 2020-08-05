from flask_sqlalchemy import SQLAlchemy
from api import app
from datetime import datetime
from exception import NoSuchItemException

db = SQLAlchemy(app)


class Result(db.Model):
    id = db.Column(db.String, primary_key=True)
    finished = db.Column(db.Boolean, default=False)
    progress = db.Column(db.Float, nullable=False, default=0.0)
    success = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.String, default="")
    audio = db.Column(db.String, default="")
    date = db.Column(db.DateTime, default=datetime.utcnow)


db.create_all()


def _get_item(id):
    item = Result.query.get(id)
    return item


def create_item(id):
    item = Result(id=id)
    db.session.add(item)
    db.session.commit()


def delete_item(id):
    item = _get_item(id)
    if item is not None:
        db.session.delete(item)
        db.session.commit()
    else:
        raise NoSuchItemException("项目已被删除")


def set_progress(id, progress):
    item = _get_item(id)
    if item is None:
        raise NoSuchItemException("找不到此项目")
    item.progress = progress
    db.session.commit()


def get_progress(id):
    item = _get_item(id)
    if item is None:
        raise NoSuchItemException("找不到此项目")
    result = {
        "finished": item.finished,
        "progress": item.progress
    }
    return result


def set_result(id, audio, success, error_message):
    item = _get_item(id)
    if item is None:
        raise NoSuchItemException("找不到此项目")
    else:
        item.progress = 1.0
        item.audio = audio
        item.success = success
        item.error_message = error_message
        item.finished = True
        db.session.commit()


def get_result(id):
    item = _get_item(id)
    if item is None:
        raise NoSuchItemException("找不到此项目")
    if item.finished:
        result = {
            "synthesis_successful": item.success,
            "message": [x for x in item.error_message.split(";") if x != ""],
            "audio": item.audio
        }
    else:
        raise Exception("项目仍在合成")
    return result
