import subprocess
import os
import glob

# Directories
input_dir = "input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Get all input AVI files
# Match all files, then filter manually for case-insensitive ".avi"
all_files = glob.glob(os.path.join(input_dir, "*"))
avi_files = [f for f in all_files if f.lower().endswith(".avi")]

# Get base names of already converted files (no extension)
converted = {
    os.path.splitext(os.path.basename(f))[0]
    for f in glob.glob(os.path.join(output_dir, "*.mp4"))
}

for avi_path in avi_files:
    base_name = os.path.splitext(os.path.basename(avi_path))[0]

    # Skip if already converted
    if base_name in converted:
        print(f"✅ Skipping {avi_path} (already converted)")
        continue

    output_path = os.path.join(output_dir, f"{base_name}.mp4")
    print(f"🔄 Converting {avi_path} → {output_path}")

    # Run FFmpeg
    subprocess.run([
        "ffmpeg",
        "-i", avi_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ])

