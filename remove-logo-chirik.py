#!/usr/bin/env python3
"""Remove the stray chirik under the dalet of the logo animation.

Canva's animation engine vocalises the wordmark and drops a chirik under the
dalet. Finding it by colour does not survive the clip: it is faint while the
text flies in, and a gold light sweep crosses the letters around the five
second mark that both lights the dot up and scatters sparkles beside it.

Instead it is placed geometrically. Measured across the frames where the dot is
unambiguous, it sits at a fixed offset from the top-left of the wordmark's
bounding box, scaled by the box's *width* — width rather than height, because
the final kaf's descender drops out of the purple mask whenever the sweep lights
it, which collapses the box's bottom edge and nothing else. The fit holds to
about three pixels over the whole clip.

Each spot is then covered with a feathered copy of the wall beside it, which
carries whatever light the sweep is casting at that moment rather than inventing
a colour, and purple pixels are masked out so the letters are never touched.
The dagesh inside the bet and the holam over the vav belong to the logo and sit
in the other word, well outside anything this reaches.

    python remove-logo-chirik.py in.mp4 out.mp4
"""
import subprocess
import sys

import imageio_ffmpeg
import numpy as np

SRC, DST = sys.argv[1], sys.argv[2]
W, H = 1280, 720
KY, KX = 0.204, 0.389      # dot offset from the box's top-left, in box widths
exe = imageio_ffmpeg.get_ffmpeg_exe()


def cover(a, cy, cx, r, purple):
    """Paste a feathered patch of the wall from beside the dot over it."""
    R = r + 7
    if not (R <= cy < H - R):
        return False
    best = None
    for dx in (60, -60, 82, -82, 104, -104, 126, -126):
        sx = cx + dx
        if not (R <= sx < W - R):
            continue
        if purple[cy - R:cy + R + 1, sx - R:sx + R + 1].any():
            continue
        src = a[cy - R:cy + R + 1, sx - R:sx + R + 1].astype(float)
        if best is None or src.std() < best[0]:      # plain wall beats sparkle
            best = (src.std(), src)
    if best is None:
        return False

    yy, xx = np.mgrid[-R:R + 1, -R:R + 1]
    alpha = np.clip((r + 3 - np.hypot(yy, xx)) / 6.0, 0, 1)
    alpha[purple[cy - R:cy + R + 1, cx - R:cx + R + 1]] = 0
    alpha = alpha[..., None]
    dst = a[cy - R:cy + R + 1, cx - R:cx + R + 1].astype(float)
    a[cy - R:cy + R + 1, cx - R:cx + R + 1] = np.clip(
        dst * (1 - alpha) + best[1] * alpha, 0, 255).astype(np.uint8)
    return True


rd = subprocess.Popen([exe, '-v', 'error', '-i', SRC, '-f', 'rawvideo',
                       '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen([exe, '-y', '-v', 'error',
                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', '24', '-i', '-', '-i', SRC,
                       '-map', '0:v', '-map', '1:a?',
                       '-c:v', 'libx264', '-profile:v', 'high', '-crf', '18',
                       '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest',
                       '-movflags', '+faststart', DST], stdin=subprocess.PIPE)

n = done = 0
while True:
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    R, G, B = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    purple = (R < 140) & (B > R) & (B < 175) & (G < 100)
    py, px = np.nonzero(purple)
    if len(py) > 600:
        y0, x0, x1 = py.min(), px.min(), px.max()
        w = x1 - x0
        if cover(a, int(y0 + KY * w), int(x0 + KX * w),
                 max(14, int(0.052 * w)), purple):
            done += 1
    wr.stdin.write(a.tobytes())
    n += 1

wr.stdin.close(); wr.wait()
print(f'frames {n}, covered {done}')
