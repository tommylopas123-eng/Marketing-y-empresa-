#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Posts v4 "Silencio Textil"
Filosofía: Toteme / COS / The Row — museo, espacio, autoridad tipográfica.
Texto arriba con espacio monumental. Foto abajo como artefacto.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_v4/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

# Paleta "Silencio Textil" — tres tonos, inevitable
BLACK    = (8,   8,   8  )   # fondo principal
WHITE    = (252, 250, 246)   # texto primario
GRAY_MD  = (150, 148, 144)   # subtítulo
GRAY_DIM = (68,  66,  62 )   # label / marca
GRAY_LN  = (28,  26,  22 )   # línea separadora
PHOTO_BG = (16,  14,  12 )   # zona de foto (ligeramente más cálida que el fondo)
PHOTO_MK = (32,  30,  26 )   # marcadores del placeholder
PHOTO_TXT= (44,  42,  38 )   # texto dentro del placeholder


def f(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()


def text_w(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def text_h(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[3] - b[1]


def cx(draw, text, font):
    return (W - text_w(draw, text, font)) // 2


def draw_tracked(draw, x, y, text, font, fill, tracking=0):
    """Dibuja texto con tracking manual entre caracteres."""
    cursor = x
    for ch in text:
        draw.text((cursor, y), ch, font=font, fill=fill)
        b = draw.textbbox((0, 0), ch, font=font)
        cursor += (b[2] - b[0]) + tracking
    return cursor


def tracked_width(draw, text, font, tracking=0):
    total = 0
    for i, ch in enumerate(text):
        b = draw.textbbox((0, 0), ch, font=font)
        total += (b[2] - b[0])
        if i < len(text) - 1:
            total += tracking
    return total


def cx_tracked(text, font, draw, tracking=0):
    return (W - tracked_width(draw, text, font, tracking)) // 2


def draw_photo_placeholder(draw, y_start, y_end, label="FOTO"):
    """Zona de foto: fondo oscuro, cruz central, texto sutil."""
    draw.rectangle([0, y_start, W, y_end], fill=PHOTO_BG)

    # Cruz de registro muy sutil
    mid_x = W // 2
    mid_y = (y_start + y_end) // 2
    arm = 22
    draw.line([(mid_x - arm, mid_y), (mid_x + arm, mid_y)], fill=PHOTO_MK, width=1)
    draw.line([(mid_x, mid_y - arm), (mid_x, mid_y + arm)], fill=PHOTO_MK, width=1)

    # Círculo de registro
    r = 6
    draw.ellipse([mid_x - r, mid_y - r, mid_x + r, mid_y + r], outline=PHOTO_MK, width=1)

    # Texto placeholder
    f_ph = f("Jura-Light.ttf", 12)
    pw = text_w(draw, label, f_ph)
    draw.text(((W - pw) // 2, mid_y + 32), label, font=f_ph, fill=PHOTO_TXT)


def draw_brand_mark(draw, y=None):
    """KORMAN ETIQUETAS — marca sutil abajo a la derecha."""
    if y is None:
        y = H - 36
    f_b = f("BricolageGrotesque-Bold.ttf", 14)
    brand = "KORMAN ETIQUETAS"
    bw = tracked_width(draw, brand, f_b, tracking=2)
    x = W - bw - 40
    draw_tracked(draw, x, y, brand, f_b, GRAY_DIM, tracking=2)


def draw_thin_rule(draw, y, x0=60, x1=None):
    """Línea fina separadora."""
    if x1 is None:
        x1 = W - 60
    draw.line([(x0, y), (x1, y)], fill=GRAY_LN, width=1)


# ─────────────────────────────────────────────────────────────────────────────
# POST TIPO ESTÁNDAR — texto arriba, foto abajo
# ─────────────────────────────────────────────────────────────────────────────

def make_post_standard(filename, title, subtitle, label, photo_pct=0.52):
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    photo_h = int(H * photo_pct)
    text_h_  = H - photo_h
    sep_y   = text_h_  # separador entre texto y foto

    # ── ZONA DE TEXTO ──────────────────────────────────────────────────────
    pad_top = 80

    # Label — Jura Light, muy pequeño, tracking amplio
    f_label = f("Jura-Light.ttf", 15)
    tracking_label = 4
    lw = tracked_width(draw, label, f_label, tracking_label)
    lx = (W - lw) // 2
    draw_tracked(draw, lx, pad_top, label, f_label, GRAY_DIM, tracking_label)

    # Espacio entre label y título — generoso
    title_y = pad_top + 58

    # Título — BricolageGrotesque Bold, grande, tracking 3
    f_title = f("BricolageGrotesque-Bold.ttf", 108)
    tracking_title = 3

    # Auto-reducir si no entra
    while tracked_width(draw, title, f_title, tracking_title) > W - 100:
        size = f_title.size - 4
        if size < 56:
            break
        f_title = f("BricolageGrotesque-Bold.ttf", size)

    tw = tracked_width(draw, title, f_title, tracking_title)
    tx = (W - tw) // 2
    draw_tracked(draw, tx, title_y, title, f_title, WHITE, tracking_title)

    # Espacio generoso entre título y subtítulo
    subtitle_y = title_y + f_title.size + 36

    # Subtítulo — InstrumentSans Regular, tracking suave
    f_sub = f("InstrumentSans-Regular.ttf", 24)
    tracking_sub = 1
    sw = tracked_width(draw, subtitle, f_sub, tracking_sub)
    sx = (W - sw) // 2
    draw_tracked(draw, sx, subtitle_y, subtitle, f_sub, GRAY_MD, tracking_sub)

    # ── SEPARADOR ──────────────────────────────────────────────────────────
    draw_thin_rule(draw, sep_y - 1)

    # ── ZONA DE FOTO ───────────────────────────────────────────────────────
    draw_photo_placeholder(draw, sep_y, H, "FOTO")

    # ── MARCA ──────────────────────────────────────────────────────────────
    draw_brand_mark(draw, H - 32)

    img.save(OUT + filename, "PNG", dpi=(300, 300))
    print(f"✓  {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# POST HISTORIA 1980
# ─────────────────────────────────────────────────────────────────────────────

def post_historia_1980():
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    photo_pct = 0.28
    photo_h = int(H * photo_pct)
    sep_y = H - photo_h

    pad = 72

    # Label
    f_label = f("Jura-Light.ttf", 15)
    label = "HISTORIA  ·  01"
    lw = tracked_width(draw, label, f_label, 4)
    draw_tracked(draw, (W - lw) // 2, pad, label, f_label, GRAY_DIM, 4)

    # "1980" — número héroe, enorme
    f_year = f("BricolageGrotesque-Bold.ttf", 200)
    year_y = pad + 52

    # Efecto fantasma — número detrás, en negro profundo
    ghost_col = (20, 18, 14)
    yw = tracked_width(draw, "1980", f_year, 2)
    draw_tracked(draw, (W - yw) // 2 + 4, year_y + 4, "1980", f_year, ghost_col, 2)
    draw_tracked(draw, (W - yw) // 2, year_y, "1980", f_year, WHITE, 2)

    # Línea fina bajo el número
    rule_y = year_y + f_year.size + 12
    draw_thin_rule(draw, rule_y, x0=120, x1=W - 120)

    # Subtítulo
    f_sub = f("InstrumentSans-Regular.ttf", 24)
    sub = "Así empezó KORMAN ETIQUETAS en Buenos Aires"
    sw = tracked_width(draw, sub, f_sub, 0)

    # Si no entra, dividir en dos líneas
    if sw > W - 100:
        line1 = "Así empezó KORMAN ETIQUETAS"
        line2 = "en Buenos Aires"
        sub_y = rule_y + 28
        lw1 = text_w(draw, line1, f_sub)
        lw2 = text_w(draw, line2, f_sub)
        draw.text(((W - lw1) // 2, sub_y), line1, font=f_sub, fill=GRAY_MD)
        draw.text(((W - lw2) // 2, sub_y + 36), line2, font=f_sub, fill=GRAY_MD)
    else:
        sw_x = (W - sw) // 2
        draw_tracked(draw, sw_x, rule_y + 28, sub, f_sub, GRAY_MD, 0)

    # Separador zona foto
    draw_thin_rule(draw, sep_y - 1)

    # Zona foto (taller histórico)
    draw_photo_placeholder(draw, sep_y, H, "FOTO TALLER")

    draw_brand_mark(draw, H - 32)

    img.save(OUT + "05-historia-1980.png", "PNG", dpi=(300, 300))
    print("✓  05-historia-1980.png")


# ─────────────────────────────────────────────────────────────────────────────
# POST HISTORIA 46 AÑOS
# ─────────────────────────────────────────────────────────────────────────────

def post_historia_46():
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    photo_pct = 0.52
    photo_h = int(H * photo_pct)
    sep_y = H - photo_h

    pad = 80

    # Label
    f_label = f("Jura-Light.ttf", 15)
    label = "HISTORIA  ·  02"
    lw = tracked_width(draw, label, f_label, 4)
    draw_tracked(draw, (W - lw) // 2, pad, label, f_label, GRAY_DIM, 4)

    # Título "46 AÑOS"
    f_title = f("BricolageGrotesque-Bold.ttf", 108)
    title = "46 AÑOS"
    title_y = pad + 58
    tw = tracked_width(draw, title, f_title, 3)
    draw_tracked(draw, (W - tw) // 2, title_y, title, f_title, WHITE, 3)

    # Subtítulo
    f_sub = f("InstrumentSans-Regular.ttf", 24)
    sub = "El mismo oficio  ·  la misma dedicación"
    sw = tracked_width(draw, sub, f_sub, 0)
    sub_y = title_y + f_title.size + 36
    draw.text(((W - sw) // 2, sub_y), sub, font=f_sub, fill=GRAY_MD)

    # Separador
    draw_thin_rule(draw, sep_y - 1)

    # Zona foto
    draw_photo_placeholder(draw, sep_y, H, "FOTO")

    draw_brand_mark(draw, H - 32)

    img.save(OUT + "06-historia-46-anos.png", "PNG", dpi=(300, 300))
    print("✓  06-historia-46-anos.png")


# ═════════════════════════════════════════════════════════════════════════════
# GENERAR TODOS LOS POSTS
# ═════════════════════════════════════════════════════════════════════════════

make_post_standard(
    "01-tafeta.png",
    title    = "TAFETA",
    subtitle = "Económica  ·  para etiquetas internas",
    label    = "ETIQUETA BORDADA  ·  01",
    photo_pct= 0.55,
)

make_post_standard(
    "02-alta-definicion.png",
    title    = "ALTA DEFINICIÓN",
    subtitle = "Nítida  ·  colores intensos  ·  la más elegida",
    label    = "ETIQUETA BORDADA  ·  02",
    photo_pct= 0.52,
)

make_post_standard(
    "03-triple-densidad.png",
    title    = "TRIPLE DENSIDAD",
    subtitle = "Mayor relieve  ·  presencia  ·  efecto premium",
    label    = "ETIQUETA BORDADA  ·  03",
    photo_pct= 0.52,
)

make_post_standard(
    "04-texturada.png",
    title    = "TEXTURADA",
    subtitle = "Relieve especial  ·  para marcas que se diferencian",
    label    = "ETIQUETA BORDADA  ·  04",
    photo_pct= 0.52,
)

post_historia_1980()
post_historia_46()

print(f"\n✓  6 posts v4 guardados en posts_v4/")
