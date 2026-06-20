#!/usr/bin/env python3
"""KORMAN — logo circular con paletas cálidas A y C."""
from PIL import Image, ImageDraw, ImageFont
import math, os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/logo_calido/"
os.makedirs(OUT, exist_ok=True)

S = 1200

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

def texto_arco(img, cx, cy, R, texto, font, color, arc_center_deg, total_deg, flip=False):
    n = len(texto)
    if n == 0: return
    if flip: texto = texto[::-1]
    start = arc_center_deg - total_deg/2
    step  = total_deg/(n-1) if n > 1 else 0
    for i, ch in enumerate(texto):
        deg = start + i*step; a = math.radians(deg)
        x = cx + R*math.cos(a); y = cy + R*math.sin(a)
        ci = Image.new("RGBA", (70,70), (0,0,0,0)); cd = ImageDraw.Draw(ci)
        bb = cd.textbbox((0,0), ch, font=font); cw, chh = bb[2]-bb[0], bb[3]-bb[1]
        cd.text((35-cw//2-bb[0], 35-chh//2-bb[1]), ch, font=font, fill=color)
        rot = (-deg-90) if not flip else (-deg+90)
        ci = ci.rotate(rot, expand=False, resample=Image.BICUBIC)
        img.paste(ci, (int(x)-35, int(y)-35), ci)

def logo_calido(filename, bg, circulo, texto_superior, k_color, acento):
    """
    bg            = color de fondo
    circulo       = color del anillo y texto superior
    texto_superior= color de "KORMAN ETIQUETAS BORDADAS"
    k_color       = color de la K central
    acento        = color de "EST. 1980"
    """
    img = Image.new("RGB", (S, S), bg)
    d   = ImageDraw.Draw(img)
    cx = cy = S // 2

    d.ellipse([cx-440, cy-440, cx+440, cy+440], outline=circulo, width=3)

    texto_arco(img, cx, cy, 386, "KORMAN ETIQUETAS BORDADAS",
               fnt("CrimsonPro-Bold.ttf", 54), texto_superior, -90, 205)
    texto_arco(img, cx, cy, 386, "EST. 1980",
               fnt("CrimsonPro-Bold.ttf", 46), acento, 90, 48, flip=True)

    d = ImageDraw.Draw(img)
    f_k = fnt("Gloock-Regular.ttf", 400)
    while tw(d, "K", f_k) > 340:
        f_k = fnt("Gloock-Regular.ttf", f_k.size - 6)
    kb = d.textbbox((0, 0), "K", font=f_k)
    kx = cx - (kb[0]+kb[2])//2
    ky = cy - (kb[1]+kb[3])//2 - 8
    d.text((kx, ky), "K", font=f_k, fill=k_color)

    img.save(OUT + filename, "PNG", dpi=(300,300))
    print("✓", filename)

# ── PALETA A — Beige arena + Marrón camel ─────────────────────────
BG_A      = (242, 235, 220)   # beige arena — fondo
DARK_A    = (72,  48,  24)    # marrón oscuro — círculo, texto, K
ACENTO_A  = (185, 140, 75)    # camel dorado — EST. 1980

logo_calido("logo-A-beige-marron.png",
            bg=BG_A, circulo=DARK_A, texto_superior=DARK_A,
            k_color=DARK_A, acento=ACENTO_A)

# ── PALETA C — Lino natural + Café oscuro ─────────────────────────
BG_C      = (235, 224, 206)   # lino natural — fondo
DARK_C    = (60,  38,  18)    # café oscuro — círculo, texto, K
ACENTO_C  = (172, 120, 60)    # siena cálido — EST. 1980

logo_calido("logo-C-lino-cafe.png",
            bg=BG_C, circulo=DARK_C, texto_superior=DARK_C,
            k_color=DARK_C, acento=ACENTO_C)

# ── VARIANTE: lino con K en camel (más sutil) ─────────────────────
logo_calido("logo-C2-lino-k-camel.png",
            bg=BG_C, circulo=DARK_C, texto_superior=DARK_C,
            k_color=ACENTO_C, acento=DARK_C)

# ── PANEL COMPARATIVO 3 logos ─────────────────────────────────────
cell = 600
panel = Image.new("RGB", (cell*3 + 20, cell), (200, 185, 160))
for i, fname in enumerate(["logo-A-beige-marron.png", "logo-C-lino-cafe.png", "logo-C2-lino-k-camel.png"]):
    im = Image.open(OUT + fname).convert("RGB").resize((cell, cell), Image.LANCZOS)
    panel.paste(im, (i*(cell+10), 0))

d_p = ImageDraw.Draw(panel)
f_l = fnt("Jura-Light.ttf", 22)
labels = ["A · BEIGE + MARRÓN", "C · LINO + CAFÉ", "C2 · LINO + K CAMEL"]
for i, lbl in enumerate(labels):
    d_p.text((i*(cell+10)+16, cell-38), lbl, font=f_l, fill=(80, 55, 30))

panel.save(OUT + "panel-logos-calidos.png", "PNG")
print("\n✓ panel-logos-calidos.png")
