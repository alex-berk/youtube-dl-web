from flask import Flask, render_template, request
from controller import download as yt_download, get_download_status
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # TODO: add links to recently downloaded
    return render_template("index.html")


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == 'POST':
        reqData = json.loads(request.data.decode())
        video_id = reqData.get("video_id")
        if video_id:
            # TODO: add 'cancel download'
            yt_download(video_id)
            return json.dumps({"success": True})
        else:
            return "Couldn't parse video url", 400
    else:
        download_status = get_download_status()
        # TODO: add a link to the video on success
        if download_status:
            return json.dumps({
                "success": True,
                "state": download_status.state,
                "percentage_done": download_status.percentage_done,
                "size_done": download_status.size_done,
                "speed": download_status.speed,
                "eta": download_status.eta,
            })
        return '{"success": false}', 204


if __name__ == "__main__":
    app.run(host="0.0.0.0")
