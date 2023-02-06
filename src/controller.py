from youtube_dl import YoutubeDL
from os import getcwd, path, listdir
import re
import json
from collections import namedtuple
import multiprocessing
from logger import Logger

running_jobs = {}

DownloadStatus = namedtuple(
    "download_status", ("state", "percentage_done", "size_done", "speed", "eta",))

# TODO: check "listformats" and "merge_output_format"
format_mapping = {
    "default": "best",
    "2160p": "401+140",
    "1440p": "400+140",
    "1080p": "137+140",
    "1080p60fps": "299+140",
    "720p60fps": "298+140",
    "480p": "135+140",
    "360p": "134+140",
    "240p": "133+140",
    "144p": "160+140",
}


ytdl_logger = Logger()

current_dir = getcwd()
downloads_dir = path.join(current_dir, "downloads/")
out_template = downloads_dir + "%(title)s-%(id)s.%(ext)s"

ytdl = YoutubeDL({"outtmpl": out_template, "logger": ytdl_logger})


def download(yt_id, download=None):
    video_format = format_mapping[download or "default"]
    ytdl.params["format"] = video_format
    process = multiprocessing.Process(target=ytdl.download, args=([yt_id,],))
    running_jobs[yt_id] = process
    running_jobs[yt_id].start()


def cancel_download(request):
    reqData = json.loads(request.data.decode())
    yt_id = reqData.get("video_id")
    try:
        running_jobs.pop(yt_id).terminate()
        return json.dumps({"success": True})
    except KeyError:
        return '{"success": false}', 204


# TODO: check progress_hooks, dump_single_json
def parse_download_status(message):
    pattern = re.compile(
        r".*\[(\w+)\] +([\d\.]+%) of ([\d\.]+\w+) at ([\d\.]+\w+)\/s ETA (\d{2}:\d{2})")
    match = re.match(pattern, message)
    if match:
        download_status = DownloadStatus(*match.groups())
        return download_status
    if "[download] 100" in message or "[download] 100.0%" in message:
        return DownloadStatus("completed", "100.0%", "", "", "",)
    return None


def get_download_status():
    return parse_download_status(ytdl_logger.latest_message)


def get_downloaded_items():
    downloads_files = listdir(downloads_dir)
    downloads_vids = list(
        filter(lambda f: f.endswith(".mp4") and not f.startswith("."), downloads_files))
    downloads_vids.sort(
        key=lambda x: path.getctime(path.join(downloads_dir, x)), reverse=True)
    return downloads_vids
