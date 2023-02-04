from flask import Flask, render_template, request
from controller import download as yt_download, get_download_status
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
        download_status = get_download_status()
        if download_status:
            return json.dumps({
                "success": True,
                "status": download_status.state,
                "percentage_done": int(download_status.percentage_done),
                "size_done": download_status.size_done,
                "speed": download_status.speed,
                "eta": download_status.eta,
            })


if __name__ == "__main__":
    app.run()
