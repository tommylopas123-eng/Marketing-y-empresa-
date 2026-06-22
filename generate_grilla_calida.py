#!/usr/bin/env python3
"""KORMAN — mockup de grilla con filas de colores cálidos combinados."""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/grilla_calida/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
GOLD  = (176, 138, 58)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

def post_calido(bg, titulo_extra=None):
    """Genera un post 1080x1080 con fondo cálido dado."""
    BLACK = (22, 18, 14)
    GRAY  = tuple(max(c - 80, 30) for c in bg)

    img = Image.new("RGB", (W, H), bg)
    d   = ImageDraw.Draw(img)

    weave = tuple(max(c - 12, 0) for c in bg)
    for off in range(-H, W+H, 26):
        d.line([(off,0),(off+H,H)], fill=weave, width=1)
        d.line([(off+H,0),(off,H)], fill=weave, width=1)

    border = tuple(max(c - 30, 0) for c in bg)
    d.rectangle([18,18,W-18,H-18], outline=border, width=1)

    f_k = fnt("Jura-Light.ttf", 16)
    kick = "ETIQUETAS BORDADAS  ·  BUENOS AIRES"
    d.text(((W - tw(d,kick,f_k))//2, 108), kick, font=f_k, fill=GRAY)

    titulos = [("46 AÑOS", BLACK), ("CON ETIQUETAS", BLACK), ("BORDADAS", GOLD)]
    y = 210
    for txt, col in titulos:
        f_t = fnt("BigShoulders-Bold.ttf", 128)
        while tw(d, txt, f_t) > W-120:
            f_t = fnt("BigShoulders-Bold.ttf", f_t.size-4)
        d.text(((W - tw(d,txt,f_t))//2, y), txt, font=f_t, fill=col)
        y += f_t.size + 8

    ly = y + 20
    d.line([(W//2-120, ly),(W//2+120, ly)], fill=GOLD, width=2)

    f_s = fnt("InstrumentSans-Regular.ttf", 30)
    sub = "empresa familiar argentina"
    d.text(((W - tw(d,sub,f_s))//2, ly+28), sub, font=f_s, fill=GRAY)

    f_b = fnt("CrimsonPro-Bold.ttf", 22)
    brand = "KORMAN ETIQUETAS BORDADAS"
    d.text(((W - tw(d,brand,f_b))//2, H-58), brand, font=f_b, fill=BLACK)

    return img

# ── COMBINACIONES DE FILAS ─────────────────────────────────────────
# Cada combo: (nombre, color_fila_clara, color_fila_oscura)
combos = [
    ("A-beige-marron",
     (242, 235, 220),   # beige arena — fila clara
     (185, 158, 120)),  # marrón camel — fila oscura

    ("B-crema-terracota",
     (248, 240, 224),   # crema muy suave — fila clara
     (210, 172, 130)),  # terracota medio — fila oscura

    ("C-lino-cafe",
     (235, 224, 206),   # lino natural — fila clara
     (172, 140, 100)),  # café oscuro — fila oscura

    ("D-arena-siena",
     (244, 236, 218),   # arena pálida — fila clara
     (196, 152, 98)),   # siena cálido — fila oscura
]

cell = 360; gap = 6
GW = cell*3 + gap*2

for nombre, color_claro, color_oscuro in combos:
    # generar posts para cada fila
    p_claro  = post_calido(color_claro).resize((cell,cell), Image.LANCZOS)
    p_oscuro = post_calido(color_oscuro).resize((cell,cell), Image.LANCZOS)

    canvas = Image.new("RGB", (GW, GW), (200, 185, 165))

    # fila 1: oscuro oscuro oscuro
    for c in range(3):
        canvas.paste(p_oscuro, (c*(cell+gap), 0))
    # fila 2: claro claro claro
    for c in range(3):
        canvas.paste(p_claro,  (c*(cell+gap), cell+gap))
    # fila 3: oscuro oscuro oscuro
    for c in range(3):
        canvas.paste(p_oscuro, (c*(cell+gap), (cell+gap)*2))

    canvas.save(OUT + nombre + ".png", "PNG")
    print("✓", nombre)

# ── PANEL COMPARATIVO 2x2 ──────────────────────────────────────────
pw = GW*2 + 20
panel = Image.new("RGB", (pw, pw), (160, 140, 110))
for i, (nombre, _, __) in enumerate(combos):
    im = Image.open(OUT + nombre + ".png").convert("RGB").resize((GW, GW), Image.LANCZOS)
    r, c = divmod(i, 2)
    panel.paste(im, (c*(GW+20), r*(GW+20)))

    # label
    d_p = ImageDraw.Draw(panel)
    f_l = fnt("Jura-Light.ttf", 28)
    letra = nombre.split("-")[0].upper()
    d_p.text((c*(GW+20)+16, r*(GW+20)+GW-44), letra + " · " + nombre[2:].replace("-"," ").upper(), font=f_l, fill=(240,230,210))

panel.save("/home/user/Marketing-y-empresa-/assets/panel-grilla-calida.png", "PNG")
print("\n✓ panel-grilla-calida.png")
