from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# In-memory storage for tweets
tweets = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(url_for("tweet"))
    return render_template("index.html", tweets=tweets)


@app.route("/tweet", methods=["POST"])
def tweet():
    if "tweetText" not in request.form:
        return "Tweet text is missing", 400

    content = request.form.get("tweetText")
    image = request.files.get("imageUpload")
    video = request.files.get("videoUpload")

    if not content:
        return "Content is required", 400

    image_filename = None
    video_filename = None

    if image and image.filename:
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

    if video and video.filename:
        video_filename = secure_filename(video.filename)
        video.save(os.path.join(app.config["UPLOAD_FOLDER"], video_filename))

    new_tweet = {
        "username": "DefaultUser",
        "content": content,
        "image": image_filename,
        "video": video_filename,
        "timestamp": datetime.now(),
    }

    tweets.append(new_tweet)

    return redirect(url_for("index"))


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
