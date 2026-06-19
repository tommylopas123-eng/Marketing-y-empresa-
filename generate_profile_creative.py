#!/usr/bin/env python3
"""KORMAN — conceptos creativos, sin circulos."""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/assets/"
random.seed(7)

def fnt(n,s):
    try: return ImageFont.truetype(FONTS+n,s)
    except: return ImageFont.load_default()
def tw(d,t,f):
    b=d.textbbox((0,0),t,f); return b[2]-b[0]
def th(d,t,f):
    b=d.textbbox((0,0),t,f); return b[3]-b[1]

# ── A — PUNTADA: KORMAN formado por una linea de puntadas continua ──
# La marca dibujada como hilo cosido sobre tela. Diagonal dinamica.
def puntada():
    S=1000
    img=Image.new("RGB",(S,S),(248,245,239)); d=ImageDraw.Draw(img)
    # Trama de tela tenue
    for y in range(0,S,7):
        d.line([(0,y),(S,y)],fill=(240,237,230),width=1)
    for x in range(0,S,7):
        d.line([(x,0),(x,S)],fill=(243,240,233),width=1)
    # Bloque negro diagonal grande (corte sastre)
    d.polygon([(0,640),(S,420),(S,S),(0,S)],fill=(12,11,10))
    # Hilo cosido cruzando — puntadas tipo running stitch en rojo
    red=(150,30,24)
    y0=300
    x=40
    pts=[]
    while x < S-40:
        yy = y0 + int(38*math.sin(x/95))
        pts.append((x,yy)); x+=4
    for i in range(0,len(pts)-6,9):
        d.line([pts[i],pts[i+5]],fill=red,width=4)
    # KORMAN grande negro sobre la zona clara
    f=fnt("BigShoulders-Bold.ttf",150)
    while tw(d,"KORMAN",f)>S-90: f=fnt("BigShoulders-Bold.ttf",f.size-4)
    w=tw(d,"KORMAN",f); h=th(d,"KORMAN",f)
    d.text((S//2-w//2,150),"KORMAN",font=f,fill=(12,11,10))
    # ETIQUETAS BORDADAS en blanco sobre el bloque negro
    f2=fnt("Jura-Medium.ttf",40)
    t="ETIQUETAS  BORDADAS"; w2=tw(d,t,f2)
    d.text((S//2-w2//2,800),t,font=f2,fill=(248,245,239))
    # aguja: linea fina con ojo
    img.save(OUT+"perfil-puntada.jpg","JPEG",quality=97); print("✓ perfil-puntada.jpg")
puntada()

# ── B — BAUHAUS SASTRE: composicion asimetrica con bloques de color ──
def bauhaus():
    S=1000
    img=Image.new("RGB",(S,S),(236,232,224)); d=ImageDraw.Draw(img)
    black=(15,14,13); gold=(190,150,60); red=(150,40,30)
    # Banda vertical negra a la izquierda
    d.rectangle([0,0,300,S],fill=black)
    # Banda dorada inferior
    d.rectangle([300,760,S,S],fill=gold)
    # Cuadrado rojo
    d.rectangle([300,0,S,300],fill=red)
    # Hilo: linea diagonal fina cruzando todo
    d.line([(0,0),(S,S)],fill=(255,255,255),width=1)
    # KORMAN rotado vertical en la banda negra
    txt_img=Image.new("RGBA",(900,260),(0,0,0,0)); td=ImageDraw.Draw(txt_img)
    f=fnt("BigShoulders-Bold.ttf",160)
    while tw(td,"KORMAN",f)>880: f=fnt("BigShoulders-Bold.ttf",f.size-4)
    td.text((10,30),"KORMAN",font=f,fill=(248,245,239))
    rot=txt_img.rotate(90,expand=True)
    img.paste(rot,(20,S//2-rot.height//2),rot)
    # ETIQUETAS en el cuadrado rojo
    f2=fnt("Jura-Medium.ttf",46)
    d.text((340,110),"ETIQUETAS",font=f2,fill=(248,245,239))
    f3=fnt("Jura-Light.ttf",34)
    d.text((342,175),"BORDADAS",font=f3,fill=(248,245,239))
    # EST 1980 sobre dorado
    f4=fnt("BigShoulders-Bold.ttf",100)
    d.text((360,810),"1980",font=f4,fill=black)
    f5=fnt("Jura-Light.ttf",26)
    d.text((640,860),"EST.",font=f5,fill=black)
    img.save(OUT+"perfil-bauhaus.jpg","JPEG",quality=97); print("✓ perfil-bauhaus.jpg")
bauhaus()

# ── C — CARRETEL: hilo enrollado formando composicion vertical ──
def carretel():
    S=1000
    img=Image.new("RGB",(S,S),(14,12,10)); d=ImageDraw.Draw(img)
    gold=(205,170,90); gold_d=(120,95,45); cream=(244,236,216)
    # Lineas de hilo enrolladas — diagonales densas en la mitad inferior
    cx=S//2
    for i in range(-260,260,5):
        shade=gold if (i//5)%2==0 else gold_d
        d.line([(cx+i,560),(cx+i+40,940)],fill=shade,width=2)
    # Bloque carretel (madera) arriba y abajo del hilo
    d.rectangle([cx-280,520,cx+280,560],fill=cream)
    d.rectangle([cx-280,940,cx+280,980],fill=cream)
    # KORMAN arriba en cream serif
    f=fnt("YoungSerif-Regular.ttf",128)
    while tw(d,"KORMAN",f)>S-120: f=fnt("YoungSerif-Regular.ttf",f.size-4)
    w=tw(d,"KORMAN",f)
    d.text((cx-w//2,180),"KORMAN",font=f,fill=cream)
    f2=fnt("Jura-Light.ttf",40)
    t="E T I Q U E T A S   B O R D A D A S"; w2=tw(d,t,f2)
    d.text((cx-w2//2,330),t,font=f2,fill=gold)
    img.save(OUT+"perfil-carretel.jpg","JPEG",quality=97); print("✓ perfil-carretel.jpg")
carretel()

# ── D — ESCUDO SASTRE: emblema con forma de escudo (no circulo) ──
def escudo():
    S=1000
    img=Image.new("RGB",(S,S),(245,242,235)); d=ImageDraw.Draw(img)
    black=(16,15,14); gold=(180,145,65)
    cx=S//2
    # Forma de escudo (shield) centrado
    top=140; bot=880; wid=300
    pts=[(cx-wid,top),(cx+wid,top),(cx+wid,560),
         (cx,bot),(cx-wid,560)]
    d.polygon(pts,fill=black)
    # Borde dorado interior del escudo
    inpts=[(cx-wid+18,top+18),(cx+wid-18,top+18),(cx+wid-18,555),
           (cx,bot-40),(cx-wid+18,555)]
    d.line(inpts+[inpts[0]],fill=gold,width=2)
    # Linea horizontal divisoria (chief del escudo)
    d.line([(cx-wid+18,330),(cx+wid-18,330)],fill=gold,width=1)
    # K grande gravada arriba del escudo
    f=fnt("BricolageGrotesque-Bold.ttf",200)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,150),"K",font=f,fill=gold)
    # KORMAN vertical en el cuerpo del escudo
    f2=fnt("Jura-Medium.ttf",52)
    t="KORMAN"; 
    # letra por letra apilada
    yy=370
    for ch in t:
        cw=tw(d,ch,f2)
        d.text((cx-cw//2,yy),ch,font=f2,fill=(244,236,216))
        yy+=58
    # ETIQUETAS BORDADAS bajo el escudo
    f3=fnt("Jura-Light.ttf",30)
    t2="ETIQUETAS  BORDADAS"; w3=tw(d,t2,f3)
    d.text((cx-w3//2,910),t2,font=f3,fill=black)
    img.save(OUT+"perfil-escudo.jpg","JPEG",quality=97); print("✓ perfil-escudo.jpg")
escudo()

print("\n✓ 4 conceptos creativos listos")
