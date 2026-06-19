#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Posts v4 "Silencio Textil"
Filosofía: Toteme / COS / The Row — museo, espacio, autoridad tipográfica.
Etiqueta compuesta directo sobre el fondo — un solo conjunto, sin zonas separadas.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS    = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT      = "/home/user/Marketing-y-empresa-/posts_v4/"
FOTOS    = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

BLACK   = (8,   8,   8  )
WHITE   = (252, 250, 246)
GRAY_MD = (150, 148, 144)
GRAY_DIM= (68,  66,  62 )
GRAY_LN = (28,  26,  22 )


def f(name, size):
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


def draw_tracked(draw, x, y, text, font, fill, tracking=0):
    cursor = x
    for ch in text:
        draw.text((cursor, y), ch, font=font, fill=fill)
        b = draw.textbbox((0, 0), ch, font=font)
        cursor += (b[2] - b[0]) + tracking
    return cursor


def cx_t(draw, text, font, tracking=0):
    return (W - tw(draw, text, font, tracking)) // 2


def brand_mark(draw):
    fb = f("BricolageGrotesque-Bold.ttf", 14)
    brand = "KORMAN ETIQUETAS"
    bw = tw(draw, brand, fb, 2)
    draw_tracked(draw, W - bw - 40, H - 36, brand, fb, GRAY_DIM, 2)


def thin_rule(draw, y, x0=60, x1=None):
    draw.line([(x0, y), (x1 or W - 60, y)], fill=GRAY_LN, width=1)


def paste_label(img, png_name, y_top, y_bot, max_fill=0.82):
    """Composita el PNG transparente de la etiqueta sobre el fondo negro del post."""
    path = FOTOS + png_name
    try:
        label = Image.open(path).convert("RGBA")
    except Exception as e:
        print(f"  [warn] {e}")
        return

    zone_w = W
    zone_h = y_bot - y_top
    lw, lh = label.size
    scale = min((zone_w * max_fill) / lw, (zone_h * max_fill) / lh)
    new_w, new_h = int(lw * scale), int(lh * scale)
    label = label.resize((new_w, new_h), Image.LANCZOS)

    x = (zone_w - new_w) // 2
    y = y_top + (zone_h - new_h) // 2

    # Compositar sobre el canvas (que ya tiene fondo negro)
    img.paste(label, (x, y), label)


# ─────────────────────────────────────────────────────────────────────────────
# MAKE POST — texto arriba, etiqueta abajo, todo sobre fondo negro continuo
# ─────────────────────────────────────────────────────────────────────────────

def make_post(filename, title, subtitle, label_txt, png_label, photo_pct=0.55):
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    sep_y = int(H * (1 - photo_pct))   # dónde termina el texto y empieza la etiqueta

    # ── LABEL ────────────────────────────────────────────────────────────────
    pad_top = 72
    f_lbl = f("Jura-Light.ttf", 15)
    lw_ = tw(draw, label_txt, f_lbl, 4)
    draw_tracked(draw, (W - lw_) // 2, pad_top, label_txt, f_lbl, GRAY_DIM, 4)

    # ── TÍTULO ───────────────────────────────────────────────────────────────
    title_y = pad_top + 52
    f_t = f("BricolageGrotesque-Bold.ttf", 108)
    while tw(draw, title, f_t, 3) > W - 80:
        sz = f_t.size - 4
        if sz < 52: break
        f_t = f("BricolageGrotesque-Bold.ttf", sz)

    draw_tracked(draw, cx_t(draw, title, f_t, 3), title_y, title, f_t, WHITE, 3)

    # ── SUBTÍTULO ────────────────────────────────────────────────────────────
    sub_y = title_y + f_t.size + 28
    f_s = f("InstrumentSans-Regular.ttf", 22)
    draw_tracked(draw, cx_t(draw, subtitle, f_s, 0), sub_y, subtitle, f_s, GRAY_MD, 0)

    # ── LÍNEA SEPARADORA SUTIL ───────────────────────────────────────────────
    thin_rule(draw, sep_y - 1)

    # ── ETIQUETA (PNG transparente sobre fondo negro continuo) ───────────────
    paste_label(img, png_label, sep_y, H - 48)
    draw = ImageDraw.Draw(img)  # re-bind tras paste

    # ── MARCA ────────────────────────────────────────────────────────────────
    brand_mark(draw)

    img.save(OUT + filename, "PNG", dpi=(300, 300))
    print(f"✓  {filename}")


# ═════════════════════════════════════════════════════════════════════════════
# POSTS — solo los que tienen foto confirmada
# ═════════════════════════════════════════════════════════════════════════════

# TAFETA — única foto tafeta confirmada: nxlevel
make_post(
    "01-tafeta.png",
    title     = "TAFETA",
    subtitle  = "Económica  ·  para etiquetas internas",
    label_txt = "ETIQUETA BORDADA  ·  01",
    png_label = "nxlevel-transparente.png",
    photo_pct = 0.55,
)

# ALTA DEFINICIÓN — fotos confirmadas: givenchy, balmain, beditorial, tough, pierre-cardin, elmo, camp, converse, precioux
# Usamos la más representativa y limpia
make_post(
    "02-alta-definicion.png",
    title     = "ALTA DEFINICIÓN",
    subtitle  = "Nítida  ·  colores intensos  ·  la más elegida",
    label_txt = "ETIQUETA BORDADA  ·  02",
    png_label = "givenchy-denim-transparente.png",
    photo_pct = 0.55,
)

print(f"\n✓  Posts listos en posts_v4/")
