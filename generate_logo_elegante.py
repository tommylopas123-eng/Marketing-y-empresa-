#!/usr/bin/env python3
"""KORMAN — direcciones elegantes: linea fina, mas aire, K con estilo, aguja fina."""
from PIL import Image, ImageDraw, ImageFont
import math, os
FONTS="/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT="/home/user/Marketing-y-empresa-/assets/pruebas-elegante/"
os.makedirs(OUT, exist_ok=True)
def fnt(n,s):
    try: return ImageFont.truetype(FONTS+n,s)
    except: return ImageFont.load_default()
def tw(d,t,f):
    b=d.textbbox((0,0),t,f); return b[2]-b[0]
def th(d,t,f):
    b=d.textbbox((0,0),t,f); return b[3]-b[1]

WHITE=(252,250,247); BLACK=(18,17,16)
GOLD=(176,138,58); SIL=(176,182,190); SIL_LT=(232,236,242)

def aguja_fina(d,cx,cy,ang,length,hw=4,col=SIL,colhi=SIL_LT):
    """Aguja delgada y elegante."""
    ax1=cx-length/2*math.cos(ang); ay1=cy-length/2*math.sin(ang)
    ax2=cx+length/2*math.cos(ang); ay2=cy+length/2*math.sin(ang)
    perp=ang+math.pi/2
    taper=0.9
    tx=ax1+(ax2-ax1)*taper; ty=ay1+(ay2-ay1)*taper
    def poly(w,col):
        d.polygon([(ax1+w*math.cos(perp),ay1+w*math.sin(perp)),
                   (tx+w*math.cos(perp),ty+w*math.sin(perp)),
                   (ax2,ay2),
                   (tx-w*math.cos(perp),ty-w*math.sin(perp)),
                   (ax1-w*math.cos(perp),ay1-w*math.sin(perp))],fill=col)
    poly(hw,col)
    d.line([(ax1,ay1),(ax2,ay2)],fill=colhi,width=1)
    # cabeza con ojo
    d.ellipse([ax1-hw-1,ay1-hw-1,ax1+hw+1,ay1+hw+1],fill=col)
    eye=Image.new("RGBA",(40,40),(0,0,0,0)); ed=ImageDraw.Draw(eye)
    ed.ellipse([20-3,20-11,20+3,20+11],outline=BLACK,width=2)
    return ax1,ay1,eye.rotate(-math.degrees(ang),expand=False),ax1,ay1

# ───────────────────────────── A · HEXAGONO LINEA FINA ─────────────────────────
def dir_A(fname, techo=GOLD):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=370
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    # contorno hexagono fino
    d.line(hexp+[hexp[0]],fill=BLACK,width=3,joint="curve")
    # lineas internas del cubo isometrico (Y) finas
    for i in (1,3,5):
        d.line([(cx,cy),hexp[i]],fill=BLACK,width=2)
    # techo: solo las dos aristas superiores en dorado
    d.line([hexp[0],hexp[1]],fill=techo,width=3)
    d.line([hexp[5],hexp[0]],fill=techo,width=3)
    d.line([(cx,cy),hexp[1]],fill=techo,width=2)
    d.line([(cx,cy),hexp[5]],fill=techo,width=2)
    # K serif elegante
    f=fnt("Italiana-Regular.ttf",430)
    while tw(d,"K",f)>R*1.1: f=fnt("Italiana-Regular.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-90),"K",font=f,fill=BLACK)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

# ───────────────────────────── B · MONOGRAMA CIRCULAR ──────────────────────────
def dir_B(fname, acc=GOLD):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=360
    d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=BLACK,width=3)
    d.ellipse([cx-R+14,cy-R+14,cx+R-14,cy+R-14],outline=acc,width=1)
    # K serif alto
    f=fnt("Gloock-Regular.ttf",420)
    while tw(d,"K",f)>R*1.0: f=fnt("Gloock-Regular.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-70),"K",font=f,fill=BLACK)
    # aguja fina horizontal-diagonal cruzando suave
    ang=math.radians(-30)
    aguja_fina(d,cx,cy+40,ang,560,hw=3)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

# ───────────────────────────── C · CUBO REFINADO ───────────────────────────────
def dir_C(fname, techo=GOLD):
    S=1000; img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
    cx,cy=S//2,S//2; R=370
    hexp=[(cx+R*math.cos(math.radians(60*i-90)),cy+R*math.sin(math.radians(60*i-90))) for i in range(6)]
    d.polygon(hexp,fill=BLACK)
    d.polygon([hexp[0],hexp[1],(cx,cy)],fill=techo)
    d.polygon([hexp[0],hexp[5],(cx,cy)],fill=techo)
    # K serif elegante en vez de bold pesada
    f=fnt("Italiana-Regular.ttf",480)
    while tw(d,"K",f)>R*1.3: f=fnt("Italiana-Regular.ttf",f.size-6)
    kw=tw(d,"K",f); kh=th(d,"K",f)
    d.text((cx-kw//2,cy-kh//2-90),"K",font=f,fill=WHITE)
    # aguja fina
    ang=math.radians(-38)
    ax1,ay1,eye_rot,ex,ey=aguja_fina(d,cx,cy+30,ang,640,hw=4)
    img.paste(eye_rot,(int(ex)-20,int(ey)-20),eye_rot)
    img.save(OUT+fname,"JPEG",quality=97); print("✓",fname)

dir_A("A-hexagono-linea.jpg")
dir_B("B-monograma-circular.jpg")
dir_C("C-cubo-refinado.jpg")
print("\n✓ listos")
