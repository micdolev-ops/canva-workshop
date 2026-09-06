#!/usr/bin/env python3
"""Burn Hebrew captions into the middle of a vertical reel.

Instagram covers the bottom third of a reel with the caption, the username and
the action buttons, and the top with its own header, so anything that has to be
read sits in the middle band. The captions are drawn here rather than by
ffmpeg's drawtext: drawtext has no bidi pass, so Hebrew comes out reversed.
Pillow draws them instead, through libraqm, which runs the bidi algorithm
itself — so the strings stay in logical order and only need direction='rtl'.

    pip install imageio-ffmpeg "pillow[raqm]"
    python build-reel-captions.py in.mp4 out.mp4

Brand palette is the calendar's: purple #4A3463 on the cream #FBF8F2, never
white. The font is Assistant Bold, fetched from Google Fonts if it isn't
already beside this script.
"""
import os
import subprocess
import sys
import tempfile
import urllib.request

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, features

PURPLE = (0x4A, 0x34, 0x63, 255)
CREAM = (0xFB, 0xF8, 0xF2, 205)          # ~80%, so the shot still reads through
FONT_URL = ('https://fonts.gstatic.com/s/assistant/v24/'
            '2sDPZGJYnIjSi6H75xkZZE1I0yCmYzzQtgFgEGE.ttf')

MARGIN = 56          # from the frame edge to the box
PAD_X, PAD_Y = 34, 26
MAX_SIZE = 68
LINE_GAP = 1.22
RADIUS = 26
CENTRE_Y = 0.50      # box centre, as a fraction of frame height
FADE = 0.3

# (lines, start, end) — ends at 8.9 because the last shot is a cut to her face,
# and that close is stronger without a box over it.
CAPTIONS = [
    (['שניים.', 'זה כל מה שאת צריכה.'], 0.3, 4.6),
    (['אחד לכותרות.', 'אחד לטקסט הרץ.'], 4.9, 8.9),
]


def check_raqm():
    if not features.check('raqm'):
        sys.exit('Pillow was built without libraqm; Hebrew would come out '
                 'reversed. Install with: pip install "pillow[raqm]"')


def font_path():
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assistant-Bold.ttf')
    if not os.path.exists(here):
        urllib.request.urlretrieve(FONT_URL, here)
    return here


def probe(path):
    out = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', path],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if 'Video:' in line and 'Stream' in line:
            for part in line.split(','):
                part = part.strip().split(' ')[0]
                if 'x' in part and part.replace('x', '').isdigit():
                    w, h = part.split('x')
                    return int(w), int(h)
    sys.exit('could not read the video dimensions')


def width(f, line):
    box = f.getbbox(line, direction='rtl', language='he')
    return box[2] - box[0]


def fit(lines, path, box_w):
    """Largest size at which the longest line still fits the box."""
    for size in range(MAX_SIZE, 17, -1):
        f = ImageFont.truetype(path, size)
        if max(width(f, l) for l in lines) <= box_w:
            return f, size
    return ImageFont.truetype(path, 18), 18


def plate(lines, W, H, path):
    f, size = fit(lines, path, W - 2 * MARGIN - 2 * PAD_X)
    step = round(size * LINE_GAP)

    text_w = max(width(f, l) for l in lines)
    box_w = text_w + 2 * PAD_X
    box_h = step * len(lines) + 2 * PAD_Y
    x0 = (W - box_w) // 2
    y0 = round(H * CENTRE_Y) - box_h // 2

    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], RADIUS, fill=CREAM)
    for i, line in enumerate(lines):
        d.text((W // 2, y0 + PAD_Y + i * step + step // 2), line,
               font=f, fill=PURPLE, anchor='mm',
               direction='rtl', language='he')
    return im


def main():
    check_raqm()
    src, out = sys.argv[1], sys.argv[2]
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    W, H = probe(src)
    fp = font_path()

    work = tempfile.mkdtemp()
    try:
        cmd = [exe, '-y', '-v', 'error', '-i', src]
        chain, label = [], '[0:v]'
        for n, (lines, start, end) in enumerate(CAPTIONS, start=1):
            png = f'{work}/cap{n}.png'
            plate(lines, W, H, fp).save(png)
            cmd += ['-loop', '1', '-i', png]
            chain.append(
                f'[{n}:v]format=rgba,'
                f'fade=t=in:st={start}:d={FADE}:alpha=1,'
                f'fade=t=out:st={end - FADE}:d={FADE}:alpha=1[c{n}]')
            chain.append(f'{label}[c{n}]overlay=0:0:format=auto:shortest=0[v{n}]')
            label = f'[v{n}]'

        cmd += ['-filter_complex', ';'.join(chain),
                '-map', label, '-map', '0:a?',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
                '-pix_fmt', 'yuv420p', '-c:a', 'copy',
                '-movflags', '+faststart', '-shortest', out]
        subprocess.run(cmd, check=True)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)

    print(f'{out}  {os.path.getsize(out) // 1024} KB')


if __name__ == '__main__':
    main()
