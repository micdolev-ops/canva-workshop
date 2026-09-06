#!/usr/bin/env python3
"""Turn the logo animation into a profile picture for Google, WhatsApp or LinkedIn.

Profile photos are cropped to a circle from a square, so the landscape video is
cropped to its centre 720x720 — which still holds the whole logo, wordmark
included — before being scaled down. The wall's paper grain is invisible at
avatar size but is pure noise to GIF compression, so a light denoise pass takes
the file from about 1.8MB to under 800KB with nothing lost on screen. The last
frame is held so the loop rests on the finished logo rather than mid-draw.

    pip install imageio-ffmpeg pillow
    python build-profile-gif.py logo.mp4 out.gif
"""
import os
import subprocess
import sys

import imageio_ffmpeg

SRC, OUT = sys.argv[1], sys.argv[2]
START, LENGTH = 1.4, 5.6      # the drawing-on; before this the frame is bare
SIZE, FPS, COLOURS = 256, 8, 64
exe = imageio_ffmpeg.get_ffmpeg_exe()

chain = (f"crop=720:720:280:0,"
         f"hqdn3d=10:10:14:14,"                    # kill the paper grain
         f"fps={FPS},scale={SIZE}:{SIZE}:flags=lanczos,"
         f"tpad=stop_mode=clone:stop_duration=1.5")  # rest on the finished logo

palette = os.path.join(os.path.dirname(OUT) or '.', '.palette.png')
subprocess.run([exe, '-y', '-v', 'error', '-ss', str(START), '-t', str(LENGTH),
                '-i', SRC, '-vf',
                f"{chain},palettegen=max_colors={COLOURS}:stats_mode=diff",
                palette], check=True)
subprocess.run([exe, '-y', '-v', 'error', '-ss', str(START), '-t', str(LENGTH),
                '-i', SRC, '-i', palette, '-lavfi',
                f"{chain}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5",
                '-loop', '0', OUT], check=True)
os.remove(palette)
print(f'{OUT}  {os.path.getsize(OUT) // 1024} KB')
