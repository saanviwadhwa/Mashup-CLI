from flask import Flask, render_template, request
import yt_dlp
from moviepy import VideoFileClip
from pydub import AudioSegment
import os
import zipfile
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


# ------------------------------
# Generate Mashup
# ------------------------------
def generate_mashup(singer, count, duration):
    video_files = []

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "video_%(id)s.%(ext)s",
        "noplaylist": True,
        "merge_output_format": "mp4",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_query = f"ytsearch{count}:{singer}"
        info = ydl.extract_info(search_query, download=True)

        for entry in info["entries"]:
            filename = ydl.prepare_filename(entry)
            if not filename.endswith(".mp4"):
                filename = os.path.splitext(filename)[0] + ".mp4"
            video_files.append(filename)

    # Convert + Trim
    combined = AudioSegment.empty()

    for video in video_files:
        clip = VideoFileClip(video)
        audio_name = os.path.splitext(video)[0] + ".mp3"
        clip.audio.write_audiofile(audio_name, logger=None)
        clip.close()

        sound = AudioSegment.from_file(audio_name)
        trimmed = sound[:duration * 1000]
        combined += trimmed

    output_file = "mashup.mp3"
    combined.export(output_file, format="mp3")

    return output_file


# ------------------------------
# Send Email
# ------------------------------
def send_email(receiver_email, file_path):

    sender_email = "swadhwa_be23@thapar.edu"
    sender_password = "amayazirkachlajd"

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Your mashup file is attached.")

    # Zip the file
    zip_name = "mashup.zip"
    with zipfile.ZipFile(zip_name, "w") as zipf:
        zipf.write(file_path)

    with open(zip_name, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename=zip_name
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


# ------------------------------
# Flask Routes
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        singer = request.form["singer"]
        count = int(request.form["count"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        try:
            output = generate_mashup(singer, count, duration)
            send_email(email, output)
            message = "Mashup generated and sent to email!"
        except Exception as e:
            message = f"Error: {e}"

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
