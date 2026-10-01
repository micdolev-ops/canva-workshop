#!/usr/bin/env python3
"""Turn carousel slides into a vertical reel, timed by how much there is to read.

Each slide gets a duration derived from its word count, so a slide with two
lines does not sit on screen as long as one with a paragraph. Square slides are
laid over a blurred blow-up of themselves, which fills the 9:16 frame without
the empty bands that flat padding leaves.

    pip install imageio-ffmpeg pillow
    python build-reel-from-slides.py out.mp4 slide1.png:14 slide2.png:30 ...

The number after each colon is the word count on that slide.
"""
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageEnhance, ImageFilter

W, H = 1080, 1920          # Instagram reel frame
LIFT = 90                  # nudge up: Instagram's UI covers the bottom
FPS = 30


def duration(words):
    """Reading time in seconds. Roughly 3.2 Hebrew words a second, plus a beat
    to take the slide in before the text starts being read."""
    return max(3.5, round(1.0 + words / 3.2, 2))


def backdrop(im):
    scale = max(W / im.width, H / im.height)
    b = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (b.width - W) // 2, (b.height - H) // 2
    b = b.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(48))
    return ImageEnhance.Brightness(b).enhance(1.04)


def main(out_path, specs, work_dir="."):
    entries, total = [], 0.0
    for i, spec in enumerate(specs, 1):
        path, _, words = spec.rpartition(":")
        im = Image.open(path).convert("RGB")
        art = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        canvas = backdrop(im)
        canvas.paste(art, (0, max(0, (H - art.height) // 2 - LIFT)))
        frame = f"{work_dir}/frame{i:02d}.png"
        canvas.save(frame)

        d = duration(int(words))
        total += d
        entries.append(f"file '{frame}'\nduration {d}")
        print(f"slide {i}: {words:>3} words -> {d:>5.2f}s")

    entries.append(entries[-1].split("\n")[0])   # concat needs the last file twice
    listing = f"{work_dir}/slides.txt"
    with open(listing, "w") as fh:
        fh.write("\n".join(entries) + "\n")
    print(f"\ntotal: {total:.1f}s  ({int(total // 60)}:{int(total % 60):02d})")

    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), "-y",
        "-f", "concat", "-safe", "0", "-i", listing,
        "-vf", f"fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.0", "-crf", "20",
        "-movflags", "+faststart",
        "-an",                                   # audio is added in Instagram
        out_path,
    ], check=True)
    print("wrote", out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
