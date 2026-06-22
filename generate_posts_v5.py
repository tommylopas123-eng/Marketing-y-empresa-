#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Posts v5 (estilo nuevo, conjunto con la presentación)
Fondo de tejido diagonal sutil. Detalle dorado. Tipografía BigShoulders.
Etiqueta como protagonista. Sin líneas separadoras, sin numeración.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_v5/"
FOTOS = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

BG      = (252, 250, 246)   # blanco roto — color de marca
BLACK   = (8,   8,   8  )
GRAY_MD = (110, 108, 104)
GRAY_LT = (200, 198, 194)
GOLD    = (176, 138, 58 )
WEAVE   = (244, 241, 234)   # líneas de tejido


def fnt(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()


def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def weave_bg(draw):
    """Fondo de tejido: finas líneas diagonales cruzadas."""
    gap = 26
    for off in range(-H, W, gap):
        draw.line([(off, 0), (off + H, H)], fill=WEAVE, width=1)
        draw.line([(off + H, 0), (off, H)], fill=WEAVE, width=1)


def paste_label(img, png_name, cx, cy, max_w, max_h):
    """Composita el PNG transparente centrado, limitado a max_w × max_h."""
    try:
        label = Image.open(FOTOS + png_name).convert("RGBA")
    except Exception as e:
        print(f"  [warn] {e}")
        return
    lw, lh = label.size
    scale = min(max_w / lw, max_h / lh)
    nw, nh = int(lw * scale), int(lh * scale)
    label = label.resize((nw, nh), Image.LANCZOS)
    x = cx - nw // 2
    y = cy - nh // 2
    img.paste(label, (x, y), label)


def make_post(filename, tipo, titulo, descripcion, png_label):
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Fondo de tejido
    weave_bg(draw)

    # Borde perimetral
    m = 18
    draw.rectangle([m, m, W - m, H - m], outline=GRAY_LT, width=1)

    # TIPO — texto pequeño arriba
    f_tipo = fnt("Jura-Light.ttf", 15)
    tipo_y = 60
    draw.text(((W - tw(draw, tipo, f_tipo)) // 2, tipo_y), tipo, font=f_tipo, fill=GRAY_MD)

    # TÍTULO — grande, BigShoulders
    f_title = fnt("BigShoulders-Bold.ttf", 124)
    while tw(draw, titulo, f_title) > W - 120:
        sz = f_title.size - 4
        if sz < 56: break
        f_title = fnt("BigShoulders-Bold.ttf", sz)
    titulo_y = tipo_y + 36
    draw.text(((W - tw(draw, titulo, f_title)) // 2, titulo_y), titulo, font=f_title, fill=BLACK)

    # Línea dorada
    line_y = titulo_y + f_title.size + 8
    ll = 240
    draw.line([(W // 2 - ll // 2, line_y), (W // 2 + ll // 2, line_y)], fill=GOLD, width=2)

    # DESCRIPCIÓN — debajo, gris
    f_desc = fnt("InstrumentSans-Regular.ttf", 24)
    desc_y = line_y + 22
    draw.text(((W - tw(draw, descripcion, f_desc)) // 2, desc_y), descripcion, font=f_desc, fill=GRAY_MD)

    # ETIQUETA — protagonista
    label_top    = desc_y + 56
    label_bottom = H - 96
    label_cx     = W // 2
    label_cy     = label_top + (label_bottom - label_top) // 2
    max_label_w  = W - 200
    max_label_h  = label_bottom - label_top
    paste_label(img, png_label, label_cx, label_cy, max_label_w, max_label_h)
    draw = ImageDraw.Draw(img)

    # CTA — información en la bio
    f_cta = fnt("BigShoulders-Bold.ttf", 34)
    cta = "INFORMACIÓN EN LA BIO"
    draw.text(((W - tw(draw, cta, f_cta)) // 2, H - 92), cta, font=f_cta, fill=BLACK)

    # Brand mark
    f_brand = fnt("BricolageGrotesque-Bold.ttf", 14)
    brand   = "KORMAN ETIQUETAS"
    draw.text(((W - tw(draw, brand, f_brand)) // 2, H - 54), brand, font=f_brand, fill=BLACK)
    draw.line([(W // 2 - 40, H - 38), (W // 2 + 40, H - 38)], fill=GOLD, width=1)

    img.save(OUT + filename, "PNG", dpi=(300, 300))
    print(f"✓  {filename}")


# ═════════════════════════════════════════════════════════════════════════════
# POSTS — solo los que tienen foto confirmada por Tommy
# ═════════════════════════════════════════════════════════════════════════════

# TAFETA — nxlevel confirmado por Tommy como tafeta
make_post(
    "01-tafeta.png",
    tipo        = "ETIQUETA BORDADA",
    titulo      = "TAFETA",
    descripcion = "Económica  ·  ideal para etiquetas internas",
    png_label   = "nxlevel-transparente.png",
)

# ALTA DEFINICIÓN — givenchy-denim (alta definición confirmada)
make_post(
    "02-alta-definicion.png",
    tipo        = "ETIQUETA BORDADA",
    titulo      = "ALTA DEFINICIÓN",
    descripcion = "Nítida  ·  colores intensos  ·  la más elegida",
    png_label   = "givenchy-denim-transparente.png",
)

print("\n✓  Posts v5 listos en posts_v5/")
