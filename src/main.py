from flask import Flask, render_template, request
from controller import download

app = Flask(__name__)


@app.route("/")
def index():
    video_url = request.args.get("url")
    if video_url:
        download(video_url)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
