#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-input.mp3}"
OUT_DIR="${2:-audio}"
DURATION="${3:-5}"

if [[ ! -f "$INPUT" ]]; then
  echo "Input not found: $INPUT" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# Split into fixed-length segments. Re-encode for consistent timing.
ffmpeg -y -i "$INPUT" \
  -f segment \
  -segment_time "$DURATION" \
  -reset_timestamps 1 \
  -c:a aac -b:a 192k \
  "$OUT_DIR/clip_%03d.m4a"

echo "Done: $OUT_DIR"
