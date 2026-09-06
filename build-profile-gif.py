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
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import imageio_ffmpeg

SRC, OUT = sys.argv[1], sys.argv[2]
START, LENGTH = 1.4, 5.6      # the drawing-on; before this the frame is bare
SIZE, FPS, COLOURS = 256, 8, 64
exe = imageio_ffmpeg.get_ffmpeg_exe()

chain = (f"crop=720:720:280:0,"
         f"hqdn3d=10:10:14:14,"                    # kill the paper grain
         f"fps={FPS},scale={SIZE}:{SIZE}:flags=lanczos")

work = tempfile.mkdtemp()
try:
    subprocess.run([exe, '-y', '-v', 'error', '-ss', str(START), '-t', str(LENGTH),
                    '-i', SRC, '-vf', chain, f'{work}/f%03d.png'], check=True)
    frames = sorted(glob.glob(f'{work}/f*.png'))
    if not frames:
        sys.exit('no frames came out of the source')
    done = frames[-1]

    # Open on the finished logo, then draw it, then rest on it. Anywhere the GIF
    # is shown as a still — a file browser, a preview pane, some of Google's own
    # surfaces — that still is the logo instead of a half-drawn ring.
    listing = [f"file '{done}'\nduration 0.9"]
    listing += [f"file '{f}'\nduration {1 / FPS:.3f}" for f in frames]
    listing += [f"file '{done}'\nduration 1.4", f"file '{done}'"]
    with open(f'{work}/list.txt', 'w') as fh:
        fh.write("\n".join(listing) + "\n")

    concat = ['-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt']
    palette = f'{work}/palette.png'
    subprocess.run([exe, '-y', '-v', 'error', *concat, '-vf',
                    f"fps={FPS},palettegen=max_colors={COLOURS}:stats_mode=diff",
                    palette], check=True)
    subprocess.run([exe, '-y', '-v', 'error', *concat, '-i', palette, '-lavfi',
                    f"fps={FPS}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5",
                    '-loop', '0', OUT], check=True)
finally:
    shutil.rmtree(work, ignore_errors=True)

print(f'{OUT}  {os.path.getsize(OUT) // 1024} KB')
