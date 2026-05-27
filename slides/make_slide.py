from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
import random

W, H = 1080, 1350
FONTS = {
    'bold': '/usr/share/fonts/truetype/noto/NotoSansHebrew-Bold.ttf',
    'regular': '/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf',
    'medium': '/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf',
}
BG_TOP    = (13, 27, 42)
BG_BOTTOM = (20, 5, 45)
TURQUOISE = (0, 196, 204)
PURPLE    = (139, 92, 246)
GOLD      = (201, 168, 76)
GOLD_DIM  = (150, 118, 50)
WHITE     = (255, 255, 255)
GRAY      = (190, 185, 215)


def font(name, size):
    return ImageFont.truetype(FONTS[name], size)


def gradient_bg(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def add_glows(img):
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    # Turquoise glow — top right
    for r in range(280, 0, -8):
        a = int(30 * (1 - r / 280))
        gd.ellipse([W - 320 - r, -180 - r, W + r, 180 + r], fill=(*TURQUOISE, a))
    # Purple glow — bottom left
    for r in range(220, 0, -8):
        a = int(28 * (1 - r / 220))
        gd.ellipse([-r, H - 250 - r, 280 + r, H + r], fill=(*PURPLE, a))
    return Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')


def particles(draw, seed=42):
    random.seed(seed)
    for _ in range(80):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        c = TURQUOISE if random.random() > 0.45 else GOLD
        a_factor = random.uniform(0.25, 0.75)
        color = tuple(int(ch * a_factor) for ch in c)
        draw.ellipse([x - s, y - s, x + s, y + s], fill=color)


def hb(text):
    """Return bidi-visual string for Hebrew text."""
    return get_display(text)


def text_w(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0]


def draw_center(draw, text, y, fnt, fill, max_w=None):
    tw = text_w(draw, text, fnt)
    x = (W - tw) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def draw_right(draw, text, y, fnt, fill, margin=70):
    tw = text_w(draw, text, fnt)
    x = W - tw - margin
    draw.text((x, y), text, font=fnt, fill=fill)


def gold_line(draw, y, x0=100, x1=980):
    draw.line([(x0, y), (x1, y)], fill=GOLD, width=1)


def logo(draw, y=H - 85):
    fnt = font('medium', 24)
    name = hb('מאז יצייר')
    tag  = hb('נשים יוצרות לעסק')
    draw_right(draw, name, y - 28, fnt, GOLD)
    draw_right(draw, tag,  y,      font('regular', 18), GOLD_DIM)


# ─────────────────────────────────────────────
# SLIDE 1
# ─────────────────────────────────────────────
def slide_01():
    img = Image.new('RGB', (W, H))
    gradient_bg(img)
    img = add_glows(img)
    draw = ImageDraw.Draw(img)
    particles(draw, seed=1)

    title_fnt = font('bold', 68)
    body_fnt  = font('regular', 36)

    # Gold top accent line
    gold_line(draw, 260, 100, 980)

    # Title — two lines
    t1 = hb('פתחת קנבה. מצאת משהו.')
    t2 = hb('וידעת שזה לא מה שדמיינת.')
    draw_center(draw, t1, 300, title_fnt, WHITE)
    draw_center(draw, t2, 390, title_fnt, WHITE)

    # Gold bottom accent line under title
    gold_line(draw, 490, 100, 980)

    # Turquoise decorative dot
    draw.ellipse([530, 470, 550, 490], fill=TURQUOISE)

    # Body text
    b1 = hb('רוב הכלים שיכולים לשנות את התמונה —')
    b2 = hb('מסתתרים בדיוק מתחת לפני השטח.')
    draw_center(draw, b1, 560, body_fnt, GRAY)
    draw_center(draw, b2, 610, body_fnt, GRAY)

    logo(draw)

    out = '/home/user/canva-workshop/slides/slide_01.jpg'
    img.save(out, 'JPEG', quality=95)
    print(f'Saved: {out}')


slide_01()
