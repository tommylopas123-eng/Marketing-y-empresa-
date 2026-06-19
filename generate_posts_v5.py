#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Posts v5
Fondo blanco roto. Etiqueta como protagonista. Tipografía limpia.
Sin líneas separadoras, sin numeración, sin zonas diferenciadas.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_v5/"
FOTOS = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

# Paleta — fondo claro, texto oscuro
BG       = (252, 250, 246)   # blanco roto — color de marca
BLACK    = (8,   8,   8  )   # negro puro — texto principal
GRAY_MD  = (110, 108, 104)   # subtítulo
GRAY_LT  = (180, 178, 174)   # detalle sutil
ACCENT   = (8,   8,   8  )   # acento — negro (el logo es negro)


def fnt(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()


def tw(draw, text, font, tracking=0):
    total = 0
    for i, ch in enumerate(text):
        b = draw.textbbox((0, 0), ch, font=font)
        total += (b[2] - b[0])
        if i < len(text) - 1:
            total += tracking
    return total


def draw_t(draw, x, y, text, font, fill, tracking=0):
    cursor = x
    for ch in text:
        draw.text((cursor, y), ch, font=font, fill=fill)
        b = draw.textbbox((0, 0), ch, font=font)
        cursor += (b[2] - b[0]) + tracking
    return cursor


def cx_t(draw, text, font, tracking=0):
    return (W - tw(draw, text, font, tracking)) // 2


def paste_label(img, png_name, cx, cy, max_w, max_h):
    """Composita el PNG transparente centrado en (cx, cy), limitado a max_w × max_h."""
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
    # fondo blanco roto como base antes de pegar
    bg = Image.new("RGBA", img.size, (252, 250, 246, 255))
    bg.paste(img.convert("RGBA"), (0, 0))
    bg.paste(label, (x, y), label)
    result = bg.convert("RGB")
    img.paste(result)


def make_post(filename, tipo, titulo, descripcion, png_label):
    """
    tipo        → texto pequeño arriba (ej: "ETIQUETA BORDADA")
    titulo      → título grande (ej: "TAFETA")
    descripcion → una línea descriptiva
    png_label   → archivo PNG transparente de la etiqueta
    """
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ── BORDE PERIMETRAL SUTIL ────────────────────────────────────────────────
    # Marco fino que da sensación premium
    margin = 18
    draw.rectangle(
        [margin, margin, W - margin, H - margin],
        outline=GRAY_LT, width=1
    )

    # ── TIPO — texto pequeño arriba centrado ──────────────────────────────────
    f_tipo = fnt("Jura-Light.ttf", 13)
    tipo_y = 58
    tipo_w = tw(draw, tipo, f_tipo, 5)
    draw_t(draw, (W - tipo_w) // 2, tipo_y, tipo, f_tipo, GRAY_LT, 5)

    # ── TÍTULO — grande, negro, tracking suave ────────────────────────────────
    f_title = fnt("BricolageGrotesque-Bold.ttf", 96)
    while tw(draw, titulo, f_title, 2) > W - 120:
        sz = f_title.size - 4
        if sz < 48: break
        f_title = fnt("BricolageGrotesque-Bold.ttf", sz)

    titulo_y = tipo_y + 44
    draw_t(draw, cx_t(draw, titulo, f_title, 2), titulo_y, titulo, f_title, BLACK, 2)

    # ── DESCRIPCIÓN — debajo del título, gris ────────────────────────────────
    f_desc = fnt("InstrumentSans-Regular.ttf", 20)
    desc_y = titulo_y + f_title.size + 16
    draw_t(draw, cx_t(draw, descripcion, f_desc, 0), desc_y, descripcion, f_desc, GRAY_MD, 0)

    # ── ETIQUETA — protagonista, ocupa la mayor parte del post ───────────────
    # Zona disponible: desde desc_y + margen hasta arriba del brand mark
    label_top    = desc_y + 52
    label_bottom = H - 100
    label_cx     = W // 2
    label_cy     = label_top + (label_bottom - label_top) // 2
    max_label_w  = W - 160         # margen horizontal generoso
    max_label_h  = label_bottom - label_top

    paste_label(img, png_label, label_cx, label_cy, max_label_w, max_label_h)
    draw = ImageDraw.Draw(img)

    # ── BRAND MARK — abajo centrado ───────────────────────────────────────────
    f_brand = fnt("BricolageGrotesque-Bold.ttf", 13)
    brand   = "KORMAN ETIQUETAS"
    bw      = tw(draw, brand, f_brand, 3)
    draw_t(draw, (W - bw) // 2, H - 54, brand, f_brand, BLACK, 3)

    # ── LÍNEA DECORATIVA FINA bajo el brand — detalle elegante ───────────────
    line_y = H - 38
    line_len = 80
    draw.line([(W//2 - line_len//2, line_y), (W//2 + line_len//2, line_y)], fill=GRAY_LT, width=1)

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

print(f"\n✓  Posts v5 listos en posts_v5/")
