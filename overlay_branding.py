import argparse
import os
import shutil
import subprocess
import tempfile
import urllib.request


def _download_logo(url: str) -> str:
    tmp_dir = tempfile.mkdtemp(prefix="logo_")
    local_path = os.path.join(tmp_dir, "logo")
    with urllib.request.urlopen(url) as response, open(local_path, "wb") as f:
        shutil.copyfileobj(response, f)
    return local_path


def _resolve_font(font_path: str | None) -> str:
    if font_path:
        if not os.path.isfile(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")
        return font_path

    # macOS common fonts (best-effort)
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Helvetica.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        "No default font found. Provide --font with a path to a .ttf file."
    )


def _escape_drawtext(text: str) -> str:
    # Escape for ffmpeg drawtext: backslash, colon, single quote
    return (
        text.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a top logo overlay and bottom text to a video."
    )
    parser.add_argument("--input", required=True, help="Input video file path")
    parser.add_argument("--output", required=True, help="Output video file path")
    parser.add_argument(
        "--logo",
        required=True,
        help="Logo file path or URL (http/https)",
    )
    parser.add_argument("--text", required=True, help="Bottom text to display")
    parser.add_argument("--font", help="Path to a .ttf font file")
    parser.add_argument("--font-size", type=int, default=36, help="Font size in px")
    parser.add_argument(
        "--font-color",
        default="white",
        help="Font color (ffmpeg color value)",
    )
    parser.add_argument(
        "--logo-width",
        type=int,
        default=220,
        help="Logo width in px (height auto)",
    )
    parser.add_argument(
        "--top-margin",
        type=int,
        default=20,
        help="Top margin for logo in px",
    )
    parser.add_argument(
        "--bottom-margin",
        type=int,
        default=30,
        help="Bottom margin for text in px",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"Input video not found: {args.input}")

    logo_path = args.logo
    temp_logo_dir = None
    if args.logo.startswith("http://") or args.logo.startswith("https://"):
        temp_logo_path = _download_logo(args.logo)
        temp_logo_dir = os.path.dirname(temp_logo_path)
        logo_path = temp_logo_path
    elif not os.path.isfile(args.logo):
        raise FileNotFoundError(f"Logo file not found: {args.logo}")

    font_path = _resolve_font(args.font)

    safe_text = _escape_drawtext(args.text)
    drawtext = (
        "drawtext="
        f"fontfile={font_path}:"
        f"text='{safe_text}':"
        f"fontcolor={args.font_color}:"
        f"fontsize={args.font_size}:"
        "x=(w-text_w)/2:"
        f"y=h-text_h-{args.bottom_margin}"
    )

    filter_complex = (
        f"[1]scale={args.logo_width}:-1[logo];"
        f"[0][logo]overlay=x=(W-w)/2:y={args.top_margin},{drawtext}"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        args.input,
        "-i",
        logo_path,
        "-filter_complex",
        filter_complex,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "copy",
        args.output,
    ]

    try:
        subprocess.run(cmd, check=True)
    finally:
        if temp_logo_dir:
            shutil.rmtree(temp_logo_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
