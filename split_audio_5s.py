#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split an audio file into fixed-length clips (default 5s)."
    )
    parser.add_argument("input", nargs="?", default="input.mp3", help="Input file")
    parser.add_argument(
        "--out-dir", default="audio", help="Output directory for clips"
    )
    parser.add_argument(
        "--duration", type=float, default=5.0, help="Clip duration in seconds"
    )
    parser.add_argument(
        "--format",
        choices=["mp3", "m4a"],
        default="mp3",
        help="Output format",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        raise SystemExit(f"Input not found: {input_path}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.format == "mp3":
        ext = "mp3"
        codec = ["-c:a", "libmp3lame", "-b:a", "192k"]
    else:
        ext = "m4a"
        codec = ["-c:a", "aac", "-b:a", "192k"]

    # Re-encode for consistent segment timing.
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-f",
        "segment",
        "-segment_time",
        f"{args.duration:.3f}",
        "-reset_timestamps",
        "1",
        *codec,
        str(out_dir / f"clip_%03d.{ext}"),
    ]
    run(cmd)

    print(f"Done: {out_dir}")


if __name__ == "__main__":
    main()
