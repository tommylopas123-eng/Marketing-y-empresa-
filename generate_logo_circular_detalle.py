#!/usr/bin/env python3
"""KORMAN — sellos circulares con DETALLE: guilloche, perlado, hilo/aguja, oro+bordo."""
from PIL import Image, ImageDraw, ImageFont
import math, os
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/pruebas-circular/"
os.makedirs(OUT, exist_ok=True)

S = 1200
BG     = (252, 250, 247)
BLACK  = (18,  15,  15 )
BORDO  = (124, 38,  50 )
BORDO_D= (92,  26,  36 )
GOLD   = (176, 138, 58 )
GOLD_LT= (206, 172, 96 )
SIL    = (176, 182, 190)
SIL_LT = (224, 228, 234)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]
def th(d, t, f):
    b = d.textbbox((0,0), t, f); return b[3]-b[1]

# ── Roseta guilloche (hipotrocoide) ─────────────────────────────────
def guilloche(d, cx, cy, R, petals, amp, color, width=1, phase=0):
    pts = []
    steps = 1440
    for i in range(steps + 1):
        th_ = 2 * math.pi * i / steps
        r = R + amp * math.cos(petals * th_ + phase)
        pts.append((cx + r * math.cos(th_), cy + r * math.sin(th_)))
    d.line(pts, fill=color, width=width, joint="curve")

# ── Anillo perlado (beads) ──────────────────────────────────────────
def perlado(d, cx, cy, R, n, rad, color):
    for i in range(n):
        a = 2 * math.pi * i / n
        x = cx + R * math.cos(a); y = cy + R * math.sin(a)
        d.ellipse([x-rad, y-rad, x+rad, y+rad], fill=color)

