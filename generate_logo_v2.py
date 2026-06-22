#!/usr/bin/env python3
"""
KORMAN — Logo v2
Tipografía de empresa millonaria. Sin ícono. Solo wordmark.
Referencia: Celine, The Row, Bottega Veneta, Zara.
Negro puro, letra espaciada, línea fina.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/.agents/design/logo/"
os.makedirs(OUT, exist_ok=True)

BLACK    = (8, 8, 8)
WHITE    = (255, 255, 255)
OFFWHITE = (250, 248, 244)
GRAY     = (160, 158, 154)
GRAY_DIM = (110, 108, 104)

def load_font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def draw_tracked_text(draw, x, y, text, font, fill, tracking=0):
    """Dibuja texto con tracking (espaciado entre letras) manual."""
    cursor_x = x
    for ch in text:
        draw.text((cursor_x, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font)
        cursor_x += (bbox[2] - bbox[0]) + tracking
    # Retorna el ancho total
    total = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        total += (bbox[2] - bbox[0]) + tracking
    return total - tracking  # sin tracking extra al final

def tracked_width(draw, text, font, tracking=0):
    total = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        total += (bbox[2] - bbox[0]) + tracking
    return max(total - tracking, 0)

# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN HORIZONTAL — fondo blanco
# Inspiración: Celine / The Row — wordmark puro, espaciado, autoridad
# ══════════════════════════════════════════════════════════════════════════════
def logo_h_white():
    W, H = 1400, 360
    img  = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)

    f_main = load_font("BricolageGrotesque-Bold.ttf", 148)   # fuerte, moderno
    f_sub  = load_font("InstrumentSans-Regular.ttf", 24)
    f_tiny = load_font("Jura-Light.ttf", 17)

    TRACKING_MAIN = 14   # espaciado entre letras del nombre
    TRACKING_SUB  = 8

    main_w = tracked_width(draw, "KORMAN", f_main, TRACKING_MAIN)
    sub_w  = tracked_width(draw, "ETIQUETAS BORDADAS", f_sub, TRACKING_SUB)

    # Centrar todo
    cx = W // 2
    start_main = cx - main_w // 2
    start_sub  = cx - sub_w  // 2

    # "KORMAN"
    draw_tracked_text(draw, start_main, 60, "KORMAN", f_main, BLACK, TRACKING_MAIN)

    # Línea fina — del ancho del nombre
    line_y = 232
    draw.line([(start_main, line_y), (start_main + main_w, line_y)],
              fill=BLACK, width=1)

    # "ETIQUETAS BORDADAS"
    draw_tracked_text(draw, start_sub, 254, "ETIQUETAS BORDADAS", f_sub, BLACK, TRACKING_SUB)

    # "Buenos Aires · desde 1980" — derecha, alineado al borde del nombre
    tiny_text = "Buenos Aires  ·  desde 1980"
    tiny_w = tracked_width(draw, tiny_text, f_tiny, 2)
    draw_tracked_text(draw, start_main + main_w - tiny_w, 305,
                      tiny_text, f_tiny, GRAY, 2)

    path = OUT + "korman-logo-v2-horizontal-blanco.png"
    img.save(path, "PNG", dpi=(300, 300))
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN HORIZONTAL — fondo negro
# ══════════════════════════════════════════════════════════════════════════════
def logo_h_black():
    W, H = 1400, 360
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    f_main = load_font("BricolageGrotesque-Bold.ttf", 148)
    f_sub  = load_font("InstrumentSans-Regular.ttf", 24)
    f_tiny = load_font("Jura-Light.ttf", 17)

    TRACKING_MAIN = 14
    TRACKING_SUB  = 8

    main_w = tracked_width(draw, "KORMAN", f_main, TRACKING_MAIN)
    sub_w  = tracked_width(draw, "ETIQUETAS BORDADAS", f_sub, TRACKING_SUB)

    cx = W // 2
    start_main = cx - main_w // 2
    start_sub  = cx - sub_w  // 2

    draw_tracked_text(draw, start_main, 60, "KORMAN", f_main, OFFWHITE, TRACKING_MAIN)

    line_y = 232
    draw.line([(start_main, line_y), (start_main + main_w, line_y)],
              fill=(55, 53, 49), width=1)

    draw_tracked_text(draw, start_sub, 254, "ETIQUETAS BORDADAS", f_sub, OFFWHITE, TRACKING_SUB)

    tiny_text = "Buenos Aires  ·  desde 1980"
    tiny_w = tracked_width(draw, tiny_text, f_tiny, 2)
    draw_tracked_text(draw, start_main + main_w - tiny_w, 305,
                      tiny_text, f_tiny, GRAY_DIM, 2)

    path = OUT + "korman-logo-v2-horizontal-negro.png"
    img.save(path, "PNG", dpi=(300, 300))
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════════════════════
# AVATAR INSTAGRAM — cuadrado negro, solo "KORMAN"
# ══════════════════════════════════════════════════════════════════════════════
def logo_avatar():
    S = 1000
    img  = Image.new("RGB", (S, S), BLACK)
    draw = ImageDraw.Draw(img)

    f_main = load_font("BricolageGrotesque-Bold.ttf", 148)
    f_sub  = load_font("InstrumentSans-Regular.ttf", 26)

    TRACKING_MAIN = 10
    TRACKING_SUB  = 10

    main_w = tracked_width(draw, "KORMAN", f_main, TRACKING_MAIN)
    sub_w  = tracked_width(draw, "ETIQUETAS BORDADAS", f_sub, TRACKING_SUB)

    cx = S // 2

    # Centrar verticalmente
    start_y_main = (S - 170 - 50 - 36) // 2  # altura aprox bloque
    draw_tracked_text(draw, cx - main_w // 2, start_y_main,
                      "KORMAN", f_main, OFFWHITE, TRACKING_MAIN)

    line_y = start_y_main + 175
    draw.line([(cx - main_w // 2, line_y), (cx + main_w // 2, line_y)],
              fill=(50, 48, 44), width=1)

    draw_tracked_text(draw, cx - sub_w // 2, line_y + 22,
                      "ETIQUETAS BORDADAS", f_sub, GRAY_DIM, TRACKING_SUB)

    path = OUT + "korman-logo-v2-avatar.png"
    img.save(path, "PNG", dpi=(300, 300))
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN COMPACTA — solo "KORMAN" para watermark en posts
# ══════════════════════════════════════════════════════════════════════════════
def logo_watermark():
    # Blanco sobre transparente
    W, H = 600, 120
    img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    f = load_font("BricolageGrotesque-Bold.ttf", 90)
    TRACKING = 8
    w = tracked_width(draw, "KORMAN", f, TRACKING)
    draw_tracked_text(draw, (W - w) // 2, 10, "KORMAN", f,
                      (255, 255, 255, 220), TRACKING)

    img.save(OUT + "korman-watermark-blanco.png", "PNG")
    print(f"✓ {OUT}korman-watermark-blanco.png")

    # Negro sobre transparente
    img2  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)
    draw_tracked_text(draw2, (W - w) // 2, 10, "KORMAN", f,
                      (8, 8, 8, 200), TRACKING)
    img2.save(OUT + "korman-watermark-negro.png", "PNG")
    print(f"✓ {OUT}korman-watermark-negro.png")

# ── Run ───────────────────────────────────────────────────────────────────────
print("Generando logos KORMAN v2...")
logo_h_white()
logo_h_black()
logo_avatar()
logo_watermark()
print("\n✓ Logo v2 completo.")
