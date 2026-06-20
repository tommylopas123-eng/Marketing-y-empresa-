#!/usr/bin/env python3
"""KORMAN — A (hexagono linea) y B (monograma circular) con bordo de distintas formas."""
from PIL import Image, ImageDraw, ImageFont
import math, os
FONTS="/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT="/home/user/Marketing-y-empresa-/assets/pruebas-bordo/"
os.makedirs(OUT, exist_ok=True)
def fnt(n,s):
    try: return ImageFont.truetype(FONTS+n,s)
    except: return ImageFont.load_default()
def tw(d,t,f):
    b=d.textbbox((0,0),t,f); return b[2]-b[0]
def th(d,t,f):
    b=d.textbbox((0,0),t,f); return b[3]-b[1]

WHITE=(252,250,247); BLACK=(18,17,16)
BORDO=(124,38,50); SIL=(176,182,190); SIL_LT=(232,236,242)

def aguja_fina(d,cx,cy,ang,length,hw=4,col=SIL,colhi=SIL_LT):
    ax1=cx-length/2*math.cos(ang); ay1=cy-length/2*math.sin(ang)
    ax2=cx+length/2*math.cos(ang); ay2=cy+length/2*math.sin(ang)
    perp=ang+math.pi/2; taper=0.9
    tx=ax1+(ax2-ax1)*taper; ty=ay1+(ay2-ay1)*taper
    d.polygon([(ax1+hw*math.cos(perp),ay1+hw*math.sin(perp)),
               (tx+hw*math.cos(perp),ty+hw*math.sin(perp)),(ax2,ay2),
               (tx-hw*math.cos(perp),ty-hw*math.sin(perp)),
               (ax1-hw*math.cos(perp),ay1-hw*math.sin(perp))],fill=col)
    d.line([(ax1,ay1),(ax2,ay2)],fill=colhi,width=1)
    d.ellipse([ax1-hw-1,ay1-hw-1,ax1+hw+1,ay1+hw+1],fill=col)
    eye=Image.new("RGBA",(40,40),(0,0,0,0)); ed=ImageDraw.Draw(eye)
    ed.ellipse([20-3,20-11,20+3,20+11],outline=BLACK,width=2)
    return ax1,ay1,eye.rotate(-math.degrees(ang),expand=False)

# ───────────────────── A · HEXAGONO LINEA — variantes bordo ─────────────────────
def hexagono(fname, hex_col, inner_col, roof_col, k_col):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=370
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.line(hexp+[hexp[0]],fill=hex_col,width=3,joint="curve")
    for i in (1,3,5):
        d.line([(cx,cy),hexp[i]],fill=inner_col,width=2)
    d.line([hexp[0],hexp[1]],fill=roof_col,width=3)
    d.line([hexp[5],hexp[0]],fill=roof_col,width=3)
    d.line([(cx,cy),hexp[1]],fill=roof_col,width=2)
    d.line([(cx,cy),hexp[5]],fill=roof_col,width=2)
    f=fnt("Italiana-Regular.ttf",430)
    while tw(d,"K",f)>R*1.1: f=fnt("Italiana-Regular.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-90),"K",font=f,fill=k_col)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

# A1 — techo y aristas en bordo, resto negro
hexagono("A1-techo-bordo.jpg",   BLACK, BLACK, BORDO, BLACK)
# A2 — todo el contorno en bordo, K negra
hexagono("A2-contorno-bordo.jpg", BORDO, BORDO, BORDO, BLACK)
# A3 — hexagono negro, K en bordo
hexagono("A3-k-bordo.jpg",        BLACK, BLACK, BLACK, BORDO)

# ───────────────────── B · MONOGRAMA CIRCULAR — variantes bordo ─────────────────
def monograma(fname, ring_col, inner_ring_col, k_col, needle=True):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=360
    d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=ring_col,width=3)
    d.ellipse([cx-R+14,cy-R+14,cx+R-14,cy+R-14],outline=inner_ring_col,width=1)
    f=fnt("Gloock-Regular.ttf",420)
    while tw(d,"K",f)>R*1.0: f=fnt("Gloock-Regular.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-70),"K",font=f,fill=k_col)
    if needle:
        aguja_fina(d,cx,cy+40,math.radians(-30),560,hw=3)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

# B1 — anillo exterior bordo, K negra
monograma("B1-anillo-bordo.jpg",   BORDO, BORDO, BLACK)
# B2 — anillo negro, K bordo
monograma("B2-k-bordo.jpg",        BLACK, BORDO, BORDO)
# B3 — anillo negro + anillo fino interior bordo, K negra
monograma("B3-detalle-bordo.jpg",  BLACK, BORDO, BLACK)
print("\n✓ listos")
