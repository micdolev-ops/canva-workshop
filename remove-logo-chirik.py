"""Remove only the stray chirik under the dalet of the logo animation.

Threshold-based detection lost the dot while the wordmark was still fading in,
so instead the dot is located geometrically: its position is fixed relative to
the wordmark's bounding box, and the wordmark is easy to find because it is the
only deep-purple thing on screen. That holds through the fly-in, while the text
is still moving and scaling, and it can never reach the dagesh inside the bet or
the holam over the vav, which are part of the logo and sit elsewhere.
"""
import subprocess, sys
import numpy as np
import imageio_ffmpeg

SRC, DST = sys.argv[1], sys.argv[2]
W, H = 1280, 720
U, V = 0.388, 0.874        # the chirik, as a fraction of the wordmark box
exe = imageio_ffmpeg.get_ffmpeg_exe()


def fill_disc(a, cy, cx, r, keep):
    """Inpaint a disc from the ring around it, leaving `keep` pixels alone."""
    Y0, Y1 = max(0, cy - r - 8), min(H, cy + r + 9)
    X0, X1 = max(0, cx - r - 8), min(W, cx + r + 9)
    yy, xx = np.mgrid[Y0:Y1, X0:X1]
    d = np.hypot(yy - cy, xx - cx)
    hole = (d <= r) & ~keep[Y0:Y1, X0:X1]
    ring = (d > r) & (d <= r + 8) & ~keep[Y0:Y1, X0:X1]
    if hole.sum() == 0 or ring.sum() < 20:
        return
    ry, rx = np.nonzero(ring)
    rgb = a[Y0:Y1, X0:X1][ring].astype(float)
    hy, hx = np.nonzero(hole)
    d2 = (hy[:, None] - ry[None, :]) ** 2 + (hx[:, None] - rx[None, :]) ** 2
    w = 1.0 / (d2 + 1.0) ** 1.5
    w /= w.sum(1, keepdims=True)
    a[Y0 + hy, X0 + hx] = np.clip(w @ rgb, 0, 255).astype(np.uint8)


rd = subprocess.Popen([exe, '-v', 'error', '-i', SRC, '-f', 'rawvideo',
                       '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen([exe, '-y', '-v', 'error',
                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', '24', '-i', '-', '-i', SRC,
                       '-map', '0:v', '-map', '1:a?',
                       '-c:v', 'libx264', '-profile:v', 'high', '-crf', '18',
                       '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest',
                       '-movflags', '+faststart', DST], stdin=subprocess.PIPE)

n = hit = 0
while True:
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    R, G, B = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    purple = (R < 140) & (B > R) & (B < 175) & (G < 100)
    py, px = np.nonzero(purple)
    if len(py) > 600:
        y0, y1, x0, x1 = py.min(), py.max(), px.min(), px.max()
        cy = int(y0 + V * (y1 - y0))
        cx = int(x0 + U * (x1 - x0))
        r = max(9, int(0.17 * (y1 - y0)))
        fill_disc(a, cy, cx, r, purple)
        hit += 1
    wr.stdin.write(a.tobytes())
    n += 1

wr.stdin.close(); wr.wait()
print(f'frames {n}, cleaned {hit}')
