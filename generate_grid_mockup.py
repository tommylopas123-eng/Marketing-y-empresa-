#!/usr/bin/env python3
"""KORMAN — mockup de grilla 3x3 mezclando posts claros y oscuros (ritmo de feed).
Genera 3 posts oscuros de acento y compone la grilla de perfil."""
from PIL import Image, ImageDraw, ImageFont
import os
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
POSTS = "/home/user/Marketing-y-empresa-/posts_v5/"
DARK  = "/home/user/Marketing-y-empresa-/posts_oscuros/"
OUT   = "/home/user/Marketing-y-empresa-/assets/"
os.makedirs(DARK, exist_ok=True)

W = H = 1080
BG_W   = (252, 250, 246)
BLACK  = (12, 11, 11)
BORDO  = (108, 30, 42)
CREAM  = (250, 248, 244)
GOLD   = (176, 138, 58)
GRAYW  = (180, 178, 174)

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

def post_oscuro(filename, bg, l1, l2, sub):
    img = Image.new("RGB", (W, H), bg)
    d   = ImageDraw.Draw(img)
    # trama sutil un poco más clara que el fondo
    weave_bg(d, tuple(min(c+10,255) for c in bg))
    # borde fino
    d.rectangle([18,18,W-18,H-18], outline=tuple(min(c+40,255) for c in bg), width=1)
    # título grande centrado vertical
    f1 = fnt("BigShoulders-Bold.ttf", 150)
    while tw(d,l1,f1) > W-140: f1 = fnt("BigShoulders-Bold.ttf", f1.size-4)
    f2 = fnt("BigShoulders-Bold.ttf", 150)
    while tw(d,l2,f2) > W-140: f2 = fnt("BigShoulders-Bold.ttf", f2.size-4)
    d.text(((W-tw(d,l1,f1))//2, 360), l1, font=f1, fill=CREAM)
    d.text(((W-tw(d,l2,f2))//2, 360+f1.size+6), l2, font=f2, fill=GOLD)
    # línea dorada
    ly = 360+f1.size+6+f2.size+30
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

# 3 posts oscuros de acento
post_oscuro("o1-cada-punto.png", BLACK, "CADA PUNTO,", "TU MARCA", "bordado real, no estampa")
post_oscuro("o2-46-anios.png",   BLACK, "46 AÑOS", "DE OFICIO", "empresa familiar argentina")
post_oscuro("o3-argentina.png",  BLACK, "HECHO EN", "ARGENTINA", "maquinaria suiza · alta definición")

# ── COMPONER GRILLA 3x3 ─────────────────────────────────────────────
cell = 360
grid_imgs = [
    POSTS+"00-presentacion.png", DARK+"o1-cada-punto.png", POSTS+"01-tafeta.png",
    DARK+"o2-46-anios.png",      POSTS+"02-alta-definicion.png", DARK+"o3-argentina.png",
    POSTS+"01-tafeta.png",       DARK+"o1-cada-punto.png", POSTS+"00-presentacion.png",
]
gap = 6
GW = cell*3 + gap*2
canvas = Image.new("RGB", (GW, GW), (255,255,255))
for i, p in enumerate(grid_imgs):
    im = Image.open(p).convert("RGB").resize((cell, cell), Image.LANCZOS)
    r, c = divmod(i, 3)
    canvas.paste(im, (c*(cell+gap), r*(cell+gap)))
canvas.save(OUT + "mockup-grilla.png", "PNG")
print("\n✓ mockup-grilla.png")
