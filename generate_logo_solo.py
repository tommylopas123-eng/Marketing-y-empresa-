#!/usr/bin/env python3
"""KORMAN — solo el logo/emblema (sin nombre abajo). Varios tipos."""
from PIL import Image, ImageDraw, ImageFont
import math, os
FONTS="/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT="/home/user/Marketing-y-empresa-/assets/"
def fnt(n,s):
    try: return ImageFont.truetype(FONTS+n,s)
    except: return ImageFont.load_default()
def tw(d,t,f):
    b=d.textbbox((0,0),t,f); return b[2]-b[0]
def th(d,t,f):
    b=d.textbbox((0,0),t,f); return b[3]-b[1]
BLACK=(15,14,13); CREAM=(248,245,239); GOLD=(196,158,68); GOLD_D=(120,96,42); RED=(150,38,30)

# 1 — ROMBO AGUJA: K en rombo negro, aguja+hilo. emblema centrado, ocupa casi todo.
def t1():
    S=1000; img=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=420
    d.polygon([(cx,cy-R),(cx+R,cy),(cx,cy+R),(cx-R,cy)],fill=BLACK)
    Ri=R-26
    d.line([(cx,cy-Ri),(cx+Ri,cy),(cx,cy+Ri),(cx-Ri,cy),(cx,cy-Ri)],fill=GOLD,width=4)
    f=fnt("BricolageGrotesque-Bold.ttf",420)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-70),"K",font=f,fill=CREAM)
    d.line([(cx-250,cy+230),(cx+290,cy-280)],fill=GOLD,width=6)
    d.ellipse([cx+278,cy-294,cx+302,cy-270],outline=GOLD,width=4)
    px,py=cx-250,cy+230
    for t in range(0,160,4):
        xx=cx-250-t; yy=cy+230+int(22*math.sin(t/16))
        d.line([(px,py),(xx,yy)],fill=RED,width=4); px,py=xx,yy
    img.save(OUT+"logo-rombo-aguja.jpg","JPEG",quality=97); print("✓ logo-rombo-aguja.jpg")
t1()

# 2 — HEXAGONO CARRETEL: K en hexagono cream sobre negro
def t2():
    S=1000; img=Image.new("RGB",(S,S),BLACK); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=430
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=CREAM)
    Ri=R-30
    hexi=[(cx+Ri*math.cos(math.radians(60*i-90)),cy+Ri*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.line(hexi+[hexi[0]],fill=GOLD,width=5)
    f=fnt("BigShoulders-Bold.ttf",460)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-110),"K",font=f,fill=BLACK)
    for yy in range(cy+150,cy+250,11):
        d.line([(cx-110,yy),(cx+110,yy)],fill=GOLD,width=4)
    d.rectangle([cx-130,cy+136,cx+130,cy+148],fill=RED)
    d.rectangle([cx-130,cy+250,cx+130,cy+262],fill=RED)
    img.save(OUT+"logo-hexa-carretel.jpg","JPEG",quality=97); print("✓ logo-hexa-carretel.jpg")
t2()

# 3 — BADGE KE: monograma K+E entrelazado en badge redondeado
def t3():
    S=1000; img=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; bw=760
    d.rounded_rectangle([cx-bw//2,cy-bw//2,cx+bw//2,cy+bw//2],radius=110,fill=BLACK)
    d.rounded_rectangle([cx-bw//2+26,cy-bw//2+26,cx+bw//2-26,cy+bw//2-26],radius=88,outline=GOLD,width=4)
    fk=fnt("Italiana-Regular.ttf",560)
    kw=tw(d,"K",fk); kh=th(d,"K",fk)
    d.text((cx-kw+50,cy-kh//2-110),"K",font=fk,fill=CREAM)
    d.text((cx-70,cy-kh//2-110),"E",font=fk,fill=GOLD)
    img.save(OUT+"logo-badge-ke.jpg","JPEG",quality=97); print("✓ logo-badge-ke.jpg")
t3()

# 4 — ESCUDO: K en escudo sastre, emblema completo
def t4():
    S=1000; img=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(img)
    cx=S//2; top=110; bot=900; wid=360
    sh=[(cx-wid,top),(cx+wid,top),(cx+wid,560),(cx,bot),(cx-wid,560)]
    d.polygon(sh,fill=BLACK)
    si=[(cx-wid+22,top+22),(cx+wid-22,top+22),(cx+wid-22,552),(cx,bot-44),(cx-wid+22,552)]
    d.line(si+[si[0]],fill=GOLD,width=4)
    d.line([(cx-wid+22,350),(cx+wid-22,350)],fill=GOLD,width=2)
    f=fnt("BricolageGrotesque-Bold.ttf",330)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,150),"K",font=f,fill=CREAM)
    d.line([(cx,600),(cx,720)],fill=GOLD,width=5)
    d.ellipse([cx-8,610,cx+8,626],outline=GOLD,width=3)
    img.save(OUT+"logo-escudo-solo.jpg","JPEG",quality=97); print("✓ logo-escudo-solo.jpg")
t4()

# 5 — CIRCULO MINIMAL: K sola, fina, dorada, centrada en negro (lujo silencioso)
def t5():
    S=1000; img=Image.new("RGB",(S,S),BLACK); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2
    f=fnt("Italiana-Regular.ttf",620)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-150),"K",font=f,fill=CREAM)
    # punto dorado pequeño como acento
    d.ellipse([cx+150,cy+150,cx+172,cy+172],fill=GOLD)
    img.save(OUT+"logo-k-minimal.jpg","JPEG",quality=97); print("✓ logo-k-minimal.jpg")
t5()

# 6 — TRAMA: K calada sobre patron de bordado (puntos), estilo textil
def t6():
    S=1000; img=Image.new("RGB",(S,S),BLACK); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2
    for x in range(60,S-60,26):
        for y in range(60,S-60,26):
            d.ellipse([x-3,y-3,x+3,y+3],fill=(40,36,28))
    # K grande dorada encima
    f=fnt("BigShoulders-Bold.ttf",560)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    # sombra
    d.text((cx-kw//2+4,cy-kh//2-140+4),"K",font=f,fill=(8,7,6))
    d.text((cx-kw//2,cy-kh//2-140),"K",font=f,fill=GOLD)
    img.save(OUT+"logo-k-trama-dorada.jpg","JPEG",quality=97); print("✓ logo-k-trama-dorada.jpg")
t6()

print("\n✓ 6 logos solos listos")
