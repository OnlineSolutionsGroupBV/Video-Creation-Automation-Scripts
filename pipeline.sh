#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${1:-config.json}"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Config not found: $CONFIG_FILE" >&2
  exit 1
fi

read_json() {
  local key="$1"
  python3 - <<PY
import json
with open("$CONFIG_FILE", "r", encoding="utf-8") as f:
    data = json.load(f)
val = data
for part in "$key".split("."):
    val = val.get(part, "")
print("" if val is None else val)
PY
}

INPUT="$(read_json input)"
BRANDED_OUTPUT="$(read_json branded_output)"
FINAL_OUTPUT="$(read_json final_output)"
LOGO="$(read_json logo)"
TEXT="$(read_json text)"
FONT="$(read_json font)"
FONT_SIZE="$(read_json font_size)"
FONT_COLOR="$(read_json font_color)"
TEXT_BORDER_WIDTH="$(read_json text_border_width)"
TEXT_BORDER_COLOR="$(read_json text_border_color)"
AUDIO_FOLDER="$(read_json audio_folder)"
AUDIO_DURATION="$(read_json audio_duration)"
AUDIO_MODE="$(read_json audio_mode)"
AUDIO_VOLUME="$(read_json audio_volume)"
ORIGINAL_VOLUME="$(read_json original_volume)"
AUDIO_OUTPUT="$(read_json audio_output)"
LOGO_WIDTH="$(read_json logo_width)"
TOP_MARGIN="$(read_json top_margin)"
BOTTOM_MARGIN="$(read_json bottom_margin)"
TEXT_MARGIN="$(read_json text_margin)"
TEXT_POSITION="$(read_json text_position)"
META_TITLE="$(read_json metadata.title)"
META_ARTIST="$(read_json metadata.artist)"
META_COMMENT="$(read_json metadata.comment)"

if [[ -z "$INPUT" || -z "$BRANDED_OUTPUT" || -z "$FINAL_OUTPUT" ]]; then
  echo "Missing required config values (input/branded_output/final_output)." >&2
  exit 1
fi

if [[ -z "$TEXT_MARGIN" ]]; then
  TEXT_MARGIN="12"
fi
if [[ -z "$TEXT_POSITION" ]]; then
  TEXT_POSITION="top"
fi
if [[ -z "$TEXT_BORDER_WIDTH" ]]; then
  TEXT_BORDER_WIDTH="2"
fi
if [[ -z "$TEXT_BORDER_COLOR" ]]; then
  TEXT_BORDER_COLOR="gray"
fi
if [[ -z "$AUDIO_DURATION" ]]; then
  AUDIO_DURATION="5"
fi
if [[ -z "$AUDIO_MODE" ]]; then
  AUDIO_MODE="replace"
fi
if [[ -z "$AUDIO_VOLUME" ]]; then
  AUDIO_VOLUME="1.0"
fi
if [[ -z "$ORIGINAL_VOLUME" ]]; then
  ORIGINAL_VOLUME="1.0"
fi

if [[ "$BRANDED_OUTPUT" == */* ]]; then
  mkdir -p "$(dirname "$BRANDED_OUTPUT")"
fi
if [[ "$FINAL_OUTPUT" == */* ]]; then
  mkdir -p "$(dirname "$FINAL_OUTPUT")"
fi

BRAND_CMD=(
  python3 overlay_branding.py
  --input "$INPUT"
  --output "$BRANDED_OUTPUT"
  --logo "$LOGO"
  --text "$TEXT"
  --font-size "$FONT_SIZE"
  --font-color "$FONT_COLOR"
  --text-border-width "$TEXT_BORDER_WIDTH"
  --text-border-color "$TEXT_BORDER_COLOR"
  --logo-width "$LOGO_WIDTH"
  --top-margin "$TOP_MARGIN"
  --bottom-margin "$BOTTOM_MARGIN"
  --text-margin "$TEXT_MARGIN"
  --text-position "$TEXT_POSITION"
)

if [[ -n "$FONT" ]]; then
  BRAND_CMD+=(--font "$FONT")
fi

"${BRAND_CMD[@]}"

SOURCE_FOR_META="$BRANDED_OUTPUT"
if [[ -n "$AUDIO_FOLDER" ]]; then
  if [[ -z "$AUDIO_OUTPUT" ]]; then
    base="${BRANDED_OUTPUT%.*}"
    AUDIO_OUTPUT="${base}-audio.mp4"
  fi
  if [[ "$AUDIO_OUTPUT" == */* ]]; then
    mkdir -p "$(dirname "$AUDIO_OUTPUT")"
  fi
  python3 add_random_audio.py \
    --input-video "$BRANDED_OUTPUT" \
    --output "$AUDIO_OUTPUT" \
    --audio-folder "$AUDIO_FOLDER" \
    --duration "$AUDIO_DURATION" \
    --mode "$AUDIO_MODE" \
    --audio-volume "$AUDIO_VOLUME" \
    --original-volume "$ORIGINAL_VOLUME"
  SOURCE_FOR_META="$AUDIO_OUTPUT"
fi

ffmpeg -y -i "$SOURCE_FOR_META" -c copy \
  -metadata title="$META_TITLE" \
  -metadata artist="$META_ARTIST" \
  -metadata comment="$META_COMMENT" \
  "$FINAL_OUTPUT"

echo "Branded video: $BRANDED_OUTPUT"
echo "Final video: $FINAL_OUTPUT"
