#!/usr/bin/env python3
"""KORMAN — casa negra + acento color, aguja real atravesando."""
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
WHITE=(252,250,247); BLACK=(18,17,16)

def aguja_logo(fname, roof, accent, hilo):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=420
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=BLACK)
    # techo color de acento
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=roof)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=roof)
    # K grande blanca
    f=fnt("BigShoulders-Bold.ttf",560)
    while tw(d,"K",f)>R*1.7: f=fnt("BigShoulders-Bold.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2+4,cy-kh//2-100+4),"K",font=f,fill=(0,0,0))
    d.text((cx-kw//2,cy-kh//2-100),"K",font=f,fill=WHITE)

    # AGUJA real atravesando en diagonal (abajo-izq -> arriba-der)
    ax1,ay1=cx-360,cy+360   # cola (ojo)
    ax2,ay2=cx+380,cy-300   # punta
    # cuerpo de la aguja (metalico, color acento)
    d.line([(ax1,ay1),(ax2,ay2)],fill=accent,width=14)
    # brillo central mas claro
    light=tuple(min(255,c+60) for c in accent)
    d.line([(ax1,ay1),(ax2,ay2)],fill=light,width=4)
    # punta afilada
    ang=math.atan2(ay2-ay1,ax2-ax1)
    tiplen=46
    tx=ax2+tiplen*math.cos(ang); ty=ay2+tiplen*math.sin(ang)
    perp=ang+math.pi/2
    bw=14
    d.polygon([(tx,ty),
               (ax2+bw*math.cos(perp),ay2+bw*math.sin(perp)),
               (ax2-bw*math.cos(perp),ay2-bw*math.sin(perp))],fill=accent)
    # ojo de la aguja (elipse en la cola)
    eye_cx=ax1+40*math.cos(ang); eye_cy=ay1+40*math.sin(ang)
    d.ellipse([eye_cx-13,eye_cy-22,eye_cx+13,eye_cy+22],outline=accent,width=6)
    # hilo saliendo del ojo, ondulado
    px,py=ax1,ay1
    for t in range(0,200,4):
        xx=ax1-t*math.cos(ang-0.3)
        yy=ay1-t*math.sin(ang-0.3)+int(20*math.sin(t/18))
        d.line([(px,py),(xx,yy)],fill=hilo,width=4); px,py=xx,yy
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

# negro + distintos acentos
aguja_logo("logo-aguja-oro.jpg",    roof=(212,168,64),  accent=(212,168,64),  hilo=(212,168,64))   # negro + oro
aguja_logo("logo-aguja-rojo.jpg",   roof=(196,40,34),   accent=(196,40,34),   hilo=(212,168,64))   # negro + rojo + hilo oro
aguja_logo("logo-aguja-verde.jpg",  roof=(34,150,108),  accent=(34,150,108),  hilo=(240,236,228))  # negro + verde esmeralda
aguja_logo("logo-aguja-cobre.jpg",  roof=(198,108,58),  accent=(198,108,58),  hilo=(240,236,228))  # negro + cobre
aguja_logo("logo-aguja-celeste.jpg",roof=(64,150,196),  accent=(64,150,196),  hilo=(240,236,228))  # negro + celeste
aguja_logo("logo-aguja-fucsia.jpg", roof=(196,48,120),  accent=(196,48,120),  hilo=(212,168,64))   # negro + fucsia + hilo oro
print("\n✓ 6 logos aguja listos")
