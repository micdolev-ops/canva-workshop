from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys

FONT = "VarelaRound.ttf"
LINES = [
    "הַשְׁקִיפָה מִמְּעוֹן קָדְשְׁךָ מִן־הַשָּׁמַיִם",
    "וּבָרֵךְ אֶת־עַמְּךָ אֶת־יִשְׂרָאֵל",
    "וְאֵת הָאֲדָמָה אֲשֶׁר נָתַתָּה לָנוּ...",
]

def build(align, out, size=50, top=140, right=1200, cx=830):
    im = Image.open("base.png").convert("RGB")
    W, H = im.size
    font = ImageFont.truetype(FONT, size)
    step = int(size * 1.66)
    lw = lambda t: font.getbbox(t, direction="rtl", language="he")[2]

    def pos(i, t):
        y = top + i * step
        x = right - lw(t) if align == "right" else cx - lw(t) / 2
        return x, y

    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for i, t in enumerate(LINES):
        gd.text(pos(i, t), t, font=font, fill=255, direction="rtl", language="he",
                stroke_width=5, stroke_fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(11)).point(lambda v: min(255, int(v * 1.5)))
    im.paste(Image.new("RGB", (W, H), (255, 251, 242)), (0, 0), glow)

    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for i, t in enumerate(LINES):
        x, y = pos(i, t)
        sd.text((x + 2, y + 3), t, font=font, fill=110, direction="rtl", language="he")
    im.paste(Image.new("RGB", (W, H), (120, 95, 60)), (0, 0),
             sh.filter(ImageFilter.GaussianBlur(4)))

    d = ImageDraw.Draw(im)
    for i, t in enumerate(LINES):
        d.text(pos(i, t), t, font=font, fill=(40, 30, 20),
               direction="rtl", language="he")
    im.save(out)

build("right", "verse_right.png")
build("center", "verse_center.png")
print("done")
