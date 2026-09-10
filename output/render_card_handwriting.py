from PIL import Image, ImageDraw, ImageFont, ImageFilter

RIGHT = 1210
VERSE = [
    "הַשְׁקִיפָה מִמְּעוֹן קָדְשְׁךָ מִן־הַשָּׁמַיִם",
    "וּבָרֵךְ אֶת־עַמְּךָ אֶת־יִשְׂרָאֵל",
    "וְאֵת הָאֲדָמָה אֲשֶׁר נָתַתָּה לָנוּ...",
]

def build(out, font_file, color, vsize, greet_size, name_size,
          verse_top, greet_y, name_y, leading=1.62, glow_boost=1.7,
          greet="שנה טובה ומתוקה", name="משפחת אלגרבלי", shadow=(30, 45, 25)):
    im = Image.open("base.png").convert("RGB")
    W, H = im.size
    fv = ImageFont.truetype(font_file, vsize)
    fg = ImageFont.truetype(font_file, greet_size)
    fn = ImageFont.truetype(font_file, name_size)
    step = int(vsize * leading)

    items = [(t, fv, verse_top + i * step) for i, t in enumerate(VERSE)]
    items += [(greet, fg, greet_y), (name, fn, name_y)]
    place = lambda t, f: RIGHT - f.getbbox(t, direction="rtl", language="he")[2]

    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for t, f, y in items:
        gd.text((place(t, f), y), t, font=f, fill=255, direction="rtl",
                language="he", stroke_width=7, stroke_fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(14)).point(
        lambda v: min(255, int(v * glow_boost)))
    im.paste(Image.new("RGB", (W, H), (255, 253, 247)), (0, 0), glow)

    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for t, f, y in items:
        sd.text((place(t, f) + 2, y + 3), t, font=f, fill=90,
                direction="rtl", language="he")
    im.paste(Image.new("RGB", (W, H), shadow), (0, 0),
             sh.filter(ImageFilter.GaussianBlur(4)))

    d = ImageDraw.Draw(im)
    for t, f, y in items:
        d.text((place(t, f), y), t, font=f, fill=color, direction="rtl", language="he")
    im.save(out)
    for t, f, y in items:
        print("  ", round(f.getbbox(t, direction='rtl', language='he')[2]), y, t[:14])
    print(out, "saved")

if __name__ == "__main__":
    CYPRESS = (51, 71, 43)
    build("hand_test.png", "GveretLevin.ttf", CYPRESS, 60, 62, 44, 92, 400, 486)
