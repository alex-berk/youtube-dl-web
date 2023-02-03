from youtube_dl import YoutubeDL
from os import getcwd, path


current_dir = getcwd()
downloads_dir = path.join(current_dir, "downloads/")
out_template = downloads_dir + "%(id)s_%(title)s.%(ext)s"

# TODO: subscribe to progress -  check progress_hooks, dump_single_json
ytdl = YoutubeDL({"outtmpl": out_template, })


def download(yt_id):
    ytdl.download([yt_id])
