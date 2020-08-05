from flask import Flask, request
from flask_cors import CORS
from uuid import uuid1
from threading import Thread, Timer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from database import delete_item, get_result, get_progress, set_result, create_item, set_progress
from xispeech import XiSpeechSynthesizer

s = XiSpeechSynthesizer()  # load and arrange audio files
CORS(app)
print("初始化完成")


class TaskManipulator:
    threads = {}

    class MyThread(Thread):
        def __init__(self, text, request_id):
            super().__init__()
            self.text = text
            self.request_id = request_id
            self.synthesizer = XiSpeechSynthesizer()

        def run(self):
            create_item(self.request_id)
            self.synthesizer = XiSpeechSynthesizer()
            self.update_progress()
            self.synthesizer.create_and_store_encoded_audio(self.text)
            TaskManipulator.delete(self.request_id)

        def update_progress(self):
            def func_wrapper():
                if not self.synthesizer.stop:
                    set_progress(self.request_id, self.synthesizer.progress)
                    if self.synthesizer.progress < 1:
                        self.update_progress()
                    else:
                        set_result(self.request_id, self.synthesizer.result, True, self.synthesizer.error)

            t = Timer(0.25, func_wrapper)
            t.start()

    @staticmethod
    def kill(request_id):
        if request_id in TaskManipulator.threads:
            TaskManipulator.threads[request_id].synthesizer.stop = True
            del TaskManipulator.threads[request_id]

    @staticmethod
    def delete(request_id):
        if request_id in TaskManipulator.threads:
            del TaskManipulator.threads[request_id]

    @staticmethod
    def start(text, request_id):
        TaskManipulator.threads[request_id] = TaskManipulator.MyThread(text, request_id)
        TaskManipulator.threads[request_id].start()


@app.route("/task", methods=['POST'])
def create():
    json = request.get_json()
    if json is not None and "text" in json:
        request_id = str(uuid1())
        text = json["text"]
        if len(text) > 1000:
            result = {
                "request_successful": False,
                "message": "文本不得超过1000字"
            }
            return result
        try:
            TaskManipulator.start(text, request_id)
            result = {
                "request_successful": True,
                "id": request_id
            }
        except Exception as e:
            result = {
                "request_successful": False,
                "message": str(e)
            }
    else:
        result = {
            "request_successful": False,
            "message": "文本缺失"
        }
    return result


@app.route("/progress", methods=['GET'])
def query_progress():
    request_id = request.args.get("id", "")
    try:
        result = {
            "request_successful": True,
            "result": get_progress(request_id)
        }
    except Exception as e:
        result = {
            "request_successful": False,
            "message": str(e)
        }
    return result


@app.route("/result", methods=['GET'])
def query_result():
    request_id = request.args.get("id", "")
    try:
        result = {
            "request_successful": True,
            "result": get_result(request_id)
        }
    except Exception as e:
        result = {
            "request_successful": False,
            "message": str(e)
        }
    return result


@app.route("/result", methods=['DELETE'])
def delete_result():
    request_id = request.args.get("id", "")
    try:
        TaskManipulator.kill(request_id)
        delete_item(request_id)
        result = {
            "request_successful": True
        }
    except Exception as e:
        result = {
            "request_successful": False,
            "message": str(e)
        }
    return result
