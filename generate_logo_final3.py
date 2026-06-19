#!/usr/bin/env python3
"""KORMAN — techo dorado, aguja en color contrastante."""
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
GOLD=(184,146,62); GOLD_LT=(220,184,104); GOLD_DK=(132,100,40)  # dorado metalico real

def lighten(c,n): return tuple(min(255,x+n) for x in c)
def darken(c,n): return tuple(max(0,x-n) for x in c)

def draw_aguja(d,cx,cy,ang,length,col):
    col_lt=lighten(col,70); col_dk=darken(col,70)
    ax1=cx-length/2*math.cos(ang); ay1=cy-length/2*math.sin(ang)
    ax2=cx+length/2*math.cos(ang); ay2=cy+length/2*math.sin(ang)
    perp=ang+math.pi/2
    taper=0.82
    tx=ax1+(ax2-ax1)*taper; ty=ay1+(ay2-ay1)*taper
    hw=8
    out=[(ax1+(hw+2)*math.cos(perp),ay1+(hw+2)*math.sin(perp)),
         (tx+(hw+2)*math.cos(perp),ty+(hw+2)*math.sin(perp)),
         (ax2,ay2),
         (tx-(hw+2)*math.cos(perp),ty-(hw+2)*math.sin(perp)),
         (ax1-(hw+2)*math.cos(perp),ay1-(hw+2)*math.sin(perp))]
    d.polygon(out,fill=col_dk)
    body=[(ax1+hw*math.cos(perp),ay1+hw*math.sin(perp)),
          (tx+hw*math.cos(perp),ty+hw*math.sin(perp)),
          (ax2,ay2),
          (tx-hw*math.cos(perp),ty-hw*math.sin(perp)),
          (ax1-hw*math.cos(perp),ay1-hw*math.sin(perp))]
    d.polygon(body,fill=col)
    d.line([(ax1,ay1),(ax2,ay2)],fill=col_lt,width=3)
    d.ellipse([ax1-hw-2,ay1-hw-2,ax1+hw+2,ay1+hw+2],fill=col_dk)
    d.ellipse([ax1-hw,ay1-hw,ax1+hw,ay1+hw],fill=col)
    eye_cx=ax1+36*math.cos(ang); eye_cy=ay1+36*math.sin(ang)
    eye_img=Image.new("RGBA",(60,60),(0,0,0,0)); ed=ImageDraw.Draw(eye_img)
    ed.ellipse([30-5,30-16,30+5,30+16],outline=BLACK,width=4)
    eye_rot=eye_img.rotate(-math.degrees(ang),expand=False)
    return ax1,ay1,ang,eye_cx,eye_cy,eye_rot

def logo(fname, aguja_col):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=420
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=BLACK)
    # TECHO DORADO
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=GOLD)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=GOLD)
    f=fnt("BigShoulders-Bold.ttf",560)
    while tw(d,"K",f)>R*1.7: f=fnt("BigShoulders-Bold.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-100),"K",font=f,fill=WHITE)
    ang=math.radians(-38)
    ax1,ay1,a,ecx,ecy,eye_rot=draw_aguja(d,cx,cy+30,ang,760,aguja_col)
    px,py=ax1,ay1
    for t in range(0,210,4):
        xx=ax1-t*math.cos(a-0.35)
        yy=ay1-t*math.sin(a-0.35)+int(22*math.sin(t/20))
        d.line([(px,py),(xx,yy)],fill=aguja_col,width=3); px,py=xx,yy
    img.paste(eye_rot,(int(ecx)-30,int(ecy)-30),eye_rot)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

logo("logo-aguja-plata.jpg",   (208,210,214))   # plata/acero
logo("logo-aguja-blanca.jpg",  WHITE)            # blanca
logo("logo-aguja-roja.jpg",    (190,44,38))      # roja
logo("logo-aguja-petroleo.jpg",(36,128,140))     # petroleo/turquesa
logo("logo-aguja-cobre.jpg",   (192,96,52))      # cobre
logo("logo-aguja-bordo.jpg",   (120,28,48))      # bordo
print("\n✓ listos")
