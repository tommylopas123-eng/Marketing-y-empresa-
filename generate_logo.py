#!/usr/bin/env python3
"""
KORMAN — Logo Generator
Negro con detalles modernos. Versiones: horizontal, cuadrado, ícono solo.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/.agents/design/logo/"
os.makedirs(OUT, exist_ok=True)

def load_font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

# ── Paleta ────────────────────────────────────────────────────────────────────
BLACK      = (10, 10, 10)
WHITE      = (255, 255, 255)
OFFWHITE   = (245, 243, 238)
GRAY_LIGHT = (200, 198, 194)
GRAY_MID   = (140, 138, 134)

# ══════════════════════════════════════════════════════════════════════════════
# ÍCONO — geometría de tejido / hilo cruzado
# Un rombo con hilos cruzados que sugiere la trama de una etiqueta tejida
# ══════════════════════════════════════════════════════════════════════════════
def draw_icon(draw, cx, cy, size, color, bg_color=None, stroke=2):
    """
    Ícono KORMAN: cuadrado rotado 45° (rombo) con líneas de trama internas.
    Representa el punto de inicio de una etiqueta tejida.
    """
    half = size // 2

    # Rombo exterior (cuadrado rotado)
    diamond = [
        (cx, cy - half),
        (cx + half, cy),
        (cx, cy + half),
        (cx - half, cy)
    ]
    if bg_color:
        draw.polygon(diamond, fill=bg_color)
    draw.polygon(diamond, outline=color, fill=None, width=stroke)

    # Cruz interior — dos líneas diagonales (trama del tejido)
    inset = half // 3
    draw.line([(cx - inset, cy - inset*2), (cx + inset, cy + inset*2)], fill=color, width=stroke)
    draw.line([(cx + inset, cy - inset*2), (cx - inset, cy + inset*2)], fill=color, width=stroke)

    # Punto central
    r = stroke + 1
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)

    # Líneas horizontales de trama (3 líneas paralelas dentro del rombo)
    for offset in [-half//3, 0, half//3]:
        # Calcular intersección con el rombo
        y_abs = cy + offset
        dx = half - abs(offset)  # ancho en ese y
        margin = stroke + 2
        if dx > margin * 2:
            draw.line([(cx - dx + margin, y_abs), (cx + dx - margin, y_abs)],
                     fill=color, width=1)


# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN 1: Logo horizontal — fondo blanco
# ══════════════════════════════════════════════════════════════════════════════
def logo_horizontal_white():
    W, H = 1200, 400
    img  = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)

    icon_size = 140
    icon_x, icon_y = 120, H // 2

    draw_icon(draw, icon_x, icon_y, icon_size, BLACK, bg_color=None, stroke=3)

    # Línea vertical separadora
    sep_x = 210
    draw.line([(sep_x, H//2 - 80), (sep_x, H//2 + 80)], fill=GRAY_MID, width=1)

    # "KORMAN" — tipografía principal
    f_brand = load_font("InstrumentSans-Bold.ttf", 108)
    f_sub   = load_font("Jura-Light.ttf", 24)

    text_x = sep_x + 40
    draw.text((text_x, H//2 - 72), "KORMAN", font=f_brand, fill=BLACK)

    # "ETIQUETAS TEJIDAS" — subtítulo espaciado
    sub_text = "E T I Q U E T A S   T E J I D A S"
    draw.text((text_x + 4, H//2 + 52), sub_text, font=f_sub, fill=GRAY_MID)

    # Punto decorativo — detalle moderno
    draw.ellipse([text_x + 4, H//2 + 92, text_x + 10, H//2 + 98], fill=BLACK)
    draw.text((text_x + 20, H//2 + 86), "Buenos Aires · desde 1978",
              font=load_font("Jura-Light.ttf", 18), fill=GRAY_LIGHT)

    path = OUT + "korman-logo-horizontal-blanco.png"
    img.save(path, "PNG", dpi=(300, 300))
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN 2: Logo horizontal — fondo negro (para Instagram)
# ══════════════════════════════════════════════════════════════════════════════
def logo_horizontal_black():
    W, H = 1200, 400
    img  = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    icon_size = 140
    icon_x, icon_y = 120, H // 2

    draw_icon(draw, icon_x, icon_y, icon_size, OFFWHITE, bg_color=None, stroke=3)

    sep_x = 210
    draw.line([(sep_x, H//2 - 80), (sep_x, H//2 + 80)], fill=(60, 58, 54), width=1)

    f_brand = load_font("InstrumentSans-Bold.ttf", 108)
    f_sub   = load_font("Jura-Light.ttf", 24)

    text_x = sep_x + 40
    draw.text((text_x, H//2 - 72), "KORMAN", font=f_brand, fill=OFFWHITE)

    sub_text = "E T I Q U E T A S   T E J I D A S"
    draw.text((text_x + 4, H//2 + 52), sub_text, font=f_sub, fill=(100, 98, 94))

    draw.ellipse([text_x + 4, H//2 + 92, text_x + 10, H//2 + 98], fill=OFFWHITE)
    draw.text((text_x + 20, H//2 + 86), "Buenos Aires · desde 1978",
              font=load_font("Jura-Light.ttf", 18), fill=(70, 68, 64))

    path = OUT + "korman-logo-horizontal-negro.png"
    img.save(path, "PNG", dpi=(300, 300))
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN 3: Logo cuadrado — para avatar de Instagram (1:1)
# ══════════════════════════════════════════════════════════════════════════════
def logo_square_black():
    S = 1000
    img  = Image.new("RGB", (S, S), BLACK)
    draw = ImageDraw.Draw(img)

    # Ícono centrado arriba
    draw_icon(draw, S//2, 340, 220, OFFWHITE, bg_color=None, stroke=4)

    # Línea horizontal
    draw.line([(120, 500), (S - 120, 500)], fill=(40, 38, 34), width=1)

    # "KORMAN" centrado
    f_brand = load_font("InstrumentSans-Bold.ttf", 120)
    f_sub   = load_font("Jura-Light.ttf", 26)

    # Calcular centro del texto
    bbox = draw.textbbox((0, 0), "KORMAN", font=f_brand)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) // 2, 530), "KORMAN", font=f_brand, fill=OFFWHITE)

    sub = "ETIQUETAS  TEJIDAS"
    bbox2 = draw.textbbox((0, 0), sub, font=f_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((S - tw2) // 2, 680), sub, font=f_sub, fill=(90, 88, 84))

    # Detalle: dos líneas cortas debajo del subtítulo (referencia al tejido)
    mid = S // 2
    draw.line([(mid - 60, 740), (mid - 10, 740)], fill=(60, 58, 54), width=1)
    draw.line([(mid + 10, 740), (mid + 60, 740)], fill=(60, 58, 54), width=1)
    draw.ellipse([(mid - 5, 736), (mid + 5, 746)], fill=(60, 58, 54))

    path = OUT + "korman-logo-cuadrado-negro.png"
    img.save(path, "PNG", dpi=(300, 300))
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════════════════════
# VERSIÓN 4: Solo ícono — para watermark en posts
# ══════════════════════════════════════════════════════════════════════════════
def logo_icon_only():
    S = 400
    # Versión blanca sobre negro
    img  = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_icon(draw, S//2, S//2, 280, OFFWHITE, bg_color=None, stroke=5)
    img.save(OUT + "korman-icono-blanco-transparente.png", "PNG")
    print(f"✓ {OUT}korman-icono-blanco-transparente.png")

    # Versión negro sobre blanco
    img2  = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)
    draw_icon(draw2, S//2, S//2, 280, BLACK, bg_color=None, stroke=5)
    img2.save(OUT + "korman-icono-negro-transparente.png", "PNG")
    print(f"✓ {OUT}korman-icono-negro-transparente.png")

# ── Run ───────────────────────────────────────────────────────────────────────
print("Generando logos KORMAN...")
logo_horizontal_white()
logo_horizontal_black()
logo_square_black()
logo_icon_only()
print("\n✓ 4 versiones del logo generadas en .agents/design/logo/")
