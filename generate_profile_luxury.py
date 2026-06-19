#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Profile photo luxury edition
Hilo de Oro philosophy — meticulous craft, textile soul, gold thread
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, os, random

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/"

def fnt(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def tw(draw, text, font):
    b = draw.textbbox((0,0), text, font=font)
    return b[2]-b[0]

def th(draw, text, font):
    b = draw.textbbox((0,0), text, font=font)
    return b[3]-b[1]

random.seed(42)

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO A — SELLO DE LACRE / GRAVADO EN METAL
# Fondo negro profundo con micropatrón de trama textil.
# "KORMAN" grabado con efecto de relieve dorado.
# Doble arco de texto con espaciado de lujo.
# ─────────────────────────────────────────────────────────────────────────────
def sello_metal():
    S = 1000
    # Base: negro profundo con noise sutil
    img = Image.new("RGB", (S, S), (6, 5, 4))
    draw = ImageDraw.Draw(img)

    # Micropatrón de fondo — trama de tejido (puntos en diagonal)
    for i in range(0, S, 8):
        for j in range(0, S, 8):
            if (i + j) % 16 == 0:
                draw.ellipse([i, j, i+1, j+1], fill=(18, 16, 12))

    # Círculos concéntricos decorativos (grabado en metal)
    cx, cy = S//2, S//2
    gold_dark  = (120, 96, 40)
    gold_mid   = (180, 148, 68)
    gold_light = (220, 190, 110)
    gold_shine = (245, 218, 150)

    for r, col, w in [
        (470, (30,28,22), 2),
        (460, gold_dark, 1),
        (452, (12,10,8), 3),
        (440, gold_mid, 1),
        (432, (12,10,8), 2),
        (210, gold_dark, 1),
        (200, (12,10,8), 2),
    ]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=col, width=w)

    # Rayos decorativos finos entre círculos (como sol/rosa)
    num_rays = 36
    r_inner = 218
    r_outer = 428
    for i in range(num_rays):
        angle = math.radians(i * 360 / num_rays)
        x1 = cx + r_inner * math.cos(angle)
        y1 = cy + r_inner * math.sin(angle)
        x2 = cx + r_outer * math.cos(angle)
        y2 = cy + r_outer * math.sin(angle)
        draw.line([(x1,y1),(x2,y2)], fill=(28,24,16), width=1)

    # Pequeños rombos en los radios principales (cada 45°)
    for i in range(8):
        angle = math.radians(i * 45)
        rm = (r_inner + r_outer) // 2
        x = cx + rm * math.cos(angle)
        y = cy + rm * math.sin(angle)
        sz = 5
        pts = [(x, y-sz),(x+sz,y),(x,y+sz),(x-sz,y)]
        draw.polygon(pts, fill=gold_mid)

    # KORMAN — efecto grabado dorado con sombra de profundidad
    f_main = fnt("BricolageGrotesque-Bold.ttf", 178)
    while tw(draw, "KORMAN", f_main) > 370:
        f_main = fnt("BricolageGrotesque-Bold.ttf", f_main.size - 4)
    mw = tw(draw, "KORMAN", f_main)
    mh = th(draw, "KORMAN", f_main)
    mx = cx - mw//2
    my = cy - mh//2 - 20

    # Sombra grabado (desplazamiento negativo = profundidad)
    draw.text((mx+2, my+2), "KORMAN", font=f_main, fill=(2,2,1))
    draw.text((mx-1, my-1), "KORMAN", font=f_main, fill=(50,40,18))
    # Color principal dorado
    draw.text((mx, my), "KORMAN", font=f_main, fill=gold_light)
    # Brillo sutil (línea 1px más arriba, más claro)
    draw.text((mx, my-1), "KORMAN", font=f_main, fill=gold_shine)

    # Línea dorada bajo KORMAN
    line_y = my + mh + 16
    draw.line([(cx-110, line_y), (cx+110, line_y)], fill=gold_mid, width=1)

    # ETIQUETAS — Italiana (serif elegante) con efecto dorado
    f_sub = fnt("Italiana-Regular.ttf", 46)
    sw = tw(draw, "ETIQUETAS", f_sub)
    sx = cx - sw//2
    sy = line_y + 14
    draw.text((sx+1, sy+1), "ETIQUETAS", font=f_sub, fill=(2,2,1))
    draw.text((sx, sy), "ETIQUETAS", font=f_sub, fill=gold_mid)

    # Texto en arco superior — BORDADAS · EST. 1980 en arco
    f_arc = fnt("Jura-Light.ttf", 22)
    arc_text = "B O R D A D A S   ·   E S T.  1 9 8 0"
    r_arc = 310
    total_deg = 110
    start_deg = -90 - total_deg/2
    chars = list(arc_text)
    if len(chars) > 1:
        step = total_deg / (len(chars)-1)
        for i, ch in enumerate(chars):
            a_deg = start_deg + i * step
            a_rad = math.radians(a_deg)
            x = cx + r_arc * math.cos(a_rad)
            y = cy + r_arc * math.sin(a_rad)
            cw = tw(draw, ch, f_arc)
            ch_img = Image.new("RGBA", (50,50), (0,0,0,0))
            cd = ImageDraw.Draw(ch_img)
            cd.text((25-cw//2, 4), ch, font=f_arc, fill=(*gold_dark, 255))
            rot = ch_img.rotate(-(a_deg+90), expand=False, resample=Image.BICUBIC)
            img.paste(rot, (int(x)-25, int(y)-25), rot)

    # Pequeños triángulos decorativos arriba/abajo del arco
    for angle_deg, flip in [(-90-total_deg/2-4, False), (-90+total_deg/2+4, False)]:
        a = math.radians(angle_deg)
        x = cx + r_arc * math.cos(a)
        y = cy + r_arc * math.sin(a)
        draw.ellipse([x-2,y-2,x+2,y+2], fill=gold_dark)

    img.save(OUT + "perfil-sello-metal.jpg", "JPEG", quality=97)
    print("✓ perfil-sello-metal.jpg")

sello_metal()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO B — LACRE / CERA DE SELLO (wax seal)
# Forma circular irregular como lacre real.
# Textura rugosa pintada a mano.
# Iniciales KE grabadas en el centro.
# ─────────────────────────────────────────────────────────────────────────────
def lacre_seal():
    S = 1000
    img = Image.new("RGB", (S, S), (252, 250, 246))
    draw = ImageDraw.Draw(img)

    cx, cy = S//2, S//2
    r = 390

    # Base lacre: rojo oscuro profundo con variaciones
    lacre_dark = (60, 12, 10)
    lacre_mid  = (90, 20, 16)
    lacre_base = (110, 28, 22)
    lacre_hi   = (140, 42, 32)

    # Forma irregular de lacre (no círculo perfecto)
    # Usamos polígono con puntos levemente irregulares
    num_pts = 72
    pts = []
    for i in range(num_pts):
        angle = math.radians(i * 360 / num_pts)
        # Pequeñas variaciones de radio para textura orgánica
        variation = random.uniform(-14, 14)
        ri = r + variation
        x = cx + ri * math.cos(angle)
        y = cy + ri * math.sin(angle)
        pts.append((x, y))
    draw.polygon(pts, fill=lacre_base)

    # Capas de color para textura de cera
    for _ in range(120):
        angle = random.uniform(0, 2*math.pi)
        dist = random.uniform(0, r*0.92)
        x = cx + dist*math.cos(angle)
        y = cy + dist*math.sin(angle)
        size = random.randint(4, 28)
        alpha_col = random.choice([lacre_dark, lacre_mid, lacre_hi])
        draw.ellipse([x-size, y-size, x+size, y+size], fill=alpha_col)

    # Borde exterior del lacre — más oscuro
    draw.polygon(pts, outline=lacre_dark, width=4)

    # Círculo interior grabado (huella del sello)
    r_inner = 280
    draw.ellipse([cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner],
                 outline=(45,8,6), width=3)
    r_inner2 = 260
    draw.ellipse([cx-r_inner2, cy-r_inner2, cx+r_inner2, cy+r_inner2],
                 outline=(45,8,6), width=1)

    # KE monograma grabado (blanco/marfil como relieve)
    ivory = (240, 228, 200)
    ivory_dark = (200, 185, 155)

    f_k = fnt("BricolageGrotesque-Bold.ttf", 220)
    f_e = fnt("Italiana-Regular.ttf", 120)

    # "K" izquierda
    kw = tw(draw, "K", f_k)
    kh = th(draw, "K", f_k)
    draw.text((cx - kw + 10, cy - kh//2 - 10), "K", font=f_k, fill=ivory_dark)
    draw.text((cx - kw + 9, cy - kh//2 - 11), "K", font=f_k, fill=ivory)

    # "E" derecha sobrepuesta
    ew = tw(draw, "E", f_e)
    draw.text((cx - 10, cy - kh//2 + 40), "E", font=f_e, fill=ivory_dark)
    draw.text((cx - 11, cy - kh//2 + 39), "E", font=f_e, fill=ivory)

    # Texto circular dentro del sello
    f_arc = fnt("Jura-Light.ttf", 20)
    arc_text = "KORMAN  ·  ETIQUETAS  ·  BORDADAS  ·"
    r_arc = 238
    chars = list(arc_text)
    step = 360 / len(chars)
    for i, ch in enumerate(chars):
        a_deg = -90 + i * step
        a_rad = math.radians(a_deg)
        x = cx + r_arc * math.cos(a_rad)
        y = cy + r_arc * math.sin(a_rad)
        cw = tw(draw, ch, f_arc)
        ch_img = Image.new("RGBA", (40,40), (0,0,0,0))
        cd = ImageDraw.Draw(ch_img)
        cd.text((20-cw//2, 4), ch, font=f_arc, fill=(*ivory_dark, 220))
        rot = ch_img.rotate(-(a_deg+90), expand=False, resample=Image.BICUBIC)
        img.paste(rot, (int(x)-20, int(y)-20), rot)

    img.save(OUT + "perfil-lacre.jpg", "JPEG", quality=97)
    print("✓ perfil-lacre.jpg")

lacre_seal()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO C — TEJIDO / ENTRAMADO TIPOGRÁFICO
# Fondo de arpillera/lino digital (lines cruzadas)
# KORMAN en serif grande, elegante, con tracking amplio
# Borde como etiqueta cosida — puntadas visibles
# ─────────────────────────────────────────────────────────────────────────────
def tejido_tipografico():
    S = 1000
    # Fondo lino oscuro
    lino = (28, 24, 18)
    img = Image.new("RGB", (S, S), lino)
    draw = ImageDraw.Draw(img)

    # Trama de lino — líneas horizontales y verticales muy finas
    for y in range(0, S, 6):
        col = (35, 30, 22) if (y//6) % 2 == 0 else (22, 18, 12)
        draw.line([(0,y),(S,y)], fill=col, width=1)
    for x in range(0, S, 6):
        col = (32, 28, 20) if (x//6) % 2 == 0 else (20, 16, 10)
        draw.line([(x,0),(x,S)], fill=col, width=1)

    # Borde de puntadas (dash line) — simula etiqueta cosida
    cx, cy = S//2, S//2
    margin = 60
    dash_col = (160, 140, 90)
    dash_len = 14
    gap_len  = 8
    # Puntadas top
    x = margin + dash_len
    while x < S - margin - dash_len:
        draw.line([(x, margin), (x+dash_len, margin)], fill=dash_col, width=2)
        x += dash_len + gap_len
    # Puntadas bottom
    x = margin + dash_len
    while x < S - margin - dash_len:
        draw.line([(x, S-margin), (x+dash_len, S-margin)], fill=dash_col, width=2)
        x += dash_len + gap_len
    # Puntadas left
    y = margin + dash_len
    while y < S - margin - dash_len:
        draw.line([(margin, y), (margin, y+dash_len)], fill=dash_col, width=2)
        y += dash_len + gap_len
    # Puntadas right
    y = margin + dash_len
    while y < S - margin - dash_len:
        draw.line([(S-margin, y), (S-margin, y+dash_len)], fill=dash_col, width=2)
        y += dash_len + gap_len

    # Bordes interiores más sutiles
    inner = 80
    draw.rectangle([inner, inner, S-inner, S-inner], outline=(45,38,28), width=1)

    gold = (200, 168, 88)
    cream = (240, 232, 210)
    gray_warm = (140, 132, 108)

    # KORMAN — serif grande (YoungSerif) con tracking manual
    f_main = fnt("YoungSerif-Regular.ttf", 140)
    while tw(draw, "KORMAN", f_main) > S - 220:
        f_main = fnt("YoungSerif-Regular.ttf", f_main.size - 4)

    mw = tw(draw, "KORMAN", f_main)
    mh = th(draw, "KORMAN", f_main)
    mx = cx - mw//2
    my = cy - mh//2 - 50

    # Sombra cálida
    draw.text((mx+3, my+3), "KORMAN", font=f_main, fill=(10,8,4))
    draw.text((mx, my), "KORMAN", font=f_main, fill=cream)

    # Línea dorada — mismo ancho que KORMAN
    line_y = my + mh + 24
    draw.line([(mx, line_y), (mx+mw, line_y)], fill=gold, width=1)

    # ETIQUETAS — Jura Light espaciado
    f_sub = fnt("Jura-Light.ttf", 42)
    # Expandir tracking manualmente
    sub_text = "E T I Q U E T A S"
    sw = tw(draw, sub_text, f_sub)
    sx = cx - sw//2
    sy = line_y + 22
    draw.text((sx, sy), sub_text, font=f_sub, fill=gold)

    # EST. 1980 abajo pequeño
    f_est = fnt("Jura-Light.ttf", 24)
    ew = tw(draw, "B O R D A D A S  ·  E S T.  1 9 8 0", f_est)
    draw.text((cx - ew//2, sy + 68), "B O R D A D A S  ·  E S T.  1 9 8 0",
              font=f_est, fill=gray_warm)

    # Pequeños ornamentos de esquina (cruces bordadas)
    def cruz(x, y, col):
        draw.line([(x-10, y),(x+10, y)], fill=col, width=1)
        draw.line([(x, y-10),(x, y+10)], fill=col, width=1)
        draw.ellipse([x-2,y-2,x+2,y+2], fill=col)

    for px, py in [(inner+30, inner+30),(S-inner-30, inner+30),
                   (inner+30, S-inner-30),(S-inner-30, S-inner-30)]:
        cruz(px, py, gold)

    img.save(OUT + "perfil-tejido.jpg", "JPEG", quality=97)
    print("✓ perfil-tejido.jpg")

tejido_tipografico()

# ─────────────────────────────────────────────────────────────────────────────
# CONCEPTO D — MEDALLÓN DE ALTA COSTURA
# Fondo oscuro. Medallón oval con textura de satén.
# KORMAN en serif cursiva (InstrumentSerif Italic) — elegancia femenina.
# Detalles en dorado fino.
# ─────────────────────────────────────────────────────────────────────────────
def medallon_couture():
    S = 1000
    bg = (10, 9, 8)
    img = Image.new("RGB", (S, S), bg)
    draw = ImageDraw.Draw(img)

    cx, cy = S//2, S//2
    gold       = (190, 158, 72)
    gold_light = (230, 200, 120)
    gold_dark  = (100, 80, 30)
    cream      = (245, 238, 218)

    # Patrón de fondo — microcheck muy oscuro
    for y in range(0, S, 4):
        for x in range(0, S, 4):
            if (x//4 + y//4) % 2 == 0:
                draw.rectangle([x, y, x+3, y+3], fill=(14,13,11))

    # Medallón oval principal
    ow, oh = 820, 820
    ox, oy = cx - ow//2, cy - oh//2

    # Efecto satén — gradiente simulado con capas
    for i in range(40):
        factor = i / 40
        r_col = int(22 + factor * 8)
        ow_i = ow - i*2
        oh_i = oh - i*2
        draw.ellipse([cx-ow_i//2, cy-oh_i//2, cx+ow_i//2, cy+oh_i//2],
                     outline=(r_col, r_col-2, r_col-4), width=1)

    # Anillos decorativos dorados
    for r, w, col in [(410, 2, gold_dark), (402, 1, gold), (392, 1, gold_dark),
                      (200, 1, gold_dark), (192, 1, (50,40,15))]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=col, width=w)

    # Cruces y puntos en los 4 ejes del medallón (estilo haute couture)
    for angle_deg in [0, 90, 180, 270]:
        a = math.radians(angle_deg)
        x = cx + 396 * math.cos(a)
        y = cy + 396 * math.sin(a)
        draw.ellipse([x-4,y-4,x+4,y+4], fill=gold)
        for d in [-10, 10]:
            if angle_deg in [0, 180]:
                draw.line([(x, y+d-3),(x, y+d+3)], fill=gold_dark, width=1)
            else:
                draw.line([(x+d-3, y),(x+d+3, y)], fill=gold_dark, width=1)

    # KORMAN — serif cursiva elegante
    f_main = fnt("InstrumentSerif-Italic.ttf", 168)
    while tw(draw, "Korman", f_main) > 680:
        f_main = fnt("InstrumentSerif-Italic.ttf", f_main.size - 4)
    mw = tw(draw, "Korman", f_main)
    mh = th(draw, "Korman", f_main)
    mx = cx - mw//2
    my = cy - mh//2 - 30

    # Sombra dorada
    draw.text((mx+3, my+3), "Korman", font=f_main, fill=(40,30,8))
    draw.text((mx, my), "Korman", font=f_main, fill=cream)

    # Ornamento dorado bajo el nombre
    line_y = my + mh + 18
    llen = mw - 20
    draw.line([(cx-llen//2, line_y), (cx+llen//2, line_y)], fill=gold, width=1)
    # Punto central en la línea
    draw.ellipse([cx-3, line_y-3, cx+3, line_y+3], fill=gold_light)

    # ETIQUETAS — Jura Light dorado
    f_et = fnt("Jura-Light.ttf", 34)
    et_text = "E T I Q U E T A S   B O R D A D A S"
    ew = tw(draw, et_text, f_et)
    draw.text((cx-ew//2, line_y + 18), et_text, font=f_et, fill=gold)

    # Texto EST 1980 muy pequeño abajo
    f_sm = fnt("Jura-Light.ttf", 20)
    sm = "— EST. 1980 —"
    smw = tw(draw, sm, f_sm)
    draw.text((cx-smw//2, line_y + 64), sm, font=f_sm, fill=gold_dark)

    img.save(OUT + "perfil-medallon.jpg", "JPEG", quality=97)
    print("✓ perfil-medallon.jpg")

medallon_couture()

print("\n✓ 4 conceptos luxury listos")
