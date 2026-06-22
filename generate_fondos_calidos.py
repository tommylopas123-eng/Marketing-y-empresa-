#!/usr/bin/env python3
"""KORMAN — fondos cálidos para posts: distintos colores de fondo, texto oscuro."""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/fondos_preview/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
BLACK = (22, 18, 14)
GOLD  = (176, 138, 58)
GRAY  = (120, 108, 95)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

fondos = [
    ("1-beige-arena",    (242, 235, 220), "BEIGE ARENA"),
    ("2-lino-natural",   (232, 222, 202), "LINO NATURAL"),
    ("3-crema-calida",   (248, 240, 224), "CREMA CÁLIDA"),
    ("4-marron-claro",   (210, 188, 158), "MARRÓN CLARO"),
    ("5-terracota-suave",(228, 205, 178), "TERRACOTA SUAVE"),
    ("6-cafe-con-leche", (220, 198, 168), "CAFÉ CON LECHE"),
]

for slug, bg, label in fondos:
    img = Image.new("RGB", (W, H), bg)
    d   = ImageDraw.Draw(img)

    # trama textil sutil (más oscuro que el fondo)
    weave = tuple(max(c - 12, 0) for c in bg)
    gap = 26
    for off in range(-H, W+H, gap):
        d.line([(off,0),(off+H,H)], fill=weave, width=1)
        d.line([(off+H,0),(off,H)], fill=weave, width=1)

    # borde perimetral
    border = tuple(max(c - 30, 0) for c in bg)
    d.rectangle([18,18,W-18,H-18], outline=border, width=1)

    # kicker
    f_k = fnt("Jura-Light.ttf", 16)
    kick = "ETIQUETAS BORDADAS  ·  BUENOS AIRES"
    kw = tw(d, kick, f_k)
    d.text(((W-kw)//2, 108), kick, font=f_k, fill=GRAY)

    # títulos
    titulos = [("46 AÑOS", BLACK), ("CON ETIQUETAS", BLACK), ("BORDADAS", GOLD)]
    y = 210
    for txt, col in titulos:
        f_t = fnt("BigShoulders-Bold.ttf", 128)
        while tw(d, txt, f_t) > W-120:
            f_t = fnt("BigShoulders-Bold.ttf", f_t.size-4)
        d.text(((W - tw(d, txt, f_t))//2, y), txt, font=f_t, fill=col)
        y += f_t.size + 8

    # línea dorada
    ly = y + 20
    d.line([(W//2-120, ly),(W//2+120, ly)], fill=GOLD, width=2)

    # subtítulo
    f_s = fnt("InstrumentSans-Regular.ttf", 30)
    sub = "empresa familiar argentina"
    d.text(((W - tw(d, sub, f_s))//2, ly+28), sub, font=f_s, fill=GRAY)

    # label del color abajo a la izquierda
    f_lbl = fnt("Jura-Light.ttf", 20)
    d.text((40, H-60), label, font=f_lbl, fill=GRAY)

    # brand
    f_b = fnt("CrimsonPro-Bold.ttf", 22)
    brand = "KORMAN ETIQUETAS BORDADAS"
    d.text(((W - tw(d, brand, f_b))//2, H-58), brand, font=f_b, fill=BLACK)

    img.save(OUT + slug + ".png", "PNG", dpi=(300,300))
    print("✓", slug)

# ── PANEL 2x3 ─────────────────────────────────────────────────────
cell = 360; gap = 6
panel = Image.new("RGB", (cell*3+gap*2, cell*2+gap), (200, 188, 168))
for i, (slug, bg, label) in enumerate(fondos):
    im = Image.open(OUT + slug + ".png").convert("RGB").resize((cell, cell), Image.LANCZOS)
    r, c = divmod(i, 3)
    panel.paste(im, (c*(cell+gap), r*(cell+gap)))

panel.save("/home/user/Marketing-y-empresa-/assets/panel-fondos-calidos.png", "PNG")
print("\n✓ panel-fondos-calidos.png")
