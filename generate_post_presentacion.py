#!/usr/bin/env python3
"""KORMAN ETIQUETAS — Post de presentación v2."""
from PIL import Image, ImageDraw, ImageFont
import os, math
FONTS="/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT="/home/user/Marketing-y-empresa-/posts_v5/"
os.makedirs(OUT, exist_ok=True)
def fnt(n,s):
    try: return ImageFont.truetype(FONTS+n,s)
    except: return ImageFont.load_default()
def tw(d,t,f):
    b=d.textbbox((0,0),t,f); return b[2]-b[0]
def th(d,t,f):
    b=d.textbbox((0,0),t,f); return b[3]-b[1]

W=H=1080
BG=(252,250,246); BLACK=(8,8,8); GRAY_MD=(110,108,104); GRAY_LT=(200,198,194)
GOLD=(176,138,58)
DOT=(238,235,229)   # trama textil sutil

img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

# ── FONDO: tejido sutil — finas líneas diagonales cruzadas (urdimbre/trama) ──
WEAVE=(244,241,234)
gap=26
for off in range(-H, W, gap):
    d.line([(off,0),(off+H,H)], fill=WEAVE, width=1)      # diagonal \\
    d.line([(off+H,0),(off,H)], fill=WEAVE, width=1)      # diagonal //

# ── ELEMENTO ATRÁS DEL TEXTO: "1980" gigante en contorno dorado tenue ──
f_big=fnt("BigShoulders-Bold.ttf",460)
big="1980"
bw=tw(d,big,f_big); bh=th(d,big,f_big)
# texto contorneado (outline) en dorado muy suave, centrado verticalmente
# 1980 de fondo DESACTIVADO (prueba sin el numero)
pass
d=ImageDraw.Draw(img)

# Borde perimetral
m=18
d.rectangle([m,m,W-m,H-m],outline=GRAY_LT,width=1)

# ── BLOQUE DE TEXTO CENTRAL ──
# Tipo arriba
f_tipo=fnt("Jura-Light.ttf",15)
tipo="ETIQUETAS BORDADAS  ·  BUENOS AIRES"
d.text(((W-tw(d,tipo,f_tipo))//2,120),tipo,font=f_tipo,fill=GRAY_MD)

# Título grande — el mensaje principal
f_t=fnt("BigShoulders-Bold.ttf",118)
t1="46 AÑOS"
while tw(d,t1,f_t)>W-120: f_t=fnt("BigShoulders-Bold.ttf",f_t.size-4)
d.text(((W-tw(d,t1,f_t))//2,210),t1,font=f_t,fill=BLACK)

f_t2=fnt("BigShoulders-Bold.ttf",118)
t2="CON ETIQUETAS"
while tw(d,t2,f_t2)>W-120: f_t2=fnt("BigShoulders-Bold.ttf",f_t2.size-4)
d.text(((W-tw(d,t2,f_t2))//2,330),t2,font=f_t2,fill=BLACK)

f_t3=fnt("BigShoulders-Bold.ttf",118)
t3="BORDADAS"
while tw(d,t3,f_t3)>W-120: f_t3=fnt("BigShoulders-Bold.ttf",f_t3.size-4)
d.text(((W-tw(d,t3,f_t3))//2,450),t3,font=f_t3,fill=GOLD)

# Línea dorada
ly=600; ll=240
d.line([(W//2-ll//2,ly),(W//2+ll//2,ly)],fill=GOLD,width=2)

# Texto cuerpo
f_b=fnt("InstrumentSans-Regular.ttf",30)
lines=[
    "Empresa familiar argentina",
    "especializada en etiquetas bordadas",
    "para marcas.",
]
y=648
for line in lines:
    d.text(((W-tw(d,line,f_b))//2,y),line,font=f_b,fill=GRAY_MD)
    y+=54

# CTA — información en la bio
f_cta=fnt("BigShoulders-Bold.ttf",46)
cta="INFORMACIÓN EN LA BIO"
d.text(((W-tw(d,cta,f_cta))//2,y+34),cta,font=f_cta,fill=BLACK)

# Brand mark
f_brand=fnt("BricolageGrotesque-Bold.ttf",14)
brand="KORMAN ETIQUETAS"
d.text(((W-tw(d,brand,f_brand))//2,H-58),brand,font=f_brand,fill=BLACK)
d.line([(W//2-40,H-40),(W//2+40,H-40)],fill=GOLD,width=1)

img.save(OUT+"00-presentacion.png","PNG",dpi=(300,300)); print("✓ 00-presentacion.png")
