#!/usr/bin/env python3
"""KORMAN — versión EDITORIAL: mucho aire, casi sin texto, etiqueta protagonista.
Pensada para comparar con el estilo v5 cargado."""
from PIL import Image, ImageDraw, ImageFont
import os
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_editorial/"
FOTOS = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
BG    = (250, 248, 244)   # papel, casi liso
BLACK = (18,  15,  15 )
GRAY  = (140, 138, 134)
BORDO = (124, 38,  50 )

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

def paste_label(img, png, cx, cy, max_w, max_h):
    label = Image.open(FOTOS + png).convert("RGBA")
    lw, lh = label.size
    scale = min(max_w/lw, max_h/lh)
    nw, nh = int(lw*scale), int(lh*scale)
    label = label.resize((nw, nh), Image.LANCZOS)
    img.paste(label, (cx-nw//2, cy-nh//2), label)

def make(filename, titulo, png_label, kicker):
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)

    # Kicker minúsculo, tracking amplio, arriba a la izquierda
    f_k = fnt("Jura-Light.ttf", 17)
    kick = "  ".join(kicker.upper())
    d.text((90, 92), kick, font=f_k, fill=GRAY)

    # Etiqueta protagonista — grande, centrada, con mucho aire
    paste_label(img, png_label, W//2, int(H*0.50), int(W*0.62), int(H*0.46))

    # Título fino abajo, una sola palabra, serif elegante
    f_t = fnt("Italiana-Regular.ttf", 96)
    d.text(((W - tw(d, titulo, f_t))//2, int(H*0.78)), titulo, font=f_t, fill=BLACK)

    # Sello chiquito abajo (wordmark discreto, no CTA)
    f_b = fnt("CrimsonPro-Bold.ttf", 20)
    brand = "KORMAN ETIQUETAS BORDADAS"
    bt = "   ".join([brand])
    d.text(((W - tw(d, brand, f_b))//2, H-78), brand, font=f_b, fill=BLACK)
    # puntito bordó centrado
    d.ellipse([W//2-3, H-44, W//2+3, H-38], fill=BORDO)

    img.save(OUT + filename, "PNG", dpi=(300,300))
    print("✓", filename)

# Dos ejemplos editoriales con etiquetas que ya tenemos
make("ed-01-tafeta.png",      "TAFETA",          "nxlevel-transparente.png",        "etiqueta bordada")
make("ed-02-alta-def.png",    "ALTA DEFINICIÓN", "givenchy-denim-transparente.png", "etiqueta bordada")
print("\n✓ editoriales listos")
