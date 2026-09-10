from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "VarelaRound.ttf"
RED = (142, 23, 16)
RIGHT = 1210
VERSE = [
    "הַשְׁקִיפָה מִמְּעוֹן קָדְשְׁךָ מִן־הַשָּׁמַיִם",
    "וּבָרֵךְ אֶת־עַמְּךָ אֶת־יִשְׂרָאֵל",
    "וְאֵת הָאֲדָמָה אֲשֶׁר נָתַתָּה לָנוּ...",
]

def build(out, greet, name, verse_top=92, greet_y=400, name_y=484,
          greet_size=62, name_size=38):
    im = Image.open("base.png").convert("RGB")
    W, H = im.size
    fv = ImageFont.truetype(FONT, 60)
    fg = ImageFont.truetype(FONT, greet_size)
    fn = ImageFont.truetype(FONT, name_size)
    step = int(60 * 1.62)

    items = [(t, fv, verse_top + i * step) for i, t in enumerate(VERSE)]
    items += [(greet, fg, greet_y), (name, fn, name_y)]
    place = lambda t, f: RIGHT - f.getbbox(t, direction="rtl", language="he")[2]

    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for t, f, y in items:
        gd.text((place(t, f), y), t, font=f, fill=255, direction="rtl",
                language="he", stroke_width=6, stroke_fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(13)).point(lambda v: min(255, int(v * 1.6)))
    im.paste(Image.new("RGB", (W, H), (255, 252, 245)), (0, 0), glow)

    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for t, f, y in items:
        sd.text((place(t, f) + 2, y + 3), t, font=f, fill=95,
                direction="rtl", language="he")
    im.paste(Image.new("RGB", (W, H), (90, 40, 25)), (0, 0),
             sh.filter(ImageFilter.GaussianBlur(4)))

    d = ImageDraw.Draw(im)
    for t, f, y in items:
        d.text((place(t, f), y), t, font=f, fill=RED, direction="rtl", language="he")
    im.save(out)
    print(out, "ok")

build("card_plain.png", "שנה טובה ומתוקה", "משפחת אלגרבלי")
build("card_nikud.png", "שָׁנָה טוֹבָה וּמְתוּקָה", "משפחת אלגרבלי")
