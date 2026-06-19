#!/usr/bin/env python3
"""KORMAN — logo casa/hexagono, K grande, paletas propias (no copia)."""
from PIL import Image, ImageDraw, ImageFont
import math
FONTS="/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT="/home/user/Marketing-y-empresa-/assets/"
def fnt(n,s):
    try: return ImageFont.truetype(FONTS+n,s)
    except: return ImageFont.load_default()
def tw(d,t,f):
    b=d.textbbox((0,0),t,f); return b[2]-b[0]
def th(d,t,f):
    b=d.textbbox((0,0),t,f); return b[3]-b[1]
WHITE=(252,250,247)

def casa(fname, base, roof, swoosh, kfill=WHITE):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=420
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=base)
    # techo (dos triangulos superiores)
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=roof)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=roof)
    # K MUCHO mas grande
    f=fnt("BigShoulders-Bold.ttf",560)
    while tw(d,"K",f)>R*1.7: f=fnt("BigShoulders-Bold.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    # sombra sutil
    d.text((cx-kw//2+4,cy-kh//2-100+4),"K",font=f,fill=(0,0,0))
    d.text((cx-kw//2,cy-kh//2-100),"K",font=f,fill=kfill)
    # swoosh ascendente (aguja/flecha)
    pts=[(cx-350,cy+340),(cx-120,cy+210),(cx+130,cy+50),(cx+370,cy-270)]
    d.line(pts,fill=swoosh,width=20,joint="curve")
    d.polygon([(cx+370,cy-270),(cx+305,cy-205),(cx+400,cy-185)],fill=swoosh)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

# Paletas propias distintas al navy/rojo de ellos
casa("logo-casa-verde.jpg", base=(22,74,58), roof=(212,168,64), swoosh=(212,168,64))      # verde bosque + oro
casa("logo-casa-negro.jpg", base=(18,17,16), roof=(196,40,34), swoosh=(212,168,64))        # negro + techo rojo + oro
casa("logo-casa-borravino.jpg", base=(96,20,40), roof=(212,168,64), swoosh=(240,236,228))  # bordo + oro
casa("logo-casa-petroleo.jpg", base=(18,74,86), roof=(228,120,40), swoosh=(240,236,228))   # petroleo + naranja
casa("logo-casa-grafito.jpg", base=(44,46,52), roof=(120,140,160), swoosh=(212,168,64))    # grafito + acero + oro
casa("logo-casa-mostaza.jpg", base=(18,17,16), roof=(214,160,48), swoosh=(214,160,48))      # negro + mostaza monocromo

print("\n✓ 6 casas listas")
