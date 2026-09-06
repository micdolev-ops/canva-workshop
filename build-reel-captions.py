#!/usr/bin/env python3
"""Burn Hebrew captions into a vertical reel, and stitch reels together.

Instagram covers the bottom third of a reel with its own caption, username and
buttons, and the top strip with its header, so anything that has to be read
sits between them. Where exactly inside that band is per-shot: the caption has
to stay off whatever the shot is actually about, so every caption carries its
own vertical position.

The text is drawn with Pillow rather than ffmpeg's drawtext, which has no bidi
pass and renders Hebrew reversed. Pillow goes through libraqm, which runs the
bidi algorithm itself, so the strings stay in logical order in the source.

    pip install imageio-ffmpeg "pillow[raqm]"
    python build-reel-captions.py spec.json out.mp4

The spec is one clip, or several to be cut together back to back:

    {"clips": [
      {"src": "before.mp4", "trim": [0, 7.0], "captions": [
        {"lines": ["...", "..."], "start": 0.4, "end": 6.6, "y": 0.20}]},
      {"src": "after.mp4",  "captions": [...]}
    ]}

`y` is the box's centre as a fraction of frame height; it defaults to 0.5.
"""
import json
import os
import shutil
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
FADE = 0.3


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
    sys.exit(f'could not read the dimensions of {path}')


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


def plate(lines, W, H, path, centre_y):
    f, size = fit(lines, path, W - 2 * MARGIN - 2 * PAD_X)
    step = round(size * LINE_GAP)

    box_w = max(width(f, l) for l in lines) + 2 * PAD_X
    box_h = step * len(lines) + 2 * PAD_Y
    x0 = (W - box_w) // 2
    y0 = round(H * centre_y) - box_h // 2

    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], RADIUS, fill=CREAM)
    for i, line in enumerate(lines):
        d.text((W // 2, y0 + PAD_Y + i * step + step // 2), line,
               font=f, fill=PURPLE, anchor='mm',
               direction='rtl', language='he')
    return im


def caption_clip(clip, out, work, tag):
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    src = clip['src']
    W, H = probe(src)
    fp = font_path()

    cmd = [exe, '-y', '-v', 'error']
    if 'trim' in clip:
        start, end = clip['trim']
        cmd += ['-ss', str(start), '-t', str(round(end - start, 3))]
    cmd += ['-i', src]

    chain, label = [], '[0:v]'
    for n, cap in enumerate(clip.get('captions', []), start=1):
        png = f'{work}/{tag}-{n}.png'
        plate(cap['lines'], W, H, fp, cap.get('y', 0.5)).save(png)
        cmd += ['-loop', '1', '-i', png]
        chain.append(
            f"[{n}:v]format=rgba,"
            f"fade=t=in:st={cap['start']}:d={FADE}:alpha=1,"
            f"fade=t=out:st={cap['end'] - FADE}:d={FADE}:alpha=1[c{n}]")
        chain.append(f'{label}[c{n}]overlay=0:0:format=auto:shortest=0[v{n}]')
        label = f'[v{n}]'

    if chain:
        cmd += ['-filter_complex', ';'.join(chain)]
    cmd += ['-map', label if chain else '0:v', '-map', '0:a?',
            '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart', '-shortest', out]
    subprocess.run(cmd, check=True)


def join(parts, out):
    """Hard cuts between the parts — a before/after wants the flip to land."""
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [exe, '-y', '-v', 'error']
    for p in parts:
        cmd += ['-i', p]
    streams = ''.join(f'[{i}:v][{i}:a]' for i in range(len(parts)))
    cmd += ['-filter_complex', f'{streams}concat=n={len(parts)}:v=1:a=1[v][a]',
            '-map', '[v]', '-map', '[a]',
            '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)


def main():
    check_raqm()
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]

    work = tempfile.mkdtemp()
    try:
        parts = []
        for i, clip in enumerate(spec['clips']):
            part = out if len(spec['clips']) == 1 else f'{work}/part{i}.mp4'
            caption_clip(clip, part, work, f'c{i}')
            parts.append(part)
        if len(parts) > 1:
            join(parts, out)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f'{out}  {os.path.getsize(out) // 1024} KB')


if __name__ == '__main__':
    main()
