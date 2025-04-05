# 🎮 Video Creation Automation Scripts

This repository contains a set of Python scripts designed to automate basic video editing tasks using python and ffmpeg. It supports:

- ✅ Converting `.AVI` video files to `.MP4`
- ✅ Concatenating multiple video clips into one
- ✅ Basic handling of video and audio tracks
- ✅ Useful for quickly generating compilation videos or cleaning up camera exports

---

## 🧹 Features

- 🔄 **Automatic format conversion** (AVI → MP4)
- 🎞 **Smart concatenation** of video clips (with audio preserved)
- 📂 **Glob-based file discovery** — no need to hardcode filenames
- 🔧 Built-in `ffmpeg` path config for macOS compatibility
- 💡 Clean and easy-to-extend codebase

---

## 👥 Requirements

- Python 3.7+
- [FFmpeg](https://ffmpeg.org/) installed and available at `/usr/local/bin/ffmpeg`

Install the required Python packages:

```bash
pip install moviepy
```

---

## 📁 Scripts

### `convert_avi_to_mp4.py`

Scans a folder for `.avi` files and converts them to `.mp4` using MoviePy and FFmpeg.

```bash
python convert_avi_to_mp4.py
```

> Outputs converted files to the same or specified folder.

---

### `merge_video.py`

Finds all `.mp4` files in a folder (e.g. `output/`) and concatenates them into a single video file (`merged_output.mp4`), preserving the audio.

```bash
python merge_video.py
```

> Uses `method="compose"` to ensure compatibility of clips with different dimensions or audio.

---

## ⚙ FFmpeg Path Configuration

For macOS or custom FFmpeg setups, you may need to set the binary paths at the top of your script:

```python
import os
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPLAY_BINARY"] = "/usr/local/bin/ffplay"
```

---

## 🛠 Future Ideas

- Add optional fade transitions between clips
- Watermark or overlay logo/text
- Batch process subfolders
- GUI or web interface

---

## 📄 License

This project is open-source and free to use under the [MIT License](LICENSE).

---

## 🤝 Contributing

Feel free to fork, submit pull requests, or suggest features via Issues.

## Blog post about use cases
[Automating Video Editing with Python](https://www.webdeveloper.today/2025/04/automating-video-editing-with-python.html)
https://www.webdeveloper.today/2025/04/automating-video-editing-with-python.html


