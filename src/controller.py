from youtube_dl import YoutubeDL
from os import getcwd, path, listdir
import re
from collections import namedtuple
from logger import Logger

ytdl_logger = Logger()

download_state = {}


def processFilename(filename):
    format, extension = filename.split(".")[-2:]
    if format[0] == "f" and format[1:].isnumeric():
        filename = filename.replace(f".{format}", "")
    return filename.split("/")[-1]


def update_download_state(message: dict) -> dict:
    formatted_message = {k if not k.startswith(
        "_") else k[1:]: v for k, v in message.items()}
    formatted_message["filename"] = processFilename(
        formatted_message["filename"])
    # good sign that this thing should be a class
    global download_state
    download_state = formatted_message


current_dir = getcwd()
downloads_dir = path.join(current_dir, "downloads/")
out_template = downloads_dir + "%(title)s-%(id)s.%(ext)s"

# check "listformats" and "merge_output_format"
format_mapping = {
    "audio": "140",
    "default": "best",
    "2160p": "401+140",
    "1440p": "400+140",
    "1080p": "137+140",
    "1080p60fps": "299+140",
    "720p60fps": "298+140",
    "480p": "135+140",
    "360p": "134+250",
    "240p": "133+249",
    "144p": "160+249",
}


ytdl_options = {
    "outtmpl": out_template,
    "logger": ytdl_logger,
    "progress_hooks": (update_download_state,),
}
ytdl = YoutubeDL(ytdl_options)


def download(yt_id, download=None):
    video_format = format_mapping[download or "default"]
    ytdl.params["format"] = video_format
    ytdl.download([yt_id])


def get_download_status():
    return download_state


def get_downloaded_items():
    downloads_files = listdir(downloads_dir)
    downloads_vids = list(
        filter(lambda f: f.endswith(".mp4") and not f.startswith("."), downloads_files))
    downloads_vids.sort(
        key=lambda x: path.getctime(path.join(downloads_dir, x)), reverse=True)
    return downloads_vids
