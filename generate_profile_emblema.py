#!/usr/bin/env python3
"""KORMAN — emblemas tipo logo-marca (estilo icono como competencia)."""
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

BLACK=(15,14,13); CREAM=(248,245,239); GOLD=(190,152,64); GOLD_D=(120,96,42)
RED=(150,38,30)

# ── A — EMBLEMA AGUJA: monograma K con aguja+hilo dentro de un escudo/diamante ──
def emblema_aguja():
    S=1000
    img=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(img)
    cx,cy=S//2,440
    # Diamante / rombo (forma contenedora, no circulo)
    R=320
    dia=[(cx,cy-R),(cx+R,cy),(cx,cy+R),(cx-R,cy)]
    d.polygon(dia,fill=BLACK)
    # borde dorado interior
    Ri=R-22
    d.line([(cx,cy-Ri),(cx+Ri,cy),(cx,cy+Ri),(cx-Ri,cy),(cx,cy-Ri)],fill=GOLD,width=3)
    # K grande centrada
    f=fnt("BricolageGrotesque-Bold.ttf",290)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-50),"K",font=f,fill=CREAM)
    # Aguja diagonal con hilo atravesando
    nx1,ny1=cx-180,cy+170; nx2,ny2=cx+210,cy-200
    d.line([(nx1,ny1),(nx2,ny2)],fill=GOLD,width=5)
    # ojo de aguja
    d.ellipse([nx2-12,ny2-12,nx2+4,ny2+4],outline=GOLD,width=3)
    # hilo ondulado saliendo
    px,py=nx1,ny1
    for t in range(0,120,4):
        xx=nx1-t
        yy=ny1+int(18*math.sin(t/14))
        d.line([(px,py),(xx,yy)],fill=RED,width=3); px,py=xx,yy
    # KORMAN abajo del emblema
    f2=fnt("BricolageGrotesque-Bold.ttf",92)
    while tw(d,"KORMAN",f2)>S-160: f2=fnt("BricolageGrotesque-Bold.ttf",f2.size-4)
    w2=tw(d,"KORMAN",f2)
    d.text((cx-w2//2,800),"KORMAN",font=f2,fill=BLACK)
    f3=fnt("Jura-Light.ttf",34)
    t3="E T I Q U E T A S   B O R D A D A S"; w3=tw(d,t3,f3)
    d.text((cx-w3//2,905),t3,font=f3,fill=GOLD_D)
    img.save(OUT+"emblema-aguja.jpg","JPEG",quality=97); print("✓ emblema-aguja.jpg")
emblema_aguja()

# ── B — EMBLEMA HEXAGONO: K monograma + carretel dentro de hexagono (como casa de ST) ──
def emblema_hexa():
    S=1000
    img=Image.new("RGB",(S,S),BLACK); d=ImageDraw.Draw(img)
    cx,cy=S//2,430
    R=330
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=CREAM)
    Ri=R-26
    hexi=[(cx+Ri*math.cos(math.radians(60*i-90)),cy+Ri*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.line(hexi+[hexi[0]],fill=GOLD,width=4)
    # K negra grande
    f=fnt("BigShoulders-Bold.ttf",340)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-40),"K",font=f,fill=BLACK)
    # carretel: lineas horizontales doradas debajo de la K (hilo enrollado)
    for yy in range(cy+120,cy+200,10):
        d.line([(cx-90,yy),(cx+90,yy)],fill=GOLD,width=3)
    d.rectangle([cx-110,cy+108,cx+110,cy+118],fill=RED)
    d.rectangle([cx-110,cy+200,cx+110,cy+210],fill=RED)
    # KORMAN abajo cream
    f2=fnt("BigShoulders-Bold.ttf",110)
    while tw(d,"KORMAN",f2)>S-140: f2=fnt("BigShoulders-Bold.ttf",f2.size-4)
    w2=tw(d,"KORMAN",f2)
    d.text((cx-w2//2,800),"KORMAN",font=f2,fill=CREAM)
    f3=fnt("Jura-Light.ttf",32)
    t3="ETIQUETAS  BORDADAS  ·  EST. 1980"; w3=tw(d,t3,f3)
    d.text((cx-w3//2,915),t3,font=f3,fill=GOLD)
    img.save(OUT+"emblema-hexa.jpg","JPEG",quality=97); print("✓ emblema-hexa.jpg")
emblema_hexa()

# ── C — EMBLEMA MONOGRAMA KE entrelazado dentro de un sello cuadrado redondeado ──
def emblema_ke():
    S=1000
    img=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(img)
    cx,cy=S//2,440
    # cuadrado redondeado negro (badge)
    bw=620
    d.rounded_rectangle([cx-bw//2,cy-bw//2,cx+bw//2,cy+bw//2],radius=80,fill=BLACK)
    d.rounded_rectangle([cx-bw//2+20,cy-bw//2+20,cx+bw//2-20,cy+bw//2-20],radius=64,outline=GOLD,width=3)
    # K y E entrelazadas grandes
    fk=fnt("Italiana-Regular.ttf",420)
    ew=tw(d,"K",fk); ehh=th(d,"K",fk)
    d.text((cx-ew+30,cy-ehh//2-70),"K",font=fk,fill=CREAM)
    fe=fnt("Italiana-Regular.ttf",420)
    d.text((cx-40,cy-ehh//2-70),"E",font=fe,fill=GOLD)
    # KORMAN abajo
    f2=fnt("Italiana-Regular.ttf",96)
    w2=tw(d,"KORMAN ETIQUETAS",f2)
    while w2>S-100:
        f2=fnt("Italiana-Regular.ttf",f2.size-3); w2=tw(d,"KORMAN ETIQUETAS",f2)
    d.text((cx-w2//2,810),"KORMAN ETIQUETAS",font=f2,fill=BLACK)
    f3=fnt("Jura-Light.ttf",30)
    t3="B O R D A D A S"; w3=tw(d,t3,f3)
    d.text((cx-w3//2,915),t3,font=f3,fill=GOLD_D)
    img.save(OUT+"emblema-ke.jpg","JPEG",quality=97); print("✓ emblema-ke.jpg")
emblema_ke()

# ── D — EMBLEMA ESCUDO MODERNO con K + aguja vertical (estilo deportivo/marca) ──
def emblema_escudo():
    S=1000
    img=Image.new("RGB",(S,S),CREAM); d=ImageDraw.Draw(img)
    cx=S//2; top=120; bot=720; wid=290
    shield=[(cx-wid,top),(cx+wid,top),(cx+wid,440),(cx,bot),(cx-wid,440)]
    d.polygon(shield,fill=BLACK)
    sin=[(cx-wid+18,top+18),(cx+wid-18,top+18),(cx+wid-18,432),(cx,bot-36),(cx-wid+18,432)]
    d.line(sin+[sin[0]],fill=GOLD,width=3)
    # franja diagonal dorada (banda heraldica)
    d.line([(cx-wid+18,top+150),(cx+wid-18,top+60)],fill=GOLD_D,width=2)
    # K grande
    f=fnt("BricolageGrotesque-Bold.ttf",260)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,250),"K",font=f,fill=CREAM)
    # aguja vertical bajo la K
    d.line([(cx,540),(cx,640)],fill=GOLD,width=4)
    d.ellipse([cx-6,548,cx+6,560],outline=GOLD,width=2)
    # KORMAN ETIQUETAS abajo
    f2=fnt("BricolageGrotesque-Bold.ttf",82)
    while tw(d,"KORMAN",f2)>S-200: f2=fnt("BricolageGrotesque-Bold.ttf",f2.size-3)
    w2=tw(d,"KORMAN",f2)
    d.text((cx-w2//2,790),"KORMAN",font=f2,fill=BLACK)
    f3=fnt("Jura-Light.ttf",34)
    t3="E T I Q U E T A S   B O R D A D A S"; w3=tw(d,t3,f3)
    d.text((cx-w3//2,895),t3,font=f3,fill=GOLD_D)
    img.save(OUT+"emblema-escudo-moderno.jpg","JPEG",quality=97); print("✓ emblema-escudo-moderno.jpg")
emblema_escudo()

print("\n✓ 4 emblemas listos")
