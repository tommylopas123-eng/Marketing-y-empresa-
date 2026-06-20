#!/usr/bin/env python3
"""KORMAN — Panel de paletas de colores cálidas para posts de Instagram."""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/"
os.makedirs(OUT, exist_ok=True)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()

# ── 6 PALETAS CÁLIDAS ──────────────────────────────────────────────
paletas = [
    {
        "nombre": "A · ARENA",
        "desc":   "Beige arena · marrón tostado · dorado suave",
        "colores": [(242, 236, 224), (193, 158, 103), (139, 97,  55), (62,  46,  30), (176, 138, 58)],
    },
    {
        "nombre": "B · LINO",
        "desc":   "Lino natural · camel · siena",
        "colores": [(238, 230, 215), (196, 172, 128), (172, 120, 72), (108, 68,  36), (90,  60,  30)],
    },
    {
        "nombre": "C · TERRACOTA",
        "desc":   "Crema · ocre · terracota ladrillo",
        "colores": [(248, 240, 228), (220, 185, 140), (196, 120, 72), (162, 76,  40), (90,  42,  20)],
    },
    {
        "nombre": "D · CAFÉ",
        "desc":   "Hueso cálido · cappuccino · café oscuro",
        "colores": [(246, 240, 232), (210, 186, 158), (162, 128,  90), (100, 68,  42), (52,  32,  16)],
    },
    {
        "nombre": "E · MIEL",
        "desc":   "Vainilla · ámbar · miel oscura · bordo",
        "colores": [(252, 244, 224), (230, 192, 112), (198, 148, 60), (140, 88,  28), (124, 38,  50)],
    },
    {
        "nombre": "F · PERGAMINO",
        "desc":   "Pergamino · tostado · marrón bordó · negro cálido",
        "colores": [(250, 243, 228), (210, 180, 140), (155, 110, 70), (100, 58,  38), (36,  22,  14)],
    },
]

# ── DIMENSIONES DEL PANEL ──────────────────────────────────────────
PW = 1800   # panel width
ROW_H = 280  # alto por paleta
PAD = 40
SWATCH = 200  # tamaño de cada swatch de color

panel = Image.new("RGB", (PW, ROW_H * len(paletas) + PAD*2), (30, 26, 22))
d = ImageDraw.Draw(panel)

f_nombre = fnt("BigShoulders-Bold.ttf", 34)
f_desc   = fnt("InstrumentSans-Regular.ttf", 22)
f_hex    = fnt("Jura-Light.ttf", 18)

for i, pal in enumerate(paletas):
    y0 = PAD + i * ROW_H
    # nombre paleta
    d.text((PAD, y0 + 14), pal["nombre"], font=f_nombre, fill=(250, 243, 228))
    d.text((PAD, y0 + 58), pal["desc"],   font=f_desc,   fill=(160, 150, 135))

    # swatches de colores
    sx = PAD
    sy = y0 + 100
    for col in pal["colores"]:
        d.rectangle([sx, sy, sx+SWATCH-12, sy+120], fill=col)
        # hex label
        hx = "#{:02X}{:02X}{:02X}".format(*col)
        d.text((sx + 6, sy + 126), hx, font=f_hex, fill=(160, 150, 135))
        sx += SWATCH + 8

    # separador
    if i < len(paletas) - 1:
        d.line([(PAD, y0+ROW_H-10), (PW-PAD, y0+ROW_H-10)], fill=(55, 48, 40), width=1)

panel.save(OUT + "panel-paletas-calidas.png", "PNG")
print("✓ panel-paletas-calidas.png")

# ── TAMBIÉN GENERAR UN POST DE EJEMPLO CON CADA PALETA ─────────────
W = H = 1080
POSTS_OUT = "/home/user/Marketing-y-empresa-/paletas_preview/"
os.makedirs(POSTS_OUT, exist_ok=True)

