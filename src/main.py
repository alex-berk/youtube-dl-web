from flask import Flask, render_template, request, send_from_directory
import json
from os import path, getcwd
from controller import download as yt_download, get_download_status, get_downloaded_items

app = Flask(__name__)


def init_download(request):
    reqData = json.loads(request.data.decode())
    video_id = reqData.get("video_id")
    download_format = reqData.get("download_format")
    if video_id:
        # TODO: add 'cancel download'
        yt_download(video_id, download_format)
        return json.dumps({"success": True})
    else:
        return "Couldn't parse video url", 400


def send_download_status():
    download_status = get_download_status()
    if download_status:
        return json.dumps(
            {"success": True,
             "state": download_status.get("status", None),
             "percentage_done": download_status.get("percent_str", None),
             "size_done": download_status.get("downloaded_bytes", None),
             "size_total": download_status.get("total_bytes_str", None),
             "speed": download_status.get("speed_str", None),
             "eta": download_status.get("eta_str", None),
             "elapsed": download_status.get("elapsed", None),
             "filename": download_status.get("filename", None)}
        )
    return '{"success": false}', 204


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", downloaded_videos=get_downloaded_items()[:11])


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == 'POST':
        return init_download(request)
    else:
        return send_download_status()


@app.route("/downloads")
def downloads():
    return render_template("downloads.html", downloaded_videos=get_downloaded_items())


@app.route("/downloads/<path:filename>")
def download_file(filename):
    downloads_folder = path.join(getcwd(), "downloads")
    return send_from_directory(downloads_folder, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
