#!/usr/bin/env python3
"""KORMAN — 4 logos innovadores de alta elegancia."""
from PIL import Image, ImageDraw, ImageFont
import math, os
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/pruebas-innovadoras/"
os.makedirs(OUT, exist_ok=True)

S = 1000
BG    = (252, 250, 247)
BLACK = (18,  15,  15 )
BORDO = (124, 38,  50 )
SIL   = (176, 182, 190)
SIL_LT= (220, 224, 230)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()

def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2] - b[0]
def th(d, t, f):
    b = d.textbbox((0,0), t, f); return b[3] - b[1]
def cx_text(d, t, f, cx):
    return cx - tw(d, t, f) // 2

# ─────────────────────────────────────────────────────────────────
# 1 · SELLO EDITORIAL
# ─────────────────────────────────────────────────────────────────
def sello_editorial():
    img = Image.new("RGB", (S, S), BG)
    d   = ImageDraw.Draw(img)
    cx = cy = S // 2

    # Anillo exterior negro (grueso)
    R1 = 400
    d.ellipse([cx-R1, cy-R1, cx+R1, cy+R1], outline=BLACK, width=2)
    # Anillo bordo fino interior
    R2 = 372
    d.ellipse([cx-R2, cy-R2, cx+R2, cy+R2], outline=BORDO, width=1)
    # Anillo negro fino más interior
    R3 = 350
    d.ellipse([cx-R3, cy-R3, cx+R3, cy+R3], outline=BLACK, width=1)

    # Texto circular: "KORMAN ETIQUETAS · BUENOS AIRES · EST. 1980 ·"
    texto = "KORMAN ETIQUETAS  ·  BUENOS AIRES  ·  EST. 1980  ·  "
    f_circ = fnt("Jura-Light.ttf", 20)
    radio_txt = 386
    total_chars = len(texto)
    # distribuir uniformemente
    angulo_total = 2 * math.pi
    step = angulo_total / total_chars
    start = -math.pi / 2
    for i, ch in enumerate(texto):
        ang = start + i * step
        # posicion del caracter
        x = cx + radio_txt * math.cos(ang)
        y = cy + radio_txt * math.sin(ang)
        # rotar imagen de caracter
        char_img = Image.new("RGBA", (30, 30), (0,0,0,0))
        cd = ImageDraw.Draw(char_img)
        cw = cd.textbbox((0,0), ch, font=f_circ)
        cd.text((15 - (cw[2]-cw[0])//2, 15 - (cw[3]-cw[1])//2), ch, font=f_circ, fill=BLACK)
        rotated = char_img.rotate(-math.degrees(ang) - 90, expand=False)
        img.paste(rotated, (int(x)-15, int(y)-15), rotated)

    # K grande Gloock
    f_k = fnt("Gloock-Regular.ttf", 480)
    while tw(d, "K", f_k) > 520: f_k = fnt("Gloock-Regular.ttf", f_k.size - 6)
    kw = tw(d, "K", f_k); kh = th(d, "K", f_k)
    d.text((cx - kw//2, cy - kh//2 - 20), "K", font=f_k, fill=BLACK)

    # Pequeña línea bordo horizontal debajo de la K
    d.line([(cx-60, cy+kh//2-40), (cx+60, cy+kh//2-40)], fill=BORDO, width=1)

    img.save(OUT + "1-sello-editorial.png", "PNG", dpi=(300,300))
    print("✓  1-sello-editorial.png")


# ─────────────────────────────────────────────────────────────────
# 2 · GEOMETRÍA TEXTIL
# ─────────────────────────────────────────────────────────────────
def geometria_textil():
    img = Image.new("RGB", (S, S), BG)
    d   = ImageDraw.Draw(img)
    cx = cy = S // 2
    half = 310   # lado del rombo / 2

    # Líneas de extensión (hilo) desde cada vértice, finas bordo
    ext = 130
    d.line([(cx, cy - half - ext), (cx, cy - half)], fill=BORDO, width=1)
    d.line([(cx, cy + half), (cx, cy + half + ext)], fill=BORDO, width=1)
    d.line([(cx - half - ext, cy), (cx - half, cy)], fill=BORDO, width=1)
    d.line([(cx + half, cy), (cx + half + ext, cy)], fill=BORDO, width=1)
    # Pequeños remates en los extremos
    r_tip = 4
    for px, py in [(cx, cy-half-ext), (cx, cy+half+ext), (cx-half-ext, cy), (cx+half+ext, cy)]:
        d.ellipse([px-r_tip, py-r_tip, px+r_tip, py+r_tip], fill=BORDO)

    # Rombo exterior negro
    diamond = [(cx, cy-half), (cx+half, cy), (cx, cy+half), (cx-half, cy)]
    d.polygon(diamond, outline=BLACK, width=2)

    # Rombo interior fino bordo
    h2 = half - 22
    diamond2 = [(cx, cy-h2), (cx+h2, cy), (cx, cy+h2), (cx-h2, cy)]
    d.polygon(diamond2, outline=BORDO, width=1)

    # Líneas cruzadas internas (trama textil) — muy finas
    for off in range(-h2+40, h2, 30):
        # diagonal ↘
        d.line([(cx+off, cy-h2+abs(off)), (cx+off, cy+h2-abs(off))], fill=(220,218,214), width=1)

    # K serif en Italiana dentro del rombo
    f_k = fnt("Italiana-Regular.ttf", 400)
    while tw(d, "K", f_k) > half * 1.1: f_k = fnt("Italiana-Regular.ttf", f_k.size - 6)
    kw = tw(d, "K", f_k); kh = th(d, "K", f_k)
    d.text((cx - kw//2, cy - kh//2 - 30), "K", font=f_k, fill=BLACK)

    img.save(OUT + "2-geometria-textil.png", "PNG", dpi=(300,300))
    print("✓  2-geometria-textil.png")


# ─────────────────────────────────────────────────────────────────
# 3 · AGUJA INTEGRADA
# ─────────────────────────────────────────────────────────────────
def aguja_integrada():
    img = Image.new("RGB", (S, S), BG)
    d   = ImageDraw.Draw(img)
    cx = cy = S // 2

    # Circulo muy fino
    R = 370
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=BLACK, width=1)

    # K en Italiana — grande
    f_k = fnt("Italiana-Regular.ttf", 520)
    while tw(d, "K", f_k) > 520: f_k = fnt("Italiana-Regular.ttf", f_k.size - 6)
    kw = tw(d, "K", f_k); kh = th(d, "K", f_k)
    kx = cx - kw//2
    ky = cy - kh//2 - 20
    d.text((kx, ky), "K", font=f_k, fill=BLACK)

    # Aguja plateada elegante ocupando el brazo diagonal de la K
    # El brazo diagonal de la K va aprox de (kx+kw*0.52, ky+kh*0.46) a (kx+kw*0.95, ky+kh*0.92)
    # Calculamos los puntos
    ax1 = kx + kw * 0.50
    ay1 = ky + kh * 0.44
    ax2 = kx + kw * 0.97
    ay2 = ky + kh * 0.93
    ang  = math.atan2(ay2 - ay1, ax2 - ax1)
    length = math.hypot(ax2 - ax1, ay2 - ay1) * 1.3
    mcx  = (ax1 + ax2) / 2
    mcy  = (ay1 + ay2) / 2
    # Extender la aguja
    ex1x = mcx - length/2 * math.cos(ang)
    ex1y = mcy - length/2 * math.sin(ang)
    ex2x = mcx + length/2 * math.cos(ang)
    ex2y = mcy + length/2 * math.sin(ang)
    perp = ang + math.pi/2
    hw = 5   # aguja fina
    taper = 0.88
    tx = ex1x + (ex2x - ex1x) * taper
    ty = ex1y + (ex2y - ex1y) * taper
    # Cuerpo aguja
    body = [
        (ex1x + hw*math.cos(perp), ex1y + hw*math.sin(perp)),
        (tx   + hw*math.cos(perp), ty   + hw*math.sin(perp)),
        (ex2x, ex2y),
        (tx   - hw*math.cos(perp), ty   - hw*math.sin(perp)),
        (ex1x - hw*math.cos(perp), ex1y - hw*math.sin(perp)),
    ]
    d.polygon(body, fill=SIL)
    # Highlight
    d.line([(ex1x, ex1y), (ex2x, ex2y)], fill=SIL_LT, width=1)
    # Cabeza de aguja
    d.ellipse([ex1x-hw-1, ex1y-hw-1, ex1x+hw+1, ex1y+hw+1], fill=(90,94,100))
    d.ellipse([ex1x-hw+1, ex1y-hw+1, ex1x+hw-1, ex1y+hw-1], fill=SIL)
    # Ojo de aguja
    eye_img = Image.new("RGBA", (40,40), (0,0,0,0))
    ed = ImageDraw.Draw(eye_img)
    ed.ellipse([20-3, 20-10, 20+3, 20+10], outline=BLACK, width=2)
    eye_rot = eye_img.rotate(-math.degrees(ang), expand=False)
    ecx = ex1x + 40 * math.cos(ang)
    ecy = ex1y + 40 * math.sin(ang)
    img.paste(eye_rot, (int(ecx)-20, int(ecy)-20), eye_rot)

    # Texto pequeño bajo el círculo
    f_sub = fnt("Jura-Light.ttf", 18)
    sub = "KORMAN ETIQUETAS"
    d.text((cx - tw(d, sub, f_sub)//2, cy + R + 18), sub, font=f_sub, fill=BORDO)

    img.save(OUT + "3-aguja-integrada.png", "PNG", dpi=(300,300))
    print("✓  3-aguja-integrada.png")


# ─────────────────────────────────────────────────────────────────
# 4 · ESCUDO MODERNO
# ─────────────────────────────────────────────────────────────────
def escudo_moderno():
    img = Image.new("RGB", (S, S), BG)
    d   = ImageDraw.Draw(img)
    cx = cy = S // 2

    # Escudo — contorno puro, sin relleno
    # Forma: rectángulo superior con punta inferior redondeada
    sw = 280   # semi-ancho
    sh = 360   # semi-alto desde centro
    top    = cy - sh
    bot_y  = cy + sh
    left   = cx - sw
    right  = cx + sw

    # Trazamos el escudo con polyline — punta en la base
    shield = [
        (left,  top + 40),      # esquina sup-izq con radio
        (left,  top),
        (right, top),
        (right, top + 40),
        (right, bot_y - 140),   # curva hacia la punta
        (cx,    bot_y),         # punta
        (left,  bot_y - 140),
        (left,  top + 40),
    ]
    # Dos trazos: negro fino exterior, bordo muy fino interior (offset)
    d.polygon(shield, outline=BLACK, width=2)
    # Escudo interior bordo (offset de 14px)
    off = 18
    shield_in = [
        (left+off,  top+off+40),
        (left+off,  top+off),
        (right-off, top+off),
        (right-off, top+off+40),
        (right-off, bot_y-off-130),
        (cx,        bot_y-off*2),
        (left+off,  bot_y-off-130),
        (left+off,  top+off+40),
    ]
    d.polygon(shield_in, outline=BORDO, width=1)

    # Línea horizontal fina bordo cruzando el escudo en el tercio superior
    rule_y = top + (bot_y - top) * 0.38
    d.line([(left+4, rule_y), (right-4, rule_y)], fill=BORDO, width=1)

    # K bold arriba del corte
    f_k = fnt("BricolageGrotesque-Bold.ttf", 300)
    while tw(d, "K", f_k) > sw * 1.4: f_k = fnt("BricolageGrotesque-Bold.ttf", f_k.size - 6)
    kw = tw(d, "K", f_k); kh = th(d, "K", f_k)
    k_center_y = top + (rule_y - top) / 2
    d.text((cx - kw//2, k_center_y - kh//2), "K", font=f_k, fill=BLACK)

    # "1980" pequeño bajo la línea bordo
    f_year = fnt("Jura-Light.ttf", 22)
    year = "EST. 1980"
    d.text((cx - tw(d, year, f_year)//2, rule_y + 14), year, font=f_year, fill=BORDO)

    # "KORMAN ETIQUETAS" muy pequeño bajo la punta del escudo
    f_sub = fnt("Jura-Light.ttf", 16)
    sub = "KORMAN  ETIQUETAS"
    d.text((cx - tw(d, sub, f_sub)//2, bot_y + 22), sub, font=f_sub, fill=BLACK)

    img.save(OUT + "4-escudo-moderno.png", "PNG", dpi=(300,300))
    print("✓  4-escudo-moderno.png")


sello_editorial()
geometria_textil()
aguja_integrada()
escudo_moderno()
print("\n✓ 4 logos listos en assets/pruebas-innovadoras/")