def post_muestra(filename, pal):
    bg   = pal["colores"][0]   # más claro = fondo
    mid  = pal["colores"][2]   # medio = acento/linea
    dark = pal["colores"][4]   # más oscuro = texto
    gold = pal["colores"][3]   # penúltimo = dorado/acento

    img = Image.new("RGB", (W, H), bg)
    d2  = ImageDraw.Draw(img)

    # trama textil sutil
    weave = tuple(max(c-10, 0) for c in bg)
    gap = 26
    for off in range(-H, W+H, gap):
        d2.line([(off,0),(off+H,H)], fill=weave, width=1)
        d2.line([(off+H,0),(off,H)], fill=weave, width=1)

    # borde perimetral
    d2.rectangle([18,18,W-18,H-18], outline=mid, width=1)

    # kicker
    f_k  = fnt("Jura-Light.ttf", 16)
    kick = "ETIQUETAS BORDADAS  ·  BUENOS AIRES"
    bk   = d2.textbbox((0,0), kick, f_k); kw = bk[2]-bk[0]
    d2.text(((W-kw)//2, 110), kick, font=f_k, fill=mid)

    # titulo
    f_t1 = fnt("BigShoulders-Bold.ttf", 130)
    for txt in ["46 AÑOS", "CON ETIQUETAS"]:
        bt = d2.textbbox((0,0), txt, f_t1); tw2 = bt[2]-bt[0]
        while tw2 > W-120:
            f_t1 = fnt("BigShoulders-Bold.ttf", f_t1.size-4)
            bt   = d2.textbbox((0,0), txt, f_t1); tw2 = bt[2]-bt[0]

    titles = [("46 AÑOS", dark), ("CON ETIQUETAS", dark), ("BORDADAS", gold)]
    y = 200
    for txt, col in titles:
        f_use = fnt("BigShoulders-Bold.ttf", 130)
        bt = d2.textbbox((0,0), txt, f_use); tw2 = bt[2]-bt[0]
        while tw2 > W-120:
            f_use = fnt("BigShoulders-Bold.ttf", f_use.size-4)
            bt    = d2.textbbox((0,0), txt, f_use); tw2 = bt[2]-bt[0]
        d2.text(((W-tw2)//2, y), txt, font=f_use, fill=col)
        y += f_use.size + 8

    # linea
    ly = y + 20
    d2.line([(W//2-120, ly),(W//2+120, ly)], fill=gold, width=2)

    # subtitulo
    f_s  = fnt("InstrumentSans-Regular.ttf", 30)
    sub  = "empresa familiar argentina"
    bs   = d2.textbbox((0,0), sub, f_s); sw = bs[2]-bs[0]
    d2.text(((W-sw)//2, ly+28), sub, font=f_s, fill=mid)

    # nombre paleta como label
    f_lbl = fnt("Jura-Light.ttf", 22)
    d2.text((40, H-70), pal["nombre"], font=f_lbl, fill=mid)

    # brand
    f_b  = fnt("CrimsonPro-Bold.ttf", 22)
    brand = "KORMAN ETIQUETAS BORDADAS"
    bb   = d2.textbbox((0,0), brand, f_b); bw = bb[2]-bb[0]
    d2.text(((W-bw)//2, H-65), brand, font=f_b, fill=dark)

    img.save(POSTS_OUT + filename, "PNG", dpi=(300,300))
    print("✓", filename)

for p in paletas:
    slug = p["nombre"].split("·")[1].strip().lower()
    post_muestra(f"preview-{slug}.png", p)

# ── PANEL 2x3 DE PREVIEWS ─────────────────────────────────────────
cell = 360; gap = 6
preview_panel = Image.new("RGB", (cell*3+gap*2, cell*2+gap), (30,26,22))
slugs = [p["nombre"].split("·")[1].strip().lower() for p in paletas]
for i, slug in enumerate(slugs):
    im = Image.open(POSTS_OUT + f"preview-{slug}.png").convert("RGB").resize((cell, cell), Image.LANCZOS)
    r, c = divmod(i, 3)
    preview_panel.paste(im, (c*(cell+gap), r*(cell+gap)))

preview_panel.save(OUT + "panel-previews-paletas.png", "PNG")
print("\n✓ panel-previews-paletas.png — 6 paletas listas")
