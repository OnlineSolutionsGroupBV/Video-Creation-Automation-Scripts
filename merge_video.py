
import os
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"
os.environ["FFPLAY_BINARY"] = "/usr/local/bin/ffplay"

import site
site.ENABLE_USER_SITE = True
site.addsitedir('/Users/sergejdergatsjev/Library/Python/3.9/lib/python/site-packages')

from moviepy.config import check
check()

import glob
from moviepy import VideoFileClip, concatenate_videoclips


# Get all AVI files in the current directory (sorted alphabetically)
video_files = sorted(glob.glob("output/*.mp4"))

# Load the videos
clips = [VideoFileClip(file) for file in video_files]

# Merge the video clips
final_clip = concatenate_videoclips(clips, method="compose")

# Save the final video (you can change the output format if needed)
final_clip.write_videofile("merged_output.mp4", audio_codec="aac")

