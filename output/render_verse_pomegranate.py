from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "VarelaRound.ttf"
LINES = [
    "הַשְׁקִיפָה מִמְּעוֹן קָדְשְׁךָ מִן־הַשָּׁמַיִם",
    "וּבָרֵךְ אֶת־עַמְּךָ אֶת־יִשְׂרָאֵל",
    "וְאֵת הָאֲדָמָה אֲשֶׁר נָתַתָּה לָנוּ...",
]
POMEGRANATE = (142, 23, 16)

def build(out, size, top=128, right=1210):
    im = Image.open("base.png").convert("RGB")
    W, H = im.size
    font = ImageFont.truetype(FONT, size)
    step = int(size * 1.62)
    lw = lambda t: font.getbbox(t, direction="rtl", language="he")[2]
    pos = lambda i, t: (right - lw(t), top + i * step)

    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for i, t in enumerate(LINES):
        gd.text(pos(i, t), t, font=font, fill=255, direction="rtl", language="he",
                stroke_width=6, stroke_fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(13)).point(lambda v: min(255, int(v * 1.6)))
    im.paste(Image.new("RGB", (W, H), (255, 252, 245)), (0, 0), glow)

    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for i, t in enumerate(LINES):
        x, y = pos(i, t)
        sd.text((x + 2, y + 3), t, font=font, fill=95, direction="rtl", language="he")
    im.paste(Image.new("RGB", (W, H), (90, 40, 25)), (0, 0),
             sh.filter(ImageFilter.GaussianBlur(4)))

    d = ImageDraw.Draw(im)
    for i, t in enumerate(LINES):
        d.text(pos(i, t), t, font=font, fill=POMEGRANATE,
               direction="rtl", language="he")
    im.save(out)
    print(out, size, [round(lw(t)) for t in LINES], 'bottom~', top + 2*step + size)

build("verse_60.png", 60)
build("verse_68.png", 68)