# ── Texto en arco ───────────────────────────────────────────────────
def texto_arco(img, cx, cy, R, texto, font, color, arc_center_deg, total_deg, flip=False):
    n = len(texto)
    if n == 0: return
    if flip:
        texto = texto[::-1]          # invertir para que se lea bien en el arco inferior
    start = arc_center_deg - total_deg/2
    step  = total_deg / (n - 1) if n > 1 else 0
    d0 = ImageDraw.Draw(img)
    for i, ch in enumerate(texto):
        deg = start + i * step
        a = math.radians(deg)
        x = cx + R * math.cos(a); y = cy + R * math.sin(a)
        size = 64
        ci = Image.new("RGBA", (size, size), (0,0,0,0))
        cd = ImageDraw.Draw(ci)
        bb = cd.textbbox((0,0), ch, font=font)
        cw, chh = bb[2]-bb[0], bb[3]-bb[1]
        cd.text((size//2 - cw//2 - bb[0], size//2 - chh//2 - bb[1]), ch, font=font, fill=color)
        rot = (-deg - 90) if not flip else (-deg + 90)
        ci = ci.rotate(rot, expand=False, resample=Image.BICUBIC)
        img.paste(ci, (int(x)-size//2, int(y)-size//2), ci)

# ── Aguja fina con hilo ─────────────────────────────────────────────
def aguja(d, cx, cy, ang, length, hw=5):
    ax1 = cx - length/2*math.cos(ang); ay1 = cy - length/2*math.sin(ang)
    ax2 = cx + length/2*math.cos(ang); ay2 = cy + length/2*math.sin(ang)
    perp = ang + math.pi/2; taper = 0.9
    tx = ax1 + (ax2-ax1)*taper; ty = ay1 + (ay2-ay1)*taper
    d.polygon([(ax1+hw*math.cos(perp), ay1+hw*math.sin(perp)),
               (tx+hw*math.cos(perp),  ty+hw*math.sin(perp)),
               (ax2, ay2),
               (tx-hw*math.cos(perp),  ty-hw*math.sin(perp)),
               (ax1-hw*math.cos(perp), ay1-hw*math.sin(perp))], fill=SIL)
    d.line([(ax1, ay1), (ax2, ay2)], fill=SIL_LT, width=1)
    d.ellipse([ax1-hw-1, ay1-hw-1, ax1+hw+1, ay1+hw+1], fill=(90,94,100))
    d.ellipse([ax1-hw+1, ay1-hw+1, ax1+hw-1, ay1+hw-1], fill=SIL)
    return ax1, ay1

def estrella(d, cx, cy, r, color):
    pts = []
    for i in range(8):
        a = math.pi/2 + i*math.pi/4
        rr = r if i % 2 == 0 else r*0.42
        pts.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    d.polygon(pts, fill=color)

# ════════════════════════════════════════════════════════════════════
# 1 · SELLO GUILLOCHÉ
# ════════════════════════════════════════════════════════════════════
def sello_guilloche():
    img = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(img)
    cx = cy = S//2
    d.ellipse([cx-460, cy-460, cx+460, cy+460], outline=BLACK, width=3)
    perlado(d, cx, cy, 440, 120, 2.4, BLACK)
    d.ellipse([cx-420, cy-420, cx+420, cy+420], outline=BORDO, width=1)
    # banda de texto
    texto_arco(img, cx, cy, 392, "KORMAN  ETIQUETAS  BORDADAS", fnt("Jura-Medium.ttf", 34), BLACK, -90, 200)
    texto_arco(img, cx, cy, 392, "BUENOS AIRES", fnt("Jura-Medium.ttf", 30), BORDO, 90, 70, flip=True)
    d = ImageDraw.Draw(img)
    estrella(d, cx-300, cy+ -0, 12, BORDO)
    estrella(d, cx+300, cy+ 0, 12, BORDO)
    # roseta guilloche doble
    guilloche(d, cx, cy, 320, 36, 16, GOLD, 1)
    guilloche(d, cx, cy, 300, 36, 14, BORDO, 1, phase=math.pi/36)
    guilloche(d, cx, cy, 270, 24, 12, GOLD_LT, 1)
    d.ellipse([cx-250, cy-250, cx+250, cy+250], outline=BLACK, width=2)
    d.ellipse([cx-244, cy-244, cx+244, cy+244], outline=GOLD, width=1)
    # K central Gloock
    f_k = fnt("Gloock-Regular.ttf", 360)
    while tw(d,"K",f_k) > 300: f_k = fnt("Gloock-Regular.ttf", f_k.size-6)
    kw, kh = tw(d,"K",f_k), th(d,"K",f_k)
    d.text((cx-kw//2, cy-kh//2-58), "K", font=f_k, fill=BLACK)
    # aguja cruzando bajo la K
    aguja(d, cx, cy+96, math.radians(-22), 300, hw=5)
    # EST 1980
    f_y = fnt("Jura-Medium.ttf", 26)
    d.text((cx-tw(d,"EST. 1980",f_y)//2, cy+150), "EST. 1980", font=f_y, fill=BORDO)
    img.save(OUT+"1-sello-guilloche.png", "PNG", dpi=(300,300)); print("✓ 1-sello-guilloche.png")

# ════════════════════════════════════════════════════════════════════
# 2 · SELLO LAUREL TEXTIL
# ════════════════════════════════════════════════════════════════════
def hoja(d, x, y, ang, ln, color):
    ex = x + ln*math.cos(ang); ey = y + ln*math.sin(ang)
    perp = ang + math.pi/2
    midx, midy = (x+ex)/2, (y+ey)/2
    w = ln*0.32
    d.polygon([(x,y),(midx+w*math.cos(perp), midy+w*math.sin(perp)),(ex,ey),
               (midx-w*math.cos(perp), midy-w*math.sin(perp))], fill=color)

def sello_laurel():
    img = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(img)
    cx = cy = S//2
    d.ellipse([cx-460, cy-460, cx+460, cy+460], outline=BLACK, width=4)
    d.ellipse([cx-446, cy-446, cx+446, cy+446], outline=BORDO, width=1)
    perlado(d, cx, cy, 410, 90, 3, BORDO)
    texto_arco(img, cx, cy, 392, "KORMAN ETIQUETAS BORDADAS", fnt("CrimsonPro-Bold.ttf", 40), BLACK, -90, 190)
    texto_arco(img, cx, cy, 392, "46 AÑOS DE OFICIO", fnt("CrimsonPro-Bold.ttf", 34), BORDO, 90, 90, flip=True)
    d = ImageDraw.Draw(img)
    # laureles a los lados
    for side in (-1, 1):
        base_a = math.radians(180) if side==-1 else math.radians(0)
        for k in range(7):
            t = k/6.0
            a = math.radians(150*side*-1) # placeholder
        # dibujar ramas curvas
    # ramas de laurel manual (dos arcos)
    for side in (-1, 1):
        for k in range(8):
            ang0 = math.radians(200 if side==-1 else -20)
            spread = math.radians(58)
            a = ang0 + side*(-1)*0  # not used
            frac = k/7.0
            theta = math.radians((205 if side==-1 else 25) - side*0)
        pass
    # laurel simple: puntos sobre un arco
    for side in (-1, 1):
        cxr = cx
        for k in range(9):
            ang_deg = (200 + k*8) if side==1 else (340 - k*8)
            a = math.radians(ang_deg)
            bx = cx + 330*math.cos(a); by = cy + 330*math.sin(a)
            leaf_ang = a + math.radians(90*side)
            hoja(d, bx, by, leaf_ang, 46, BORDO if k%2 else BORDO_D)
    # anillo interior
    d.ellipse([cx-250, cy-250, cx+250, cy+250], outline=BLACK, width=3)
    d.ellipse([cx-238, cy-238, cx+238, cy+238], outline=GOLD, width=1)
    guilloche(d, cx, cy, 250, 48, 8, (228,224,220), 1)
    # K Italiana
    f_k = fnt("Gloock-Regular.ttf", 330)
    while tw(d,"K",f_k) > 280: f_k = fnt("Gloock-Regular.ttf", f_k.size-6)
    kw, kh = tw(d,"K",f_k), th(d,"K",f_k)
    d.text((cx-kw//2, cy-kh//2-50), "K", font=f_k, fill=BLACK)
    aguja(d, cx, cy+92, math.radians(-20), 280, hw=5)
    f_y = fnt("CrimsonPro-Bold.ttf", 30)
    d.text((cx-tw(d,"EST. 1980",f_y)//2, cy+140), "EST. 1980", font=f_y, fill=BORDO)
    img.save(OUT+"2-sello-laurel.png", "PNG", dpi=(300,300)); print("✓ 2-sello-laurel.png")

# ════════════════════════════════════════════════════════════════════
# 3 · SELLO TEJIDO (hilo entrelazado)
# ════════════════════════════════════════════════════════════════════
def sello_tejido():
    img = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(img)
    cx = cy = S//2
    # anillo exterior grueso bordo
    d.ellipse([cx-460, cy-460, cx+460, cy+460], outline=BORDO, width=6)
    d.ellipse([cx-444, cy-444, cx+444, cy+444], outline=BLACK, width=1)
    # banda con texto
    texto_arco(img, cx, cy, 412, "· KORMAN ETIQUETAS ·", fnt("Italiana-Regular.ttf", 48), BLACK, -90, 160)
    texto_arco(img, cx, cy, 412, "BUENOS AIRES · 1980", fnt("Italiana-Regular.ttf", 40), BORDO, 90, 110, flip=True)
    d = ImageDraw.Draw(img)
    d.ellipse([cx-380, cy-380, cx+380, cy+380], outline=BLACK, width=2)
    # patron de hilo entrelazado: dos guilloche desfasadas formando trenza
    guilloche(d, cx, cy, 350, 60, 18, GOLD, 1)
    guilloche(d, cx, cy, 350, 60, 18, BORDO, 1, phase=math.pi/60)
    # anillo punteado dorado
    perlado(d, cx, cy, 300, 80, 2.5, GOLD)
    d.ellipse([cx-280, cy-280, cx+280, cy+280], outline=BLACK, width=2)
    # centro: K Italiana grande
    f_k = fnt("Italiana-Regular.ttf", 420)
    while tw(d,"K",f_k) > 320: f_k = fnt("Italiana-Regular.ttf", f_k.size-6)
    kw, kh = tw(d,"K",f_k), th(d,"K",f_k)
    d.text((cx-kw//2, cy-kh//2-40), "K", font=f_k, fill=BLACK)
    # hilo y aguja entrelazados sobre el centro
    ax1, ay1 = aguja(d, cx+30, cy+70, math.radians(-30), 360, hw=5)
    px, py = ax1, ay1
    for t in range(0, 200, 4):
        a = math.radians(-30)
        xx = ax1 - t*math.cos(a-0.4)
        yy = ay1 - t*math.sin(a-0.4) + int(20*math.sin(t/18))
        d.line([(px,py),(xx,yy)], fill=GOLD, width=2); px, py = xx, yy
    img.save(OUT+"3-sello-tejido.png", "PNG", dpi=(300,300)); print("✓ 3-sello-tejido.png")

sello_guilloche()
sello_laurel()
sello_tejido()
print("\n✓ sellos circulares detallados listos")
