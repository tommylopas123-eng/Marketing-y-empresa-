#!/usr/bin/env python3
"""KORMAN — posts v6 con fondo lino café (paleta aprobada 20/06/2026)."""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_v6/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

# Paleta aprobada
BG    = (175, 150, 112)   # lino café — fondo oficial
DARK  = (60,  38,  18)    # marrón oscuro — texto principal
BORDO = (124, 38,  50)    # bordó — acento
CAMEL = (210, 178, 118)   # camel — línea dorada y detalles
GRAY  = (140, 115, 85)    # gris cálido — subtítulos
WEAVE = (163, 139, 102)   # trama textil

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

def post_base():
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)
    # trama textil sutil
    for off in range(-H, W+H, 26):
        d.line([(off,0),(off+H,H)], fill=WEAVE, width=1)
        d.line([(off+H,0),(off,H)], fill=WEAVE, width=1)
    # borde perimetral
    d.rectangle([18,18,W-18,H-18], outline=GRAY, width=1)
    return img, d

# ── POST 01 — 46 AÑOS CON ETIQUETAS BORDADAS ──────────────────────
img, d = post_base()

# kicker
f_k = fnt("Jura-Light.ttf", 16)
kick = "ETIQUETAS BORDADAS  ·  BUENOS AIRES"
d.text(((W - tw(d,kick,f_k))//2, 108), kick, font=f_k, fill=GRAY)

# títulos
titulos = [("46 AÑOS", DARK), ("CON ETIQUETAS", DARK), ("BORDADAS", BORDO)]
y = 210
for txt, col in titulos:
    f_t = fnt("BigShoulders-Bold.ttf", 128)
    while tw(d, txt, f_t) > W-120:
        f_t = fnt("BigShoulders-Bold.ttf", f_t.size-4)
    d.text(((W - tw(d,txt,f_t))//2, y), txt, font=f_t, fill=col)
    y += f_t.size + 8

# línea camel
ly = y + 20
d.line([(W//2-120, ly),(W//2+120, ly)], fill=CAMEL, width=2)

# subtítulo
f_s = fnt("InstrumentSans-Regular.ttf", 30)
sub = "empresa familiar argentina"
d.text(((W - tw(d,sub,f_s))//2, ly+28), sub, font=f_s, fill=GRAY)

# CTA
f_cta = fnt("BigShoulders-Bold.ttf", 44)
cta = "INFORMACIÓN EN LA BIO"
d.text(((W - tw(d,cta,f_cta))//2, ly+90), cta, font=f_cta, fill=DARK)

# brand
f_b = fnt("CrimsonPro-Bold.ttf", 22)
brand = "KORMAN ETIQUETAS BORDADAS"
d.text(((W - tw(d,brand,f_b))//2, H-58), brand, font=f_b, fill=DARK)

img.save(OUT + "01-46-anios.png", "PNG", dpi=(300,300))
print("✓ 01-46-anios.png")
