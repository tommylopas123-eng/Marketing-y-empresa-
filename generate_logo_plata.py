#!/usr/bin/env python3
"""KORMAN — techo dorado, aguja plateada con brillo metalico realista."""
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
GOLD=(184,146,62)

# Paleta plata metalica: sombra, base, brillo
SIL_DK=(120,124,132); SIL=(176,182,190); SIL_LT=(232,236,242); SIL_SHINE=(255,255,255)

def draw_aguja_plata(d,cx,cy,ang,length):
    ax1=cx-length/2*math.cos(ang); ay1=cy-length/2*math.sin(ang)
    ax2=cx+length/2*math.cos(ang); ay2=cy+length/2*math.sin(ang)
    perp=ang+math.pi/2
    taper=0.84
    tx=ax1+(ax2-ax1)*taper; ty=ay1+(ay2-ay1)*taper
    hw=9
    def poly(w,off,col):
        ox=off*math.cos(perp); oy=off*math.sin(perp)
        d.polygon([(ax1+w*math.cos(perp)+ox,ay1+w*math.sin(perp)+oy),
                   (tx+w*math.cos(perp)+ox,ty+w*math.sin(perp)+oy),
                   (ax2,ay2),
                   (tx-w*math.cos(perp)+ox,ty-w*math.sin(perp)+oy),
                   (ax1-w*math.cos(perp)+ox,ay1-w*math.sin(perp)+oy)],fill=col)
    # contorno oscuro
    poly(hw+2,0,(70,74,80))
    # base plata
    poly(hw,0,SIL)
    # sombra lado inferior
    poly(hw*0.5,hw*0.5,SIL_DK)
    # brillo lado superior
    poly(hw*0.45,-hw*0.5,SIL_LT)
    # linea de brillo central
    d.line([(ax1,ay1),(ax2,ay2)],fill=SIL_SHINE,width=2)
    # cabeza
    d.ellipse([ax1-hw-2,ay1-hw-2,ax1+hw+2,ay1+hw+2],fill=(70,74,80))
    d.ellipse([ax1-hw,ay1-hw,ax1+hw,ay1+hw],fill=SIL)
    d.ellipse([ax1-hw+3,ay1-hw+3,ax1+2,ay1+2],fill=SIL_LT)
    # ojo
    eye_cx=ax1+38*math.cos(ang); eye_cy=ay1+38*math.sin(ang)
    eye_img=Image.new("RGBA",(60,60),(0,0,0,0)); ed=ImageDraw.Draw(eye_img)
    ed.ellipse([30-5,30-17,30+5,30+17],outline=BLACK,width=4)
    eye_rot=eye_img.rotate(-math.degrees(ang),expand=False)
    return ax1,ay1,ang,eye_cx,eye_cy,eye_rot

def logo(fname, hilo):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=420
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=BLACK)
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=GOLD)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=GOLD)
    f=fnt("BigShoulders-Bold.ttf",560)
    while tw(d,"K",f)>R*1.7: f=fnt("BigShoulders-Bold.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-100),"K",font=f,fill=WHITE)
    ang=math.radians(-38)
    ax1,ay1,a,ecx,ecy,eye_rot=draw_aguja_plata(d,cx,cy+30,ang,760)
    px,py=ax1,ay1
    for t in range(0,210,4):
        xx=ax1-t*math.cos(a-0.35)
        yy=ay1-t*math.sin(a-0.35)+int(22*math.sin(t/20))
        d.line([(px,py),(xx,yy)],fill=hilo,width=3); px,py=xx,yy
    img.paste(eye_rot,(int(ecx)-30,int(ecy)-30),eye_rot)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

logo("logo-plata-hilo-oro.jpg",   GOLD)        # hilo dorado
logo("logo-plata-hilo-blanco.jpg",WHITE)       # hilo blanco
logo("logo-plata-hilo-plata.jpg", SIL)         # hilo plata
print("\n✓ listos")
