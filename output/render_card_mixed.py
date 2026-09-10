from PIL import Image, ImageDraw, ImageFont, ImageFilter

RIGHT = 1210
RED = (142, 23, 16)          # pomegranate skin
CYPRESS = (51, 71, 43)       # cypress crown, lifted for contrast
VERSE = [
    "הַשְׁקִיפָה מִמְּעוֹן קָדְשְׁךָ מִן־הַשָּׁמַיִם",
    "וּבָרֵךְ אֶת־עַמְּךָ אֶת־יִשְׂרָאֵל",
    "וְאֵת הָאֲדָמָה אֲשֶׁר נָתַתָּה לָנוּ...",
]

def build(out, green=CYPRESS, verse_top=92, gap_block=40, gap_sign=18,
          greet_size=70, name_size=50,
          greet="שנה טובה ומתוקה", name="משפחת אלגרבלי"):
    im = Image.open("base.png").convert("RGB")
    W, H = im.size
    fv = ImageFont.truetype("VarelaRound.ttf", 60)
    fg = ImageFont.truetype("GveretLevin.ttf", greet_size)
    fn = ImageFont.truetype("GveretLevin.ttf", name_size)
    box = lambda t, f: f.getbbox(t, direction="rtl", language="he")

    # verse: fixed leading, as approved
    items = [(t, fv, verse_top + i * 97, RED) for i, t in enumerate(VERSE)]

    # greeting + signature: stacked on measured ink, not on the em box
    ink_bottom = items[-1][2] + box(VERSE[-1], fv)[3]
    gy = ink_bottom + gap_block - box(greet, fg)[1]
    items.append((greet, fg, gy, green))
    ny = gy + box(greet, fg)[3] + gap_sign - box(name, fn)[1]
    items.append((name, fn, ny, green))

    place = lambda t, f: RIGHT - box(t, f)[2]

    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for t, f, y, _ in items:
        gd.text((place(t, f), y), t, font=f, fill=255, direction="rtl",
                language="he", stroke_width=7, stroke_fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 1.7)))
    im.paste(Image.new("RGB", (W, H), (255, 253, 247)), (0, 0), glow)

    for shade, colour in (("verse", (90, 40, 25)), ("sign", (30, 45, 25))):
        sh = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(sh)
        for t, f, y, c in items:
            if (c == RED) != (shade == "verse"):
                continue
            sd.text((place(t, f) + 2, y + 3), t, font=f, fill=90,
                    direction="rtl", language="he")
        im.paste(Image.new("RGB", (W, H), colour), (0, 0),
                 sh.filter(ImageFilter.GaussianBlur(4)))

    d = ImageDraw.Draw(im)
    for t, f, y, c in items:
        d.text((place(t, f), y), t, font=f, fill=c, direction="rtl", language="he")
    im.save(out)
    print(out, "greet_y", round(gy), "name_y", round(ny),
          "name ink bottom", round(ny + box(name, fn)[3]))

if __name__ == "__main__":
    build("mix_a.png")
    build("mix_b.png", green=(62, 92, 50))
