from youtube_dl import YoutubeDL
from os import getcwd, path
import re
from collections import namedtuple
from logger import Logger


DownloadStatus = namedtuple(
    "download_status", ("state", "percentage_done", "size_done", "speed", "eta",))


ytdl_logger = Logger()

current_dir = getcwd()
downloads_dir = path.join(current_dir, "downloads/")
out_template = downloads_dir + "%(title)s-%(id)s.%(ext)s"

ytdl = YoutubeDL({"outtmpl": out_template, "logger": ytdl_logger})


def download(yt_id):
    ytdl.download([yt_id])


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
