from flask import Flask, render_template, request, send_from_directory
import json
from os import path, getcwd
from controller import download as yt_download, get_download_status, ytdl_logger, get_downloaded_items

app = Flask(__name__)


def init_download(request):
    reqData = json.loads(request.data.decode())
    video_id = reqData.get("video_id")
    if video_id:
        # TODO: add 'cancel download'
        yt_download(video_id)
        return json.dumps({"success": True})
    else:
        return "Couldn't parse video url", 400


def send_download_status():
    download_status = get_download_status()
    if download_status:
        return json.dumps({
            "success": True,
            "state": download_status.state,
            "percentage_done": download_status.percentage_done,
            "size_done": download_status.size_done,
            "speed": download_status.speed,
            "eta": download_status.eta,
            "filename": ytdl_logger.download_name
        })
    return '{"success": false}', 204


@app.route("/", methods=["GET"])
def index():
    # TODO: add links to recently downloaded
    return render_template("index.html", downloaded_videos=get_downloaded_items())


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == 'POST':
        return init_download(request)
    else:
        return send_download_status()


@app.route("/downloads/<path:filename>")
def download_file(filename):
    downloads_folder = path.join(getcwd(), "downloads")
    return send_from_directory(downloads_folder, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
