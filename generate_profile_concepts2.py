#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Profile photo concepts v2
Beyond the single K — full brand expressions
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT = "/home/user/Marketing-y-empresa-/assets/"

def fnt(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def th(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[3] - b[1]

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO 1 — SELLO CIRCULAR
# "KORMAN ETIQUETAS" en arco superior + "EST. 1980" en arco inferior
# K grande en el centro — tipo sello de casa de moda
# ─────────────────────────────────────────────────────────────────────────────
def concepto_sello():
    S = 1000
    img = Image.new("RGB", (S, S), (8, 8, 8))
    draw = ImageDraw.Draw(img)

    cx, cy = S // 2, S // 2
    r_outer = 460
    r_inner = 400

    # Círculo exterior
    draw.ellipse([cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer], outline=(252,250,246), width=2)
    draw.ellipse([cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner], outline=(252,250,246), width=1)

    # Texto en arco superior: KORMAN ETIQUETAS
    f_arc = fnt("Jura-Light.ttf", 32)
    text_top = "KORMAN  ETIQUETAS"
    r_text = 430
    # Distribuir letras en arco
    total_angle = 160  # grados
    start_angle = -90 - total_angle/2  # arriba
    chars = list(text_top)
    angle_step = total_angle / max(len(chars)-1, 1)
    for i, ch in enumerate(chars):
        angle_deg = start_angle + i * angle_step
        angle_rad = math.radians(angle_deg)
        x = cx + r_text * math.cos(angle_rad)
        y = cy + r_text * math.sin(angle_rad)
        cw = tw(draw, ch, f_arc)
        ch_img = Image.new("RGBA", (60, 60), (0,0,0,0))
        ch_draw = ImageDraw.Draw(ch_img)
        ch_draw.text((30 - cw//2, 5), ch, font=f_arc, fill=(252,250,246,255))
        rotated = ch_img.rotate(-(angle_deg + 90), expand=False)
        rx = int(x) - 30
        ry = int(y) - 30
        img.paste(rotated, (rx, ry), rotated)

    # Texto en arco inferior: EST. 1980
    f_arc2 = fnt("Jura-Light.ttf", 28)
    text_bot = "BORDADAS  ·  EST. 1980"
    total_angle2 = 130
    start_angle2 = 90 - total_angle2/2
    chars2 = list(text_bot)
    angle_step2 = total_angle2 / max(len(chars2)-1, 1)
    for i, ch in enumerate(chars2):
        angle_deg = start_angle2 + i * angle_step2
        angle_rad = math.radians(angle_deg)
        x = cx + r_text * math.cos(angle_rad)
        y = cy + r_text * math.sin(angle_rad)
        cw = tw(draw, ch, f_arc2)
        ch_img = Image.new("RGBA", (60, 60), (0,0,0,0))
        ch_draw = ImageDraw.Draw(ch_img)
        ch_draw.text((30 - cw//2, 5), ch, font=f_arc2, fill=(252,250,246,255))
        rotated = ch_img.rotate(-(angle_deg + 90) + 180, expand=False)
        rx = int(x) - 30
        ry = int(y) - 30
        img.paste(rotated, (rx, ry), rotated)

    # K central grande
    f_k = fnt("BricolageGrotesque-Bold.ttf", 280)
    k_w = tw(draw, "K", f_k)
    k_h = th(draw, "K", f_k)
    draw.text((cx - k_w//2, cy - k_h//2 - 10), "K", font=f_k, fill=(252,250,246))

    img.save(OUT + "perfil-sello-circular.jpg", "JPEG", quality=95)
    print("✓ perfil-sello-circular.jpg")

concepto_sello()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO 2 — WORDMARK STACKED MINIMALISTA
# "KORMAN" grande arriba / línea fina / "ETIQUETAS" abajo más chico
# Fondo negro, letras blancas — tipo The Row, COS
# ─────────────────────────────────────────────────────────────────────────────
def concepto_wordmark():
    S = 1000
    img = Image.new("RGB", (S, S), (8, 8, 8))
    draw = ImageDraw.Draw(img)
    cx = S // 2

    # KORMAN — grande
    f_k = fnt("BricolageGrotesque-Bold.ttf", 148)
    while tw(draw, "KORMAN", f_k) > 820:
        f_k = fnt("BricolageGrotesque-Bold.ttf", f_k.size - 4)
    kw = tw(draw, "KORMAN", f_k)
    kh = th(draw, "KORMAN", f_k)
    k_y = S//2 - kh - 18

    # ETIQUETAS — que tenga el mismo ancho que KORMAN
    f_e = fnt("Jura-Light.ttf", 52)
    while tw(draw, "ETIQUETAS", f_e) > kw:
        f_e = fnt("Jura-Light.ttf", f_e.size - 2)
    while tw(draw, "ETIQUETAS", f_e) < kw - 10:
        f_e = fnt("Jura-Light.ttf", f_e.size + 2)
    ew = tw(draw, "ETIQUETAS", f_e)
    e_y = S//2 + 18

    draw.text((cx - kw//2, k_y), "KORMAN", font=f_k, fill=(252,250,246))

    # Línea separadora del mismo ancho que KORMAN
    line_y = S//2
    draw.line([(cx - kw//2, line_y), (cx + kw//2, line_y)], fill=(150,148,144), width=1)

    draw.text((cx - ew//2, e_y), "ETIQUETAS", font=f_e, fill=(150,148,144))

    img.save(OUT + "perfil-wordmark-stacked.jpg", "JPEG", quality=95)
    print("✓ perfil-wordmark-stacked.jpg")

concepto_wordmark()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO 3 — ETIQUETA REAL (forma de etiqueta bordada)
# Rectángulo con esquinas redondeadas simulando una etiqueta física
# "KORMAN" bordado en el centro, como si fuera la etiqueta misma
# Fondo blanco roto, borde negro
# ─────────────────────────────────────────────────────────────────────────────
def concepto_etiqueta_fisica():
    S = 1000
    img = Image.new("RGB", (S, S), (180, 178, 174))  # fondo gris neutro
    draw = ImageDraw.Draw(img)

    # Forma de etiqueta: rectángulo vertical redondeado
    tag_w, tag_h = 480, 680
    tx = (S - tag_w) // 2
    ty = (S - tag_h) // 2
    r = 28  # radio esquinas

    # Sombra sutil
    for offset in range(8, 0, -1):
        alpha_val = int(30 * offset / 8)
        draw.rounded_rectangle([tx+offset, ty+offset, tx+tag_w+offset, ty+tag_h+offset],
                                radius=r, fill=(60,60,60))

    # Etiqueta blanca rota
    draw.rounded_rectangle([tx, ty, tx+tag_w, ty+tag_h], radius=r, fill=(252,250,246))
    draw.rounded_rectangle([tx, ty, tx+tag_w, ty+tag_h], radius=r, outline=(8,8,8), width=3)

    # Agujero de la etiqueta arriba
    hole_r = 16
    hole_cx = S // 2
    hole_cy = ty + 44
    draw.ellipse([hole_cx-hole_r, hole_cy-hole_r, hole_cx+hole_r, hole_cy+hole_r],
                 fill=(180,178,174), outline=(8,8,8), width=2)

    # Línea de perforación
    draw.line([(tx+24, ty+88), (tx+tag_w-24, ty+88)], fill=(200,198,194), width=1)

    # KORMAN — grande en el centro
    f_main = fnt("BricolageGrotesque-Bold.ttf", 92)
    while tw(draw, "KORMAN", f_main) > tag_w - 48:
        f_main = fnt("BricolageGrotesque-Bold.ttf", f_main.size - 4)
    mw = tw(draw, "KORMAN", f_main)
    draw.text((S//2 - mw//2, ty + tag_h//2 - 80), "KORMAN", font=f_main, fill=(8,8,8))

    # ETIQUETAS — abajo más pequeño
    f_sub = fnt("Jura-Light.ttf", 36)
    sw = tw(draw, "ETIQUETAS", f_sub)
    draw.text((S//2 - sw//2, ty + tag_h//2 + 30), "ETIQUETAS", font=f_sub, fill=(110,108,104))

    # Línea decorativa
    lx = S//2
    draw.line([(lx - 60, ty + tag_h//2 + 16), (lx + 60, ty + tag_h//2 + 16)],
              fill=(180,178,174), width=1)

    # EST 1980 abajo
    f_est = fnt("Jura-Light.ttf", 24)
    ew = tw(draw, "EST. 1980", f_est)
    draw.text((S//2 - ew//2, ty + tag_h - 80), "EST. 1980", font=f_est, fill=(150,148,144))

    img.save(OUT + "perfil-etiqueta-fisica.jpg", "JPEG", quality=95)
    print("✓ perfil-etiqueta-fisica.jpg")

concepto_etiqueta_fisica()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO 4 — TIPOGRÁFICO PURO: solo "KORMAN" en el cuadrado
# Una sola palabra. Tamaño máximo. Como suprematismo gráfico.
# Fondo negro, blanco puro. Sin nada más.
# ─────────────────────────────────────────────────────────────────────────────
def concepto_suprematismo():
    S = 1000
    img = Image.new("RGB", (S, S), (8, 8, 8))
    draw = ImageDraw.Draw(img)

    f = fnt("BricolageGrotesque-Bold.ttf", 180)
    while tw(draw, "KORMAN", f) > S - 60:
        f = fnt("BricolageGrotesque-Bold.ttf", f.size - 4)

    w = tw(draw, "KORMAN", f)
    h = th(draw, "KORMAN", f)
    draw.text(((S-w)//2, (S-h)//2 - 40), "KORMAN", font=f, fill=(252,250,246))

    # Línea fina bajo KORMAN
    ly = (S+h)//2 - 20
    llen = w
    draw.line([((S-llen)//2, ly), ((S+llen)//2, ly)], fill=(110,108,104), width=1)

    # ETIQUETAS BORDADAS — pequeño, mismo ancho
    f2 = fnt("Jura-Light.ttf", 36)
    while tw(draw, "ETIQUETAS BORDADAS", f2) > w:
        f2 = fnt("Jura-Light.ttf", f2.size - 1)
    while tw(draw, "ETIQUETAS BORDADAS", f2) < w - 8:
        f2 = fnt("Jura-Light.ttf", f2.size + 1)
    w2 = tw(draw, "ETIQUETAS BORDADAS", f2)
    draw.text(((S-w2)//2, ly + 16), "ETIQUETAS BORDADAS", font=f2, fill=(110,108,104))

    img.save(OUT + "perfil-suprematismo.jpg", "JPEG", quality=95)
    print("✓ perfil-suprematismo.jpg")

concepto_suprematismo()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO 5 — CUADRÍCULA / GRID BORDADO
# "KE" en grid de puntos simulando la trama de bordado
# Técnico, textil, único
# ─────────────────────────────────────────────────────────────────────────────
def concepto_grid_bordado():
    S = 1000
    img = Image.new("RGB", (S, S), (8, 8, 8))
    draw = ImageDraw.Draw(img)

    # Grid de fondo (trama textil) — puntos muy sutiles
    step = 28
    for x in range(0, S, step):
        for y in range(0, S, step):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(28,26,24))

    # KORMAN grande en el centro
    f_main = fnt("BricolageGrotesque-Bold.ttf", 200)
    while tw(draw, "KORMAN", f_main) > S - 80:
        f_main = fnt("BricolageGrotesque-Bold.ttf", f_main.size - 4)
    mw = tw(draw, "KORMAN", f_main)
    mh = th(draw, "KORMAN", f_main)
    draw.text(((S-mw)//2, (S-mh)//2 - 50), "KORMAN", font=f_main, fill=(252,250,246))

    # Línea y texto
    ly = (S+mh)//2 - 30
    draw.line([((S-mw)//2, ly), ((S+mw)//2, ly)], fill=(110,108,104), width=1)

    f2 = fnt("Jura-Light.ttf", 38)
    while tw(draw, "ETIQUETAS  BORDADAS", f2) > mw:
        f2 = fnt("Jura-Light.ttf", f2.size - 1)
    w2 = tw(draw, "ETIQUETAS  BORDADAS", f2)
    draw.text(((S-w2)//2, ly + 14), "ETIQUETAS  BORDADAS", font=f2, fill=(110,108,104))

    img.save(OUT + "perfil-grid-bordado.jpg", "JPEG", quality=95)
    print("✓ perfil-grid-bordado.jpg")

concepto_grid_bordado()

print("\n✓ 5 conceptos nuevos listos")
