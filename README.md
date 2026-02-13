Here is your **final README** with proper Markdown formatting and black code blocks.
You can copy-paste this directly into your `README.md` file on GitHub.

---

# Mashup Generator – Command Line Program

This project is a command-line based mashup generator that performs the following operations:

* Downloads **N YouTube videos** of a given singer
* Extracts audio from each video
* Trims the first **Y seconds** from each audio file
* Merges all trimmed audio files into one final mashup

---

## How to Run the Program

```bash
python <RollNumber>.py "<Singer Name>" <NumberOfVideos> <DurationSeconds> <OutputFileName>
```

### Example

```bash
python 102483080.py "Sharry Maan" 20 20 101556-output.mp3
```

---

## Parameter Description

### Singer Name

Name of the artist to search on YouTube.
If the name contains spaces, it must be written inside double quotes.

### NumberOfVideos

Number of YouTube videos to download.
Must be a positive integer.

### DurationSeconds

Number of seconds to trim from the beginning of each audio file.
Must be a positive integer.

### OutputFileName

Name of the final merged MP3 file.

---

## Functional Workflow

1. The program searches YouTube for the specified singer.
2. Downloads the requested number of videos.
3. Converts each video into MP3 format.
4. Trims the first specified number of seconds from each audio file.
5. Merges all trimmed audio clips into one final audio file.
6. Saves the merged mashup with the provided output filename.

---

## Technologies Used

* Python 3.12
* yt-dlp (YouTube downloading)
* MoviePy (audio extraction)
* Pydub (audio trimming and merging)
* FFmpeg (audio processing backend)

---

## Installation Requirements

Install required packages:

```bash
pip install yt-dlp moviepy pydub
```

Ensure **FFmpeg** is installed and added to the system PATH.

---

## Error Handling

The program validates:

* Correct number of command-line arguments
* Integer validation for number of videos and duration
* Positive value validation
* Download and processing exceptions

Appropriate error messages are displayed if invalid input is provided.

---

## Example Execution

```bash
python 102483080.py "Sharry Maan" 14 20 final_output.mp3
```

This command will:

* Download 14 videos of Sharry Maan
* Trim the first 20 seconds from each video
* Merge all trimmed clips
* Save the final mashup as final_output.mp3

---

## Author

Saanvi Wadhwa
