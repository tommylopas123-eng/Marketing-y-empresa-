#!/usr/bin/env python3
"""
KORMAN — Posts v3
Texto arriba, foto abajo.
Título en MAYÚSCULAS, sin puntos.
"BORDADAS" siempre, nunca "TEJIDAS".
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_v3/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
BLACK    = (8, 8, 8)
WHITE    = (252, 250, 246)
GRAY     = (150, 148, 144)
GRAY_DIM = (80, 78, 74)
PHOTO_BG = (20, 18, 16)

def font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def cw(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0]

def cx(draw, text, f):
    return (W - cw(draw, text, f)) // 2

def make_post(filename, title, subtitle=None, label=None, photo_h_pct=0.52):
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    ph   = int(H * photo_h_pct)   # alto de la foto (parte de abajo)
    th   = H - ph                  # alto del área de texto (parte de arriba)

    # ── ÁREA DE TEXTO — arriba ────────────────────────────────────────────────
    pad = 72

    # Label pequeño (ej: "ETIQUETA BORDADA · 01")
    y = pad
    if label:
        f_label = font("Jura-Light.ttf", 18)
        draw.text((cx(draw, label, f_label), y), label, font=f_label, fill=GRAY_DIM)
        y += 52

    # Título en MAYÚSCULAS, fuente grande
    f_title = font("BricolageGrotesque-Bold.ttf", 100)
    # Si el título es muy largo, reducir tamaño
    while cw(draw, title, f_title) > W - 120 and f_title.size > 60:
        f_title = font("BricolageGrotesque-Bold.ttf", f_title.size - 4)

    draw.text((cx(draw, title, f_title), y), title, font=f_title, fill=WHITE)
    y += f_title.size + 28

    # Subtítulo
    if subtitle:
        f_sub = font("InstrumentSans-Regular.ttf", 26)
        draw.text((cx(draw, subtitle, f_sub), y), subtitle, font=f_sub, fill=GRAY)
        y += 48

    # Línea fina separadora entre texto y foto
    draw.line([(60, th - 1), (W - 60, th - 1)], fill=(30, 28, 24), width=1)

    # ── ÁREA DE FOTO — abajo ──────────────────────────────────────────────────
    draw.rectangle([0, th, W, H], fill=PHOTO_BG)

    # Placeholder
    mid_x = W // 2
    mid_y = th + ph // 2
    draw.line([(mid_x - 28, mid_y), (mid_x + 28, mid_y)], fill=(38, 35, 32), width=1)
    draw.line([(mid_x, mid_y - 28), (mid_x, mid_y + 28)], fill=(38, 35, 32), width=1)
    f_ph = font("Jura-Light.ttf", 13)
    ph_text = "FOTO"
    draw.text((cx(draw, ph_text, f_ph), mid_y + 36), ph_text, font=f_ph, fill=(42, 40, 36))

    # KORMAN — abajo a la derecha, muy pequeño
    f_brand = font("BricolageGrotesque-Bold.ttf", 20)
    brand_w = cw(draw, "KORMAN", f_brand)
    draw.text((W - brand_w - 44, H - 40), "KORMAN", font=f_brand, fill=(55, 52, 48))

    img.save(OUT + filename, "PNG", dpi=(300, 300))
    print(f"✓  {filename}")


# ═════════════════════════════════════════════════════════════════════════════
# SERIE — TIPOS DE ETIQUETAS BORDADAS
# ═════════════════════════════════════════════════════════════════════════════

make_post("01-tafeta.png",
    title    = "TAFETA",
    subtitle = "Económica · para etiquetas internas",
    label    = "ETIQUETA BORDADA  ·  01",
)

make_post("02-alta-definicion.png",
    title    = "ALTA DEFINICIÓN",
    subtitle = "Nítida · colores intensos · la más elegida",
    label    = "ETIQUETA BORDADA  ·  02",
)

make_post("03-triple-densidad.png",
    title    = "TRIPLE DENSIDAD",
    subtitle = "Mayor relieve · presencia · efecto premium",
    label    = "ETIQUETA BORDADA  ·  03",
)

make_post("04-texturada.png",
    title    = "TEXTURADA",
    subtitle = "Relieve especial · para marcas que se diferencian",
    label    = "ETIQUETA BORDADA  ·  04",
)

# ═════════════════════════════════════════════════════════════════════════════
# SERIE — HISTORIA
# ═════════════════════════════════════════════════════════════════════════════

def post_historia_1980():
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    pad = 72
    y   = pad

    # Label
    f_label = font("Jura-Light.ttf", 18)
    label   = "HISTORIA  ·  01"
    draw.text((cx(draw, label, f_label), y), label, font=f_label, fill=GRAY_DIM)
    y += 52

    # Año grande
    f_year = font("BricolageGrotesque-Bold.ttf", 180)
    draw.text((cx(draw, "1980", f_year), y - 20), "1980", font=f_year, fill=WHITE)
    y += 178

    # Subtítulo
    f_sub = font("InstrumentSans-Regular.ttf", 26)
    sub   = "Así empezó KORMAN en Buenos Aires"
    draw.text((cx(draw, sub, f_sub), y), sub, font=f_sub, fill=GRAY)

    # Foto abajo (30% — taller histórico)
    ph = int(H * 0.28)
    th = H - ph
    draw.line([(60, th - 1), (W - 60, th - 1)], fill=(30, 28, 24), width=1)
    draw.rectangle([0, th, W, H], fill=PHOTO_BG)
    mid_x, mid_y = W // 2, th + ph // 2
    draw.line([(mid_x-28, mid_y), (mid_x+28, mid_y)], fill=(38,35,32), width=1)
    draw.line([(mid_x, mid_y-28), (mid_x, mid_y+28)], fill=(38,35,32), width=1)
    f_ph = font("Jura-Light.ttf", 13)
    ph_t = "FOTO TALLER"
    draw.text((cx(draw, ph_t, f_ph), mid_y + 36), ph_t, font=f_ph, fill=(42,40,36))

    f_brand = font("BricolageGrotesque-Bold.ttf", 20)
    brand_w = cw(draw, "KORMAN", f_brand)
    draw.text((W - brand_w - 44, H - 40), "KORMAN", font=f_brand, fill=(55,52,48))

    img.save(OUT + "05-historia-1980.png", "PNG", dpi=(300,300))
    print("✓  05-historia-1980.png")

def post_historia_46():
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    pad = 72
    y   = pad

    f_label = font("Jura-Light.ttf", 18)
    label   = "HISTORIA  ·  02"
    draw.text((cx(draw, label, f_label), y), label, font=f_label, fill=GRAY_DIM)
    y += 52

    f_title = font("BricolageGrotesque-Bold.ttf", 100)
    draw.text((cx(draw, "46 AÑOS", f_title), y), "46 AÑOS", font=f_title, fill=WHITE)
    y += 118

    f_sub = font("InstrumentSans-Regular.ttf", 26)
    sub   = "El mismo oficio · la misma dedicación"
    draw.text((cx(draw, sub, f_sub), y), sub, font=f_sub, fill=GRAY)

    ph = int(H * 0.52)
    th = H - ph
    draw.line([(60, th - 1), (W - 60, th - 1)], fill=(30, 28, 24), width=1)
    draw.rectangle([0, th, W, H], fill=PHOTO_BG)
    mid_x, mid_y = W // 2, th + ph // 2
    draw.line([(mid_x-28, mid_y), (mid_x+28, mid_y)], fill=(38,35,32), width=1)
    draw.line([(mid_x, mid_y-28), (mid_x, mid_y+28)], fill=(38,35,32), width=1)
    f_ph = font("Jura-Light.ttf", 13)
    ph_t = "FOTO"
    draw.text((cx(draw, ph_t, f_ph), mid_y + 36), ph_t, font=f_ph, fill=(42,40,36))

    f_brand = font("BricolageGrotesque-Bold.ttf", 20)
    brand_w = cw(draw, "KORMAN", f_brand)
    draw.text((W - brand_w - 44, H - 40), "KORMAN", font=f_brand, fill=(55,52,48))

    img.save(OUT + "06-historia-46-anos.png", "PNG", dpi=(300,300))
    print("✓  06-historia-46-anos.png")

post_historia_1980()
post_historia_46()

print(f"\n✓ 6 posts v3 listos en posts_v3/")
