#!/usr/bin/env python3
"""KORMAN — logos a color, estilo emblema moderno (como competencia)."""
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

WHITE=(252,250,247)
# Paletas vibrantes
NAVY=(28,42,92); RED=(196,42,38); GOLD=(212,168,64)
TEAL=(20,110,114); ORANGE=(228,120,40); PURPLE=(78,46,120)
EMERALD=(24,108,72); WINE=(120,24,52)

# 1 — HEXAGONO CASA: K monograma rojo en hexagono navy + flecha/aguja ascendente dorada
#     (replica directa del estilo ST: casa + monograma + swoosh)
def t1():
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=400
    # hexagono navy (forma de casa)
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=NAVY)
    # techo rojo (triangulo superior)
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=RED)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=RED)
    # K blanca grande
    f=fnt("BigShoulders-Bold.ttf",380)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-90),"K",font=f,fill=WHITE)
    # swoosh dorado ascendente (aguja con punta tipo flecha)
    pts=[(cx-340,cy+330),(cx-120,cy+200),(cx+120,cy+40),(cx+360,cy-260)]
    d.line(pts,fill=GOLD,width=18,joint="curve")
    # punta flecha
    d.polygon([(cx+360,cy-260),(cx+300,cy-200),(cx+390,cy-180)],fill=GOLD)
    img.save(OUT+"logo-color-casa.jpg","JPEG",quality=97); print("✓ logo-color-casa.jpg")
t1()

# 2 — CIRCULO BICOLOR: K en circulo dividido navy/rojo, aro dorado, aguja
def t2():
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=410
    # circulo base
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=NAVY)
    # mitad inferior rojo (diagonal)
    mask=Image.new("L",(S,S),0); md=ImageDraw.Draw(mask)
    md.polygon([(0,360),(S,200),(S,S),(0,S)],fill=255)
    red_layer=Image.new("RGB",(S,S),RED)
    circ=Image.new("L",(S,S),0); cd=ImageDraw.Draw(circ)
    cd.ellipse([cx-R,cy-R,cx+R,cy+R],fill=255)
    from PIL import ImageChops
    final_mask=ImageChops.multiply(mask,circ)
    img.paste(red_layer,(0,0),final_mask)
    d=ImageDraw.Draw(img)
    # aro dorado
    d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=GOLD,width=10)
    d.ellipse([cx-R+22,cy-R+22,cx+R-22,cy+R-22],outline=WHITE,width=2)
    # K blanca
    f=fnt("BricolageGrotesque-Bold.ttf",400)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-70),"K",font=f,fill=WHITE)
    img.save(OUT+"logo-color-circulo.jpg","JPEG",quality=97); print("✓ logo-color-circulo.jpg")
t2()

# 3 — ESCUDO TEAL/ORANGE: K en escudo teal con banda naranja
def t3():
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx=S//2; top=120; bot=880; wid=350
    sh=[(cx-wid,top),(cx+wid,top),(cx+wid,560),(cx,bot),(cx-wid,560)]
    d.polygon(sh,fill=TEAL)
    # banda naranja diagonal
    band=Image.new("RGBA",(S,S),(0,0,0,0)); bd=ImageDraw.Draw(band)
    bd.polygon([(cx-wid,420),(cx+wid,300),(cx+wid,400),(cx-wid,520)],fill=(*ORANGE,255))
    shmask=Image.new("L",(S,S),0); sd=ImageDraw.Draw(shmask); sd.polygon(sh,fill=255)
    img.paste(band,(0,0),Image.composite(band.split()[3],Image.new("L",(S,S),0),shmask))
    d=ImageDraw.Draw(img)
    d.line(sh+[sh[0]],fill=WHITE,width=6)
    f=fnt("BigShoulders-Bold.ttf",320)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,210),"K",font=f,fill=WHITE)
    # aguja blanca vertical
    d.line([(cx,600),(cx,720)],fill=WHITE,width=6)
    d.ellipse([cx-9,608,cx+9,626],outline=WHITE,width=3)
    img.save(OUT+"logo-color-escudo.jpg","JPEG",quality=97); print("✓ logo-color-escudo.jpg")
t3()

# 4 — ROMBO PURPLE/GOLD: K en rombo violeta con hilo dorado
def t4():
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=400
    d.polygon([(cx,cy-R),(cx+R,cy),(cx,cy+R),(cx-R,cy)],fill=PURPLE)
    Ri=R-24
    d.line([(cx,cy-Ri),(cx+Ri,cy),(cx,cy+Ri),(cx-Ri,cy),(cx,cy-Ri)],fill=GOLD,width=6)
    f=fnt("BricolageGrotesque-Bold.ttf",380)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-60),"K",font=f,fill=WHITE)
    # hilo dorado ondulado
    px,py=cx-300,cy+120
    d.line([(cx-300,cy+120),(cx+300,cy-120)],fill=GOLD,width=6)
    d.ellipse([cx+290,cy-132,cx+312,cy-110],outline=GOLD,width=4)
    img.save(OUT+"logo-color-rombo.jpg","JPEG",quality=97); print("✓ logo-color-rombo.jpg")
t4()

# 5 — EMBLEMA EMERALD: circulo emerald, monograma KE dorado
def t5():
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=410
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=EMERALD)
    d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=GOLD,width=8)
    d.ellipse([cx-R+26,cy-R+26,cx+R-26,cy+R-26],outline=GOLD,width=2)
    fk=fnt("Italiana-Regular.ttf",460)
    kw=tw(d,"K",fk); kh=th(d,"K",fk)
    d.text((cx-kw+40,cy-kh//2-90),"K",font=fk,fill=WHITE)
    d.text((cx-60,cy-kh//2-90),"E",font=fk,fill=GOLD)
    img.save(OUT+"logo-color-emerald.jpg","JPEG",quality=97); print("✓ logo-color-emerald.jpg")
t5()

# 6 — WINE BADGE: badge cuadrado vino con K crema y aguja dorada
def t6():
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; bw=720
    d.rounded_rectangle([cx-bw//2,cy-bw//2,cx+bw//2,cy+bw//2],radius=100,fill=WINE)
    d.rounded_rectangle([cx-bw//2+24,cy-bw//2+24,cx+bw//2-24,cy+bw//2-24],radius=80,outline=GOLD,width=4)
    f=fnt("BricolageGrotesque-Bold.ttf",400)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-90),"K",font=f,fill=WHITE)
    # aguja dorada diagonal
    d.line([(cx-200,cy+180),(cx+220,cy-200)],fill=GOLD,width=8)
    d.ellipse([cx+208,cy-212,cx+232,cy-188],outline=GOLD,width=4)
    img.save(OUT+"logo-color-wine.jpg","JPEG",quality=97); print("✓ logo-color-wine.jpg")
t6()

print("\n✓ 6 logos a color listos")
