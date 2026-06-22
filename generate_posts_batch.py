#!/usr/bin/env python3
"""
KORMAN — Instagram Post Batch Generator
Posts 02, 03, 04
Design philosophy: Hilo Nocturno
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/.agents/design/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

BG        = (18, 16, 14)
GOLD      = (198, 158, 86)
CREAM     = (235, 224, 200)
RUST      = (140, 80, 48)
CHARCOAL  = (38, 34, 30)
GOLD_DIM  = (110, 85, 42)

def load_font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def base_canvas():
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # diagonal thread lines
    for i in range(-H, W+H, 24):
        draw.line([(i, 0), (i + H, H)], fill=(32, 28, 24), width=1)
    # margin
    draw.rectangle([28, 28, W-28, H-28], outline=(42, 38, 32), width=1)
    return img, draw

def draw_stitch(d, cx, cy, size, color, width=1):
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    d.polygon(pts, outline=color, fill=None)
    d.line([(cx-size//2, cy-size//2),(cx+size//2, cy+size//2)], fill=color, width=width)
    d.line([(cx+size//2, cy-size//2),(cx-size//2, cy+size//2)], fill=color, width=width)

def rust_line(draw, x1, y1, x2, y2):
    draw.line([(x1,y1),(x2,y2)], fill=RUST, width=2)

def registration_mark(draw, cx, cy):
    r = 12
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=GOLD_DIM, width=1)
    draw.line([(cx-20,cy),(cx+20,cy)], fill=GOLD_DIM, width=1)
    draw.line([(cx,cy-20),(cx,cy+20)], fill=GOLD_DIM, width=1)

# ═══════════════════════════════════════════════════════════════════════════════
# POST 02 — "Sin mínimos altos. Tu primera etiqueta."
# ═══════════════════════════════════════════════════════════════════════════════
def post_02():
    img, draw = base_canvas()
    random.seed(7)

    # Fine grid — top half
    for x in range(60, W-60, 16):
        draw.line([(x, 60), (x, 480)], fill=(28,24,20), width=1)
    for y in range(60, 480, 16):
        draw.line([(60, y), (W-60, y)], fill=(28,24,20), width=1)

    # Stitch row — horizontal decorative band at 1/3
    for i, x in enumerate(range(80, W-80, 36)):
        draw_stitch(draw, x, 360, 10, GOLD_DIM if i % 2 == 0 else RUST, 1)

    # Vertical rust accent left
    rust_line(draw, 72, 80, 72, 920)
    draw.line([(68,80),(76,80)], fill=RUST, width=2)
    draw.line([(68,920),(76,920)], fill=RUST, width=2)

    # Number "01" — large ghost watermark
    f_big = load_font("Gloock-Regular.ttf", 320)
    draw.text((480, 60), "01", font=f_big, fill=(30,26,22))

    # Typography
    f_it  = load_font("Italiana-Regular.ttf", 88)
    f_sub = load_font("InstrumentSans-Regular.ttf", 30)
    f_sm  = load_font("Jura-Light.ttf", 17)
    f_br  = load_font("ArsenalSC-Regular.ttf", 38)
    f_tag = load_font("InstrumentSans-Regular.ttf", 22)

    draw.text((100, 430), "Sin mínimos", font=f_it, fill=CREAM)
    draw.text((100, 528), "altos.", font=f_it, fill=GOLD)

    # Rule
    draw.line([(100, 650), (W-100, 650)], fill=GOLD_DIM, width=1)
    draw.line([(100, 656), (420, 656)], fill=GOLD_DIM, width=1)

    draw.text((100, 680), "Tu primera etiqueta empieza acá.", font=f_sub, fill=CREAM)
    draw.text((100, 726), "Pedidos chicos para marcas que arrancan.", font=f_sm, fill=GOLD_DIM)

    # Bottom
    draw.line([(100, 860), (W-100, 860)], fill=GOLD_DIM, width=1)
    draw.text((100, 892), "KORMAN", font=f_br, fill=CREAM)
    draw.text((100, 944), "@kormanetiquetas", font=f_tag, fill=GOLD)

    registration_mark(draw, W-80, H-80)
    draw.text((W-108, H-58), "02 · BA", font=f_sm, fill=GOLD_DIM)

    path = OUT + "korman-post-02-sin-minimos.png"
    img.save(path, "PNG", dpi=(300,300))
    print(f"Saved: {path}")

# ═══════════════════════════════════════════════════════════════════════════════
# POST 03 — Proceso / "Cada punto, tu marca."
# ═══════════════════════════════════════════════════════════════════════════════
def post_03():
    img, draw = base_canvas()
    random.seed(13)

    # Dense stitch field — right column (process feel)
    for row in range(8):
        for col in range(6):
            sx = 600 + col * 72
            sy = 100 + row * 100
            if random.random() > 0.2:
                sz = random.randint(8, 18)
                col_choice = GOLD if random.random() > 0.5 else GOLD_DIM
                draw_stitch(draw, sx, sy, sz, col_choice, 1)

    # Vertical separator line
    draw.line([(540, 60), (540, H-60)], fill=CHARCOAL, width=2)
    draw.line([(546, 60), (546, H-60)], fill=GOLD_DIM, width=1)

    # Left panel: typography
    f_it   = load_font("Italiana-Regular.ttf", 96)
    f_it2  = load_font("Italiana-Regular.ttf", 78)
    f_sub  = load_font("InstrumentSans-Regular.ttf", 24)
    f_sm   = load_font("Jura-Light.ttf", 16)
    f_br   = load_font("ArsenalSC-Regular.ttf", 38)
    f_tag  = load_font("InstrumentSans-Regular.ttf", 22)

    rust_line(draw, 72, 120, 72, 820)

    draw.text((100, 160), "Cada", font=f_it, fill=CREAM)
    draw.text((100, 262), "punto,", font=f_it, fill=GOLD)
    draw.text((100, 364), "tu marca.", font=f_it2, fill=CREAM)

    # Process steps — numbered list, sparse
    draw.line([(100, 520), (480, 520)], fill=GOLD_DIM, width=1)

    steps = [
        ("01", "Diseño"),
        ("02", "Muestra"),
        ("03", "Producción"),
        ("04", "Entrega"),
    ]
    f_num  = load_font("GeistMono-Regular.ttf", 14)
    f_step = load_font("InstrumentSans-Regular.ttf", 20)
    for i, (num, label) in enumerate(steps):
        y = 544 + i * 56
        draw.text((100, y), num, font=f_num, fill=RUST)
        draw.text((148, y), label, font=f_step, fill=CREAM)
        draw.ellipse([138, y+6, 142, y+10], fill=RUST)

    draw.line([(100, 772), (480, 772)], fill=GOLD_DIM, width=1)
    draw.text((100, 800), "Producción local · CABA", font=f_sm, fill=GOLD_DIM)

    # Bottom
    draw.line([(100, 880), (480, 880)], fill=GOLD_DIM, width=1)
    draw.text((100, 912), "KORMAN", font=f_br, fill=CREAM)
    draw.text((100, 962), "@kormanetiquetas", font=f_tag, fill=GOLD)

    registration_mark(draw, W-80, H-80)
    draw.text((W-108, H-58), "03 · BA", font=f_sm, fill=GOLD_DIM)

    path = OUT + "korman-post-03-proceso.png"
    img.save(path, "PNG", dpi=(300,300))
    print(f"Saved: {path}")

# ═══════════════════════════════════════════════════════════════════════════════
# POST 04 — "Local vs China" — contraste duro
# ═══════════════════════════════════════════════════════════════════════════════
def post_04():
    img, draw = base_canvas()

    # Top half: dark / import side
    draw.rectangle([28, 28, W-28, H//2], fill=(14, 12, 10))
    # Bottom half: slightly warmer / KORMAN side
    draw.rectangle([28, H//2, W-28, H-28], fill=(22, 18, 14))

    # Center divider
    draw.line([(60, H//2), (W-60, H//2)], fill=GOLD, width=2)

    # Labels top
    f_label = load_font("GeistMono-Regular.ttf", 14)
    f_cross = load_font("Italiana-Regular.ttf", 72)
    f_check = load_font("Italiana-Regular.ttf", 72)
    f_item  = load_font("InstrumentSans-Regular.ttf", 26)
    f_sm    = load_font("Jura-Light.ttf", 15)
    f_br    = load_font("ArsenalSC-Regular.ttf", 38)
    f_tag   = load_font("InstrumentSans-Regular.ttf", 22)
    f_head  = load_font("Italiana-Regular.ttf", 52)

    # TOP — importar (negativo)
    draw.text((80, 60), "IMPORTAR DESDE CHINA", font=f_label, fill=(80,70,60))
    negatives = ["1.000+ unidades mínimo", "60–90 días de espera", "Sin revisión de muestra", "Sin trato cercano"]
    for i, txt in enumerate(negatives):
        y = 120 + i * 82
        draw.text((80, y), "—", font=f_item, fill=RUST)
        draw.text((120, y), txt, font=f_item, fill=(160,148,130))

    # Diagonal ghost lines across top half
    for x in range(-200, W+200, 40):
        draw.line([(x, 28), (x+500, H//2)], fill=(25,20,16), width=1)

    # BOTTOM — KORMAN (positivo)
    draw.text((80, H//2 + 24), "KORMAN · CABA", font=f_label, fill=GOLD_DIM)
    positives = ["Pedidos chicos", "Plazos reales", "Muestra antes de producir", "Hablás con quien lo hace"]
    for i, txt in enumerate(positives):
        y = H//2 + 72 + i * 78
        # Gold checkmark — simple geometric
        cx_, cy_ = 94, y + 14
        draw.line([(cx_-10, cy_),(cx_-3, cy_+8)], fill=GOLD, width=2)
        draw.line([(cx_-3, cy_+8),(cx_+10, cy_-6)], fill=GOLD, width=2)
        draw.text((120, y), txt, font=f_item, fill=CREAM)

    # Stitch motif bottom-right
    for angle_deg in range(0, 360, 45):
        angle = math.radians(angle_deg)
        mx = W-110 + int(48 * math.cos(angle))
        my = H-120 + int(48 * math.sin(angle))
        draw_stitch(draw, mx, my, 7, GOLD_DIM, 1)
    draw_stitch(draw, W-110, H-120, 14, GOLD, 2)

    # Bottom left brand
    draw.line([(80, H-160), (460, H-160)], fill=GOLD_DIM, width=1)
    draw.text((80, H-130), "KORMAN", font=f_br, fill=CREAM)
    draw.text((80, H-82), "@kormanetiquetas", font=f_tag, fill=GOLD)

    draw.text((W-120, H-82), "04 · BA", font=f_sm, fill=GOLD_DIM)

    path = OUT + "korman-post-04-local-vs-china.png"
    img.save(path, "PNG", dpi=(300,300))
    print(f"Saved: {path}")

# ── Run all ───────────────────────────────────────────────────────────────────
post_02()
post_03()
post_04()
print("\nBatch completo — 3 posts generados.")
