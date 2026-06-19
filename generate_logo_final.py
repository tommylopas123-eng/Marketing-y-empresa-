#!/usr/bin/env python3
"""KORMAN — logo final: negro + dorado, aguja fina real (sin flecha)."""
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
GOLD=(206,166,74); GOLD_LT=(238,212,140); GOLD_DK=(150,116,44)

def draw_aguja(d,cx,cy,ang,length,gold,gold_lt):
    """Aguja fina realista: cuerpo afinado a punta + ojo, SIN flecha."""
    ax1=cx-length/2*math.cos(ang); ay1=cy-length/2*math.sin(ang)  # cabeza (ojo)
    ax2=cx+length/2*math.cos(ang); ay2=cy+length/2*math.sin(ang)  # punta
    perp=ang+math.pi/2
    # punto donde empieza a afinar (90% hacia la punta)
    taper=0.82
    tx=ax1+(ax2-ax1)*taper; ty=ay1+(ay2-ay1)*taper
    hw=7  # medio ancho del cuerpo
    # cuerpo: polígono que afina de hw a 0 en la punta
    body=[
        (ax1+hw*math.cos(perp),ay1+hw*math.sin(perp)),
        (tx+hw*math.cos(perp),ty+hw*math.sin(perp)),
        (ax2,ay2),
        (tx-hw*math.cos(perp),ty-hw*math.sin(perp)),
        (ax1-hw*math.cos(perp),ay1-hw*math.sin(perp)),
    ]
    d.polygon(body,fill=gold)
    # brillo central
    d.line([(ax1,ay1),(ax2,ay2)],fill=gold_lt,width=2)
    # cabeza redondeada
    d.ellipse([ax1-hw,ay1-hw,ax1+hw,ay1+hw],fill=gold)
    # ojo de la aguja (elipse hueca cerca de la cabeza)
    eye_cx=ax1+34*math.cos(ang); eye_cy=ay1+34*math.sin(ang)
    ew,eh=5,16
    # elipse rotada para el ojo
    eye_img=Image.new("RGBA",(60,60),(0,0,0,0)); ed=ImageDraw.Draw(eye_img)
    ed.ellipse([30-ew,30-eh,30+ew,30+eh],outline=BLACK,width=4)
    eye_rot=eye_img.rotate(-math.degrees(ang),expand=False)
    return ax1,ay1,ang,eye_cx,eye_cy,eye_rot

def logo(fname, roof_gold=GOLD, two_tone=False):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=420
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=BLACK)
    # techo dorado
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=roof_gold)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=roof_gold)
    # K grande blanca
    f=fnt("BigShoulders-Bold.ttf",560)
    while tw(d,"K",f)>R*1.7: f=fnt("BigShoulders-Bold.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-100),"K",font=f,fill=WHITE)
    # aguja diagonal dorada (sin flecha)
    ang=math.radians(-38)
    info=draw_aguja(d,cx,cy+30,ang,760,GOLD,GOLD_LT)
    ax1,ay1,a,ecx,ecy,eye_rot=info
    # hilo dorado fino saliendo de la cabeza, ondulado
    px,py=ax1,ay1
    for t in range(0,210,4):
        xx=ax1-t*math.cos(a-0.35)
        yy=ay1-t*math.sin(a-0.35)+int(22*math.sin(t/20))
        d.line([(px,py),(xx,yy)],fill=GOLD,width=3); px,py=xx,yy
    # pegar ojo de aguja encima
    img.paste(eye_rot,(int(ecx)-30,int(ecy)-30),eye_rot)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

logo("logo-final-1.jpg")
print("\n✓ logo final listo")
