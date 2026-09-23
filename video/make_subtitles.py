from PIL import Image, ImageDraw, ImageFont
W,H=720,1280
font=ImageFont.truetype("Assistant-Bold.ttf",60,layout_engine=ImageFont.Layout.RAQM)
caps=["ארבעת המינים|לא דומים אחד לשני","לאתרוג יש טעם וריח","להדס ריח בלי טעם","ולערבה אין כלום","ובלעדיה הכל מתפרק"]
MAXW=560
def wrap(t):
    words=t.split(); lines=[]; cur=""
    for w in words:
        c=(cur+" "+w).strip()
        if font.getlength(c,direction="rtl")<=MAXW: cur=c
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
for i,t in enumerate(caps):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    lines=t.split("|") if "|" in t else wrap(t); lh=74
    tw=max(font.getlength(l,direction="rtl") for l in lines)
    px,py=40,26; bw=tw+2*px; bh=lh*len(lines)+2*py
    x0=(W-bw)/2; y0=(H-bh)/2
    d.rounded_rectangle([x0,y0,x0+bw,y0+bh],radius=22,fill=(245,235,215,165))
    for j,l in enumerate(lines):
        d.text((W/2,y0+py+lh*j+lh/2),l,font=font,fill=(40,30,20,255),anchor="mm",direction="rtl",language="he")
    im.save(f"cap{i}.png")
