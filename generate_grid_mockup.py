#!/usr/bin/env python3
"""KORMAN — mockup de grilla por filas: fila 1 NEGRA, fila 2 productos BLANCOS.
Genera los posts negros de la fila 1 y compone la grilla."""
from PIL import Image, ImageDraw, ImageFont
import os
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
POSTS = "/home/user/Marketing-y-empresa-/posts_v5/"
DARK  = "/home/user/Marketing-y-empresa-/posts_oscuros/"
OUT   = "/home/user/Marketing-y-empresa-/assets/"
os.makedirs(DARK, exist_ok=True)

W = H = 1080
BLACK  = (12, 11, 11)
CREAM  = (250, 248, 244)
GOLD   = (176, 138, 58)
GRAYW  = (170, 168, 164)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

def weave_bg(d, color):
    gap = 26
    for off in range(-H, W, gap):
        d.line([(off,0),(off+H,H)], fill=color, width=1)
        d.line([(off+H,0),(off,H)], fill=color, width=1)

def post_negro(filename, bg, lineas, gold_idx, sub, size=150):
    """lineas: lista de strings. gold_idx: índice de la línea dorada (o -1)."""
    img = Image.new("RGB", (W, H), bg)
    d   = ImageDraw.Draw(img)
    weave_bg(d, tuple(min(c+9,255) for c in bg))
    d.rectangle([18,18,W-18,H-18], outline=tuple(min(c+38,255) for c in bg), width=1)

    fonts = []
    for ln in lineas:
        f = fnt("BigShoulders-Bold.ttf", size)
        while tw(d, ln, f) > W-140: f = fnt("BigShoulders-Bold.ttf", f.size-4)
        fonts.append(f)
    total_h = sum(f.size for f in fonts) + 6*(len(lineas)-1)
    y = (H - total_h)//2 - 40
    for i, ln in enumerate(lineas):
        col = GOLD if i == gold_idx else CREAM
        d.text(((W-tw(d,ln,fonts[i]))//2, y), ln, font=fonts[i], fill=col)
        y += fonts[i].size + 6
    # línea dorada
    ly = y + 18
    d.line([(W//2-120, ly),(W//2+120, ly)], fill=GOLD, width=2)
    # subtítulo
    f_s = fnt("InstrumentSans-Regular.ttf", 30)
    d.text(((W-tw(d,sub,f_s))//2, ly+28), sub, font=f_s, fill=GRAYW)
    # marca abajo
    f_b = fnt("CrimsonPro-Bold.ttf", 22)
    brand = "KORMAN ETIQUETAS BORDADAS"
    d.text(((W-tw(d,brand,f_b))//2, H-70), brand, font=f_b, fill=CREAM)
    img.save(DARK + filename, "PNG", dpi=(300,300))
    print("✓", filename)

# Fila 1 — los 3 negros
post_negro("n1-46-anios.png", BLACK,
           ["46 AÑOS", "CON ETIQUETAS", "BORDADAS"], 2,
           "empresa familiar argentina", size=132)
post_negro("n2-cada-punto.png", BLACK,
           ["CADA PUNTO,", "TU MARCA"], 1,
           "bordado real, no estampa", size=150)
post_negro("n3-argentina.png", BLACK,
           ["HECHO EN", "ARGENTINA"], 1,
           "maquinaria suiza · alta definición", size=150)

# ── COMPONER GRILLA 3x3 ─────────────────────────────────────────────
cell = 360; gap = 6
grid_imgs = [
    # Fila 1 — NEGROS
    DARK+"n1-46-anios.png", DARK+"n2-cada-punto.png", DARK+"n3-argentina.png",
    # Fila 2 — productos BLANCOS
    POSTS+"01-tafeta.png", POSTS+"02-alta-definicion.png", POSTS+"01-tafeta.png",
    # Fila 3 — negros otra vez (continúa el patrón)
    DARK+"n1-46-anios.png", DARK+"n2-cada-punto.png", DARK+"n3-argentina.png",
]
GW = cell*3 + gap*2
canvas = Image.new("RGB", (GW, GW), (255,255,255))
for i, p in enumerate(grid_imgs):
    im = Image.open(p).convert("RGB").resize((cell, cell), Image.LANCZOS)
    r, c = divmod(i, 3)
    canvas.paste(im, (c*(cell+gap), r*(cell+gap)))
canvas.save(OUT + "mockup-grilla.png", "PNG")
print("\n✓ mockup-grilla.png")
