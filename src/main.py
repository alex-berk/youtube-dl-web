from flask import Flask, render_template, request
from controller import download as yt_download
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == 'POST':
        reqData = json.loads(request.data.decode())
        video_id = reqData.get("video_id")
        if video_id:
            yt_download(video_id)
            return json.dumps({"success": True})
        else:
            return "Couldn't parse video url", 400
    else:
        return "bad request", 400


if __name__ == "__main__":
    app.run()
