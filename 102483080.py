import sys
import os
import yt_dlp
from moviepy import VideoFileClip
from pydub import AudioSegment

def download_videos(singer, count):
    downloaded_files = []

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "video_%(id)s.%(ext)s",
        "noplaylist": True,
        "merge_output_format": "mp4",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch{count}:{singer}"
            info = ydl.extract_info(search_query, download=True)

            for entry in info["entries"]:
                filename = ydl.prepare_filename(entry)
                if not filename.endswith(".mp4"):
                    filename = os.path.splitext(filename)[0] + ".mp4"
                downloaded_files.append(filename)

        return downloaded_files

    except Exception as e:
        print("Error downloading videos:", e)
        sys.exit(1)


def convert_to_audio(video_files):
    audio_files = []

    for video in video_files:
        try:
            clip = VideoFileClip(video)
            audio_name = os.path.splitext(video)[0] + ".mp3"
            clip.audio.write_audiofile(audio_name, logger=None)
            clip.close()
            audio_files.append(audio_name)
        except Exception as e:
            print(f"Error converting {video}:", e)

    return audio_files

# -----------------------------
def trim_audios(audio_files, seconds):
    trimmed_files = []

    for audio in audio_files:
        try:
            sound = AudioSegment.from_file(audio)
            trimmed = sound[:seconds * 1000]
            trimmed_name = os.path.splitext(audio)[0] + "_trimmed.mp3"
            trimmed.export(trimmed_name, format="mp3")
            trimmed_files.append(trimmed_name)
        except Exception as e:
            print(f"Error trimming {audio}:", e)

    return trimmed_files

def merge_audios(audio_files, output_name):
    try:
        combined = AudioSegment.empty()

        for audio in audio_files:
            sound = AudioSegment.from_file(audio)
            combined += sound

        combined.export(output_name, format="mp3")
        print("\nMashup created successfully:", output_name)

    except Exception as e:
        print("Error merging audio:", e)
        sys.exit(1)

def main():
    if len(sys.argv) != 5:
        print("\nUsage:")
        print("python <rollno>.py <SingerName> <NumberOfVideos> <DurationSeconds> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("NumberOfVideos and DurationSeconds must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 0 or duration <= 0:
        print("NumberOfVideos and DurationSeconds must be positive.")
        sys.exit(1)

    print("\nDownloading videos...")
    videos = download_videos(singer, num_videos)

    print("Converting to audio...")
    audios = convert_to_audio(videos)

    print("Trimming audio...")
    trimmed = trim_audios(audios, duration)

    print("Merging audio files...")
    merge_audios(trimmed, output_file)


if __name__ == "__main__":
    main()
