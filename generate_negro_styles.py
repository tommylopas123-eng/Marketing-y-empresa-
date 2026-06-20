#!/usr/bin/env python3
"""KORMAN — 4 estilos de negro para elegir el estilo de los posts oscuros."""
from PIL import Image, ImageDraw, ImageFont
import os, math
FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/posts_negro_estilos/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
CREAM = (250, 248, 244)
GOLD  = (176, 138, 58)
GRAYW = (170, 168, 164)

def fnt(n, s):
    try:    return ImageFont.truetype(FONTS + n, s)
    except: return ImageFont.load_default()
def tw(d, t, f):
    b = d.textbbox((0,0), t, f); return b[2]-b[0]

def texto_central(img, lineas, gold_idx, sub, size=132):
    d = ImageDraw.Draw(img)
    fonts = []
    for ln in lineas:
        f = fnt("BigShoulders-Bold.ttf", size)
        while tw(d, ln, f) > W-140: f = fnt("BigShoulders-Bold.ttf", f.size-4)
        fonts.append(f)
    total_h = sum(f.size for f in fonts) + 6*(len(lineas)-1)
    y = (H - total_h)//2 - 40
    for i, ln in enumerate(lineas):
        col = GOLD if i == gold_idx else CREAM
        d.text(((W-tw(d,ln,fonts[i]))//2, y), ln, font=fonts[i], fill=col)
        y += fonts[i].size + 6
    ly = y + 18
    d.line([(W//2-120, ly),(W//2+120, ly)], fill=GOLD, width=2)
    f_s = fnt("InstrumentSans-Regular.ttf", 30)
    d.text(((W-tw(d,sub,f_s))//2, ly+28), sub, font=f_s, fill=GRAYW)
    f_b = fnt("CrimsonPro-Bold.ttf", 22)
    brand = "KORMAN ETIQUETAS BORDADAS"
    d.text(((W-tw(d,brand,f_b))//2, H-70), brand, font=f_b, fill=CREAM)

# ── ESTILO A: NEGRO MATE ────────────────────────────────────────────
def estilo_mate():
    BLACK = (10, 10, 10)
    img = Image.new("RGB", (W, H), BLACK)
    d   = ImageDraw.Draw(img)
    d.rectangle([18,18,W-18,H-18], outline=(28,28,28), width=1)
    texto_central(img, ["46 AÑOS", "CON ETIQUETAS", "BORDADAS"], 2, "empresa familiar argentina")
    img.save(OUT+"A-negro-mate.png", "PNG", dpi=(300,300))
    print("✓ A-negro-mate.png")

# ── ESTILO B: NEGRO METALIZADO (degradé grafito) ────────────────────
def estilo_metalizado():
    img = Image.new("RGB", (W, H), (10,10,10))
    d   = ImageDraw.Draw(img)
    # degradé vertical: negro arriba → grafito en diagonal → negro abajo
    for y in range(H):
        t = y / H
        # highlight en el centro-superior
        brightness = int(30 * math.exp(-((t-0.35)**2)/0.04))
        col = (18+brightness, 18+brightness, 20+brightness)
        d.line([(0,y),(W,y)], fill=col)
    # shimmer diagonal sutil
    for i in range(0, W+H, 60):
        alpha_col = (30,30,32)
        d.line([(i,0),(i-H,H)], fill=alpha_col, width=1)
    d.rectangle([18,18,W-18,H-18], outline=(55,55,58), width=1)
    texto_central(img, ["46 AÑOS", "CON ETIQUETAS", "BORDADAS"], 2, "empresa familiar argentina")
    img.save(OUT+"B-negro-metalizado.png", "PNG", dpi=(300,300))
    print("✓ B-negro-metalizado.png")

# ── ESTILO C: NEGRO TEXTURADO TIPO TELA ────────────────────────────
def estilo_texturado():
    BLACK = (12, 11, 11)
    img = Image.new("RGB", (W, H), BLACK)
    d   = ImageDraw.Draw(img)
    # trama densa tipo tejido (gap más pequeño = más detalle)
    gap = 14
    for off in range(-H, W+H, gap):
        d.line([(off,0),(off+H,H)], fill=(22,21,20), width=1)
        d.line([(off+H,0),(off,H)], fill=(20,19,18), width=1)
    # puntos de trama (efecto textil adicional)
    for y in range(0, H, 8):
        for x in range(y%16, W, 16):
            d.point((x,y), fill=(25,24,23))
    d.rectangle([18,18,W-18,H-18], outline=(38,36,34), width=1)
    texto_central(img, ["46 AÑOS", "CON ETIQUETAS", "BORDADAS"], 2, "empresa familiar argentina")
    img.save(OUT+"C-negro-texturado.png", "PNG", dpi=(300,300))
    print("✓ C-negro-texturado.png")

# ── ESTILO D: NEGRO CON RELIEVE (vignette + luz central) ───────────
def estilo_relieve():
    img = Image.new("RGB", (W, H), (8,8,8))
    d   = ImageDraw.Draw(img)
    # luz sutil desde el centro (relieve tipo estampado)
    cx, cy = W//2, H//2
    for radius in range(min(W,H)//2, 0, -2):
        t = radius / (min(W,H)//2)
        # bordes más oscuros, centro levemente más claro
        bright = int(14 * (1-t)**2)
        col = (8+bright, 8+bright, 8+bright)
        d.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], outline=col, width=2)
    # borde interior brillante (efecto relieve)
    d.rectangle([18,18,W-18,H-18], outline=(40,38,36), width=2)
    d.rectangle([22,22,W-22,H-22], outline=(18,16,15), width=1)
    texto_central(img, ["46 AÑOS", "CON ETIQUETAS", "BORDADAS"], 2, "empresa familiar argentina")
    img.save(OUT+"D-negro-relieve.png", "PNG", dpi=(300,300))
    print("✓ D-negro-relieve.png")

estilo_mate()
estilo_metalizado()
estilo_texturado()
estilo_relieve()

# ── PANEL COMPARATIVO 2x2 ──────────────────────────────────────────
cell = 520; gap = 8
panel = Image.new("RGB", (cell*2+gap, cell*2+gap), (40,40,40))
files = ["A-negro-mate.png", "B-negro-metalizado.png", "C-negro-texturado.png", "D-negro-relieve.png"]
labels = ["A · MATE", "B · METALIZADO", "C · TEXTURADO TELA", "D · RELIEVE"]
for i, (fname, label) in enumerate(zip(files, labels)):
    im = Image.open(OUT+fname).convert("RGB").resize((cell, cell), Image.LANCZOS)
    r, c = divmod(i, 2)
    x, y = c*(cell+gap), r*(cell+gap)
    panel.paste(im, (x, y))
    # label en el panel
    d_panel = ImageDraw.Draw(panel)
    f_label = ImageFont.truetype(FONTS+"InstrumentSans-Regular.ttf", 22) if os.path.exists(FONTS+"InstrumentSans-Regular.ttf") else ImageFont.load_default()
    d_panel.text((x+16, y+cell-42), label, font=f_label, fill=(200,198,194))

panel.save(OUT+"PANEL-estilos-negro.png", "PNG")
print("\n✓ PANEL-estilos-negro.png — 4 estilos listos")
