#!/usr/bin/env python3
"""
KORMAN — Posts v2
Filosofía: una idea, mucho espacio, tipografía grande.
Referencia visual: Zara, COS, The Row, Bottega.
Foto ocupa 65% del post (placeholder por ahora).
Texto: mínimo, abajo, limpio.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_v2/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

BLACK    = (8, 8, 8)
WHITE    = (252, 250, 246)
OFFWHITE = (245, 243, 238)
GRAY     = (155, 153, 148)
GRAY_DIM = (90, 88, 84)
PHOTO_BG = (22, 20, 18)   # placeholder de foto

def font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def tracked(draw, x, y, text, f, fill, spacing=0):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        b = draw.textbbox((0,0), ch, font=f)
        cx += (b[2]-b[0]) + spacing

def tw(draw, text, f, spacing=0):
    total = 0
    for ch in text:
        b = draw.textbbox((0,0), ch, font=f)
        total += (b[2]-b[0]) + spacing
    return total - spacing

def center_x(draw, text, f, spacing=0):
    return (W - tw(draw, text, f, spacing)) // 2

# ─── TEMPLATE BASE ────────────────────────────────────────────────────────────
# Foto arriba (65%), franja de texto abajo (35%) — fondo negro
def make_post(
    filename,
    headline,          # texto grande
    subline=None,      # texto chico debajo del headline (opcional)
    label=None,        # etiqueta pequeña arriba del headline (opcional)
    bg=BLACK,
    text_color=WHITE,
    sub_color=GRAY,
    photo_placeholder=True,
    photo_height_pct=0.62,  # qué % del alto ocupa la foto
):
    img  = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    ph = int(H * photo_height_pct)   # alto del área de foto
    ty = ph                           # y donde empieza el texto

    # ── Área de foto ──────────────────────────────────────────────────────────
    if photo_placeholder:
        draw.rectangle([0, 0, W, ph], fill=PHOTO_BG)
        # Cruz de placeholder muy sutil
        mid_x, mid_y = W//2, ph//2
        draw.line([(mid_x-30, mid_y), (mid_x+30, mid_y)], fill=(38,35,32), width=1)
        draw.line([(mid_x, mid_y-30), (mid_x, mid_y+30)], fill=(38,35,32), width=1)
        # Texto "FOTO" muy pequeño y sutil
        f_ph = font("Jura-Light.ttf", 13)
        b = draw.textbbox((0,0), "FOTO", font=f_ph)
        draw.text(((W - (b[2]-b[0]))//2, mid_y+18), "FOTO", font=f_ph, fill=(45,42,38))

    # ── Separador ─────────────────────────────────────────────────────────────
    # Nada — el contraste entre foto y fondo es suficiente

    # ── Texto ─────────────────────────────────────────────────────────────────
    text_area_h = H - ph
    padding     = 44

    # Label pequeño arriba (ej: "ETIQUETA TEJIDA · 01")
    if label:
        f_label = font("Jura-Light.ttf", 15)
        b = draw.textbbox((0,0), label, font=f_label)
        lw = b[2]-b[0]
        draw.text(((W-lw)//2, ty + padding), label, font=f_label, fill=sub_color)
        ty_head = ty + padding + 32
    else:
        ty_head = ty + padding

    # Headline — tipografía grande
    f_head = font("BricolageGrotesque-Bold.ttf", 72)
    hx = center_x(draw, headline, f_head, spacing=2)
    tracked(draw, hx, ty_head, headline, f_head, text_color, spacing=2)

    # Subline
    if subline:
        f_sub = font("InstrumentSans-Regular.ttf", 22)
        b = draw.textbbox((0,0), subline, font=f_sub)
        sx = (W - (b[2]-b[0])) // 2
        draw.text((sx, ty_head + 90), subline, font=f_sub, fill=sub_color)

    # KORMAN — abajo centrado, muy pequeño
    f_brand = font("BricolageGrotesque-Bold.ttf", 22)
    bx = center_x(draw, "KORMAN", f_brand, spacing=4)
    tracked(draw, bx, H - 36, "KORMAN", f_brand, (70, 68, 64), spacing=4)

    img.save(OUT + filename, "PNG", dpi=(300,300))
    print(f"✓  {filename}")
    return img


# ═════════════════════════════════════════════════════════════════════════════
# SERIE 1 — TIPOS DE ETIQUETAS (4 posts, uno por tipo)
# ═════════════════════════════════════════════════════════════════════════════

make_post(
    "01-tafeta.png",
    headline = "Tafeta.",
    subline  = "Económica. Para etiquetas internas.",
    label    = "ETIQUETA TEJIDA  ·  01",
)

make_post(
    "02-alta-definicion.png",
    headline = "Alta definición.",
    subline  = "Nítida. Colores intensos. La más elegida.",
    label    = "ETIQUETA TEJIDA  ·  02",
)

make_post(
    "03-triple-densidad.png",
    headline = "Triple densidad.",
    subline  = "Más relieve. Más presencia. Más marca.",
    label    = "ETIQUETA TEJIDA  ·  03",
)

make_post(
    "04-texturada.png",
    headline = "Texturada.",
    subline  = "Para marcas que quieren diferenciarse.",
    label    = "ETIQUETA TEJIDA  ·  04",
)


# ═════════════════════════════════════════════════════════════════════════════
# SERIE 2 — HISTORIA (2 posts)
# ═════════════════════════════════════════════════════════════════════════════

# Post historia 01 — el número
def post_historia_1():
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    # "1980" enorme, centrado, fantasma
    f_ghost = font("BricolageGrotesque-Bold.ttf", 260)
    b = draw.textbbox((0,0), "1980", font=f_ghost)
    gw = b[2]-b[0]
    draw.text(((W-gw)//2, 180), "1980", font=f_ghost, fill=(20,18,16))

    # Encima: texto real
    f_big = font("BricolageGrotesque-Bold.ttf", 110)
    b2 = draw.textbbox((0,0), "1980", font=f_big)
    draw.text(((W-(b2[2]-b2[0]))//2, 260), "1980", font=f_big, fill=WHITE)

    # Línea fina
    draw.line([(160, 430), (W-160, 430)], fill=(45,43,40), width=1)

    # Texto debajo
    f_sub = font("InstrumentSans-Regular.ttf", 28)
    lines = ["Así empezó KORMAN.", "46 años fabricando", "etiquetas en Buenos Aires."]
    for i, l in enumerate(lines):
        b = draw.textbbox((0,0), l, font=f_sub)
        x = (W-(b[2]-b[0]))//2
        col = WHITE if i == 0 else GRAY
        draw.text((x, 464 + i*52), l, font=f_sub, fill=col)

    # KORMAN abajo
    f_brand = font("BricolageGrotesque-Bold.ttf", 22)
    bx = center_x(draw, "KORMAN", f_brand, spacing=4)
    tracked(draw, bx, H-36, "KORMAN", f_brand, (70,68,64), spacing=4)

    img.save(OUT + "05-historia-1980.png", "PNG", dpi=(300,300))
    print("✓  05-historia-1980.png")

post_historia_1()

# Post historia 02 — la continuidad
def post_historia_2():
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    ph = int(H * 0.55)
    draw.rectangle([0, 0, W, ph], fill=PHOTO_BG)
    mid_x, mid_y = W//2, ph//2
    draw.line([(mid_x-30, mid_y),(mid_x+30, mid_y)], fill=(38,35,32), width=1)
    draw.line([(mid_x, mid_y-30),(mid_x, mid_y+30)], fill=(38,35,32), width=1)
    f_ph = font("Jura-Light.ttf", 13)
    b = draw.textbbox((0,0), "FOTO TALLER", font=f_ph)
    draw.text(((W-(b[2]-b[0]))//2, mid_y+18), "FOTO TALLER", font=f_ph, fill=(45,42,38))

    # Texto — simple, una idea
    ty = ph + 52
    f_big  = font("BricolageGrotesque-Bold.ttf", 68)
    f_sub  = font("InstrumentSans-Regular.ttf", 24)
    f_sm   = font("Jura-Light.ttf", 16)

    b = draw.textbbox((0,0), "46 años.", font=f_big)
    draw.text(((W-(b[2]-b[0]))//2, ty), "46 años.", font=f_big, fill=WHITE)

    b2 = draw.textbbox((0,0), "El mismo oficio. La misma dedicación.", font=f_sub)
    draw.text(((W-(b2[2]-b2[0]))//2, ty+90), "El mismo oficio. La misma dedicación.", font=f_sub, fill=GRAY)

    draw.line([(200, ty+150), (W-200, ty+150)], fill=(40,38,34), width=1)

    detail = "Buenos Aires · desde 1980"
    b3 = draw.textbbox((0,0), detail, font=f_sm)
    draw.text(((W-(b3[2]-b3[0]))//2, ty+174), detail, font=f_sm, fill=(70,68,64))

    f_brand = font("BricolageGrotesque-Bold.ttf", 22)
    bx = center_x(draw, "KORMAN", f_brand, spacing=4)
    tracked(draw, bx, H-36, "KORMAN", f_brand, (70,68,64), spacing=4)

    img.save(OUT + "06-historia-46-anos.png", "PNG", dpi=(300,300))
    print("✓  06-historia-46-anos.png")

post_historia_2()

print("\n✓ 6 posts v2 listos en posts_v2/")
print("Cuando lleguen las fotos, se reemplazan los placeholders y quedan publicables.")
