#!/usr/bin/env python3
"""KORMAN — sellos circulares ELEGANTES, punto medio (un detalle distintivo c/u)."""
from PIL import Image, ImageDraw, ImageFont
import math, os
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/pruebas-circular-medio/"
os.makedirs(OUT, exist_ok=True)

S = 1200
BG    = (252, 250, 247)
BLACK = (18,  15,  15 )
BORDO = (124, 38,  50 )
GOLD  = (176, 138, 58 )
SIL   = (176, 182, 190)
SIL_LT= (224, 228, 234)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]
def th(d, t, f):
    b = d.textbbox((0,0), t, f); return b[3]-b[1]

def texto_arco(img, cx, cy, R, texto, font, color, arc_center_deg, total_deg, flip=False):
    n = len(texto)
    if n == 0: return
    if flip: texto = texto[::-1]
    start = arc_center_deg - total_deg/2
    step  = total_deg/(n-1) if n > 1 else 0
    for i, ch in enumerate(texto):
        deg = start + i*step; a = math.radians(deg)
        x = cx + R*math.cos(a); y = cy + R*math.sin(a)
        ci = Image.new("RGBA", (70,70), (0,0,0,0)); cd = ImageDraw.Draw(ci)
        bb = cd.textbbox((0,0), ch, font=font); cw, chh = bb[2]-bb[0], bb[3]-bb[1]
        cd.text((35-cw//2-bb[0], 35-chh//2-bb[1]), ch, font=font, fill=color)
        rot = (-deg-90) if not flip else (-deg+90)
        ci = ci.rotate(rot, expand=False, resample=Image.BICUBIC)
        img.paste(ci, (int(x)-35, int(y)-35), ci)

def aguja(d, cx, cy, ang, length, hw=5):
    ax1 = cx-length/2*math.cos(ang); ay1 = cy-length/2*math.sin(ang)
    ax2 = cx+length/2*math.cos(ang); ay2 = cy+length/2*math.sin(ang)
    perp = ang+math.pi/2; taper = 0.9
    tx = ax1+(ax2-ax1)*taper; ty = ay1+(ay2-ay1)*taper
    d.polygon([(ax1+hw*math.cos(perp),ay1+hw*math.sin(perp)),
               (tx+hw*math.cos(perp),ty+hw*math.sin(perp)),(ax2,ay2),
               (tx-hw*math.cos(perp),ty-hw*math.sin(perp)),
               (ax1-hw*math.cos(perp),ay1-hw*math.sin(perp))], fill=SIL)
    d.line([(ax1,ay1),(ax2,ay2)], fill=SIL_LT, width=1)
    d.ellipse([ax1-hw-1,ay1-hw-1,ax1+hw+1,ay1+hw+1], fill=(90,94,100))
    d.ellipse([ax1-hw+1,ay1-hw+1,ax1+hw-1,ay1+hw-1], fill=SIL)
    return ax1, ay1

def estrella4(d, cx, cy, r, color):
    d.polygon([(cx,cy-r),(cx+r*0.28,cy-r*0.28),(cx+r,cy),(cx+r*0.28,cy+r*0.28),
               (cx,cy+r),(cx-r*0.28,cy+r*0.28),(cx-r,cy),(cx-r*0.28,cy-r*0.28)], fill=color)

# ── 1 · LIMPIO CLÁSICO ──────────────────────────────────────────────
# Doble anillo fino + texto + K + aguja. Cero relleno extra.
def limpio():
    img = Image.new("RGB",(S,S),BG); d = ImageDraw.Draw(img)
    cx=cy=S//2
    d.ellipse([cx-440,cy-440,cx+440,cy+440], outline=BLACK, width=3)
    # letras rellenas (serif bold) para que se lean bien en Instagram
    texto_arco(img,cx,cy,386,"KORMAN ETIQUETAS BORDADAS",fnt("CrimsonPro-Bold.ttf",54),BLACK,-90,205)
    texto_arco(img,cx,cy,386,"EST. 1980",fnt("CrimsonPro-Bold.ttf",46),BORDO,90,48,flip=True)
    d = ImageDraw.Draw(img)
    f_k = fnt("Gloock-Regular.ttf",400)
    while tw(d,"K",f_k)>340: f_k=fnt("Gloock-Regular.ttf",f_k.size-6)
    # centrado exacto usando el bounding box real (compensa el margen lateral de la fuente)
    kb = d.textbbox((0,0),"K",font=f_k)
    kx = cx - (kb[0]+kb[2])//2
    ky = cy - (kb[1]+kb[3])//2 - 8
    d.text((kx,ky),"K",font=f_k,fill=BLACK)
    # aguja con hilo
    ax1,ay1=aguja(d,cx,cy+140,math.radians(-22),300,hw=5)
    px,py=ax1,ay1
    for t in range(0,150,4):
        a=math.radians(-22)
        xx=ax1-t*math.cos(a-0.45); yy=ay1-t*math.sin(a-0.45)+int(15*math.sin(t/15))
        d.line([(px,py),(xx,yy)],fill=BORDO,width=2); px,py=xx,yy
    img.save(OUT+"1-limpio.png","PNG",dpi=(300,300)); print("✓ 1-limpio.png")

# ── 2 · UN ANILLO GUILLOCHÉ SUAVE ───────────────────────────────────
def guilloche_suave():
    img = Image.new("RGB",(S,S),BG); d = ImageDraw.Draw(img)
    cx=cy=S//2
    d.ellipse([cx-440,cy-440,cx+440,cy+440], outline=BLACK, width=3)
    texto_arco(img,cx,cy,398,"KORMAN ETIQUETAS",fnt("Italiana-Regular.ttf",56),BLACK,-90,150)
    texto_arco(img,cx,cy,398,"BUENOS AIRES",fnt("Italiana-Regular.ttf",46),BORDO,90,80,flip=True)
    d = ImageDraw.Draw(img)
    # un solo anillo guilloche fino, sutil, dorado
    pts=[]
    for i in range(1441):
        t=2*math.pi*i/1440; r=360+9*math.cos(40*t)
        pts.append((cx+r*math.cos(t),cy+r*math.sin(t)))
    d.line(pts,fill=GOLD,width=1,joint="curve")
    d.ellipse([cx-330,cy-330,cx+330,cy+330], outline=BLACK, width=2)
    f_k = fnt("Gloock-Regular.ttf",400)
    while tw(d,"K",f_k)>320: f_k=fnt("Gloock-Regular.ttf",f_k.size-6)
    kw,kh=tw(d,"K",f_k),th(d,"K",f_k)
    d.text((cx-kw//2,cy-kh//2-46),"K",font=f_k,fill=BLACK)
    aguja(d,cx,cy+98,math.radians(-22),290,hw=5)
    img.save(OUT+"2-guilloche-suave.png","PNG",dpi=(300,300)); print("✓ 2-guilloche-suave.png")

# ── 3 · MINIMAL CON HILO ────────────────────────────────────────────
def minimal_hilo():
    img = Image.new("RGB",(S,S),BG); d = ImageDraw.Draw(img)
    cx=cy=S//2
    d.ellipse([cx-430,cy-430,cx+430,cy+430], outline=BLACK, width=2)
    texto_arco(img,cx,cy,388,"KORMAN ETIQUETAS BORDADAS",fnt("Jura-Medium.ttf",38),BLACK,-90,210)
    texto_arco(img,cx,cy,388,"DESDE 1980",fnt("Jura-Medium.ttf",34),BORDO,90,60,flip=True)
    d = ImageDraw.Draw(img)
    # K + aguja con hilo bordo elegante saliendo
    f_k = fnt("Italiana-Regular.ttf",460)
    while tw(d,"K",f_k)>360: f_k=fnt("Italiana-Regular.ttf",f_k.size-6)
    kw,kh=tw(d,"K",f_k),th(d,"K",f_k)
    d.text((cx-kw//2,cy-kh//2-40),"K",font=f_k,fill=BLACK)
    ax1,ay1=aguja(d,cx+20,cy+60,math.radians(-30),360,hw=5)
    px,py=ax1,ay1
    for t in range(0,170,4):
        a=math.radians(-30)
        xx=ax1-t*math.cos(a-0.4); yy=ay1-t*math.sin(a-0.4)+int(16*math.sin(t/16))
        d.line([(px,py),(xx,yy)],fill=BORDO,width=2); px,py=xx,yy
    img.save(OUT+"3-minimal-hilo.png","PNG",dpi=(300,300)); print("✓ 3-minimal-hilo.png")

limpio(); guilloche_suave(); minimal_hilo()
print("\n✓ listos")
