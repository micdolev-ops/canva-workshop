#!/usr/bin/env python3
"""Square MP4 of the logo animation, for converting to a GIF on an outside site.

Same framing as build-profile-gif.py — the centre 720x720 crop, which holds the
whole logo — but left as video at full resolution so a converter has something
clean to work from. The finished logo is held at the start as well as the end:
Gmail freezes a profile GIF on its first frame in the inbox list, so that frame
has to be the completed mark, not a half-drawn ring.

    pip install imageio-ffmpeg
    python build-profile-square-mp4.py logo.mp4 out.mp4
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
FPS = 25
exe = imageio_ffmpeg.get_ffmpeg_exe()

work = tempfile.mkdtemp()
try:
    subprocess.run([exe, '-y', '-v', 'error', '-ss', str(START), '-t', str(LENGTH),
                    '-i', SRC, '-vf',
                    f'crop=720:720:280:0,hqdn3d=6:6:8:8,fps={FPS}',
                    f'{work}/f%03d.png'], check=True)
    frames = sorted(glob.glob(f'{work}/f*.png'))
    if not frames:
        sys.exit('no frames came out of the source')
    done = frames[-1]

    listing = [f"file '{done}'\nduration 0.9"]
    listing += [f"file '{f}'\nduration {1 / FPS:.3f}" for f in frames]
    listing += [f"file '{done}'\nduration 1.4", f"file '{done}'"]
    with open(f'{work}/list.txt', 'w') as fh:
        fh.write("\n".join(listing) + "\n")

    subprocess.run([exe, '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', f'{work}/list.txt', '-vf', f'fps={FPS},format=yuv420p',
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
                    '-movflags', '+faststart', OUT], check=True)
finally:
    shutil.rmtree(work, ignore_errors=True)

print(f'{OUT}  {os.path.getsize(OUT) // 1024} KB')
