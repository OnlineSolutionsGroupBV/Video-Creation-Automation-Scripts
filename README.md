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

### `overlay_branding.py`

Adds a top logo overlay and text under the logo. The logo can be a local file or a URL.

```bash
python overlay_branding.py \
  --input input.mp4 \
  --output output.mp4 \
  --logo https://onlinesolutionsgroup.website/img/logo-transparent.png \
  --text onlinesolutionsgroup.website
```

Inline example:
`python3 overlay_branding.py --input input.mp4 --output output.mp4 --logo https://onlinesolutionsgroup.website/img/logo-transparent.png --text onlinesolutionsgroup.website --font-size 36 --font-color white --logo-width 220 --top-margin 20 --bottom-margin 30`

Working example (local logo):
`python3 overlay_branding.py --input input.mp4 --output output.mp4 --logo logo.png --text onlinesolutionsgroup.website --font-size 36 --font-color white --logo-width 220 --top-margin 60 --bottom-margin 30`

Optional flags:
- `--font /path/to/font.ttf`
- `--font-size 36`
- `--font-color white`
- `--logo-width 220`
- `--top-margin 20`
- `--bottom-margin 30`
- `--text-margin 12`
- `--text-position top|bottom`

---

## ⚙ FFmpeg Path Configuration

For macOS or custom FFmpeg setups, you may need to set the binary paths at the top of your script:

```python
import os
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPLAY_BINARY"] = "/usr/local/bin/ffplay"
```

---

## 🎛 Metadata Commands

Show metadata (JSON):
`ffprobe -v error -show_format -show_streams -of json input.mp4`

Edit metadata (inline):
`ffmpeg -y -i output.mp4 -c copy -metadata title="Mijn Titel" -metadata artist="Online Solutions Group" -metadata comment="Beschrijving" output-meta.mp4`

---

## 🔁 One-Command Pipeline (Config Driven)

Edit `config.json`, then run:
`bash pipeline.sh`

This will:
- Create a branded video at the `branded_output` path (e.g. `output.mp4`)
- Create a final video with updated metadata at the `final_output` path (e.g. `output-meta.mp4`)

Config fields (defaults in `config.json`):
- `input`: input video (e.g. `input.mp4`)
- `branded_output`: output after branding (e.g. `output.mp4`)
- `final_output`: output after metadata update (e.g. `output-meta.mp4`)
- `logo`: logo file path or URL
- `text`: bottom text
- `font`: path to `.ttf` (empty = default)
- `font_size`, `font_color`, `logo_width`, `top_margin`, `bottom_margin`, `text_position`
- `text_margin`
- `metadata.title`, `metadata.artist`, `metadata.comment`

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
