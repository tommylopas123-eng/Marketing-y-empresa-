#!/usr/bin/env python3
"""
KORMAN Etiquetas Bordadas — Instagram Post Generator
Design philosophy: Hilo Nocturno
1080x1080px
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/.agents/design/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = (18, 16, 14)       # near-black, velvet depth
GOLD      = (198, 158, 86)     # aged gold thread
CREAM     = (235, 224, 200)    # linen cream
RUST      = (140, 80, 48)      # warm rust accent
CHARCOAL  = (38, 34, 30)       # slightly lighter than BG for subtle fields
GOLD_DIM  = (120, 95, 50)      # muted gold for fine patterns

def load_font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── 1. BACKGROUND FIELD — subtle warm gradient block ─────────────────────────
# Soft vignette: darken corners
for r in range(0, W//2, 2):
    alpha = int(30 * (r / (W//2)))
    c = tuple(max(0, v - alpha) for v in BG)

# ── 2. LOOM GRID — fine crosshatch bottom-right quadrant ─────────────────────
step = 18
for x in range(540, W, step):
    opacity = int(60 * ((x - 540) / 540))
    col = tuple(min(255, BG[i] + opacity) for i in range(3))
    draw.line([(x, 540), (x, H)], fill=(*GOLD_DIM[:3], 1), width=1)
for y in range(540, H, step):
    draw.line([(540, y), (W, y)], fill=GOLD_DIM, width=1)

# ── 3. THREAD LINES — diagonal fine lines across full canvas ─────────────────
for i in range(-H, W, 22):
    draw.line([(i, 0), (i + H, H)], fill=(40, 36, 30), width=1)

# ── 4. EMBROIDERY PATTERN — geometric motif, top-left anchor ─────────────────
# Diamond cross-stitch cluster
def draw_stitch(d, cx, cy, size, color, width=1):
    """Draw a single cross-stitch diamond"""
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    d.polygon(pts, outline=color, fill=None)
    d.line([(cx - size//2, cy - size//2), (cx + size//2, cy + size//2)], fill=color, width=width)
    d.line([(cx + size//2, cy - size//2), (cx - size//2, cy + size//2)], fill=color, width=width)

# Large decorative motif — left side, vertically centered
motif_x, motif_y = 155, 480
motif_size = 110

# Outer ring of stitches
for angle_deg in range(0, 360, 30):
    angle = math.radians(angle_deg)
    mx = motif_x + int(motif_size * math.cos(angle))
    my = motif_y + int(motif_size * math.sin(angle))
    draw_stitch(draw, mx, my, 8, GOLD_DIM, 1)

# Middle ring
for angle_deg in range(15, 360, 30):
    angle = math.radians(angle_deg)
    mx = motif_x + int((motif_size * 0.6) * math.cos(angle))
    my = motif_y + int((motif_size * 0.6) * math.sin(angle))
    draw_stitch(draw, mx, my, 5, GOLD, 1)

# Center cross
draw_stitch(draw, motif_x, motif_y, 18, GOLD, 2)
draw.ellipse([motif_x-4, motif_y-4, motif_x+4, motif_y+4], fill=GOLD)

# Outer circle trace
draw.ellipse(
    [motif_x - motif_size - 12, motif_y - motif_size - 12,
     motif_x + motif_size + 12, motif_y + motif_size + 12],
    outline=GOLD_DIM, width=1
)

# ── 5. REPEAT MINI STITCH PATTERN — scattered field, right side ──────────────
import random
random.seed(42)
for _ in range(80):
    rx = random.randint(580, 1020)
    ry = random.randint(60, 500)
    sz = random.randint(3, 9)
    alpha_factor = random.random() * 0.6 + 0.1
    col = tuple(int(GOLD_DIM[i] * alpha_factor) for i in range(3))
    draw_stitch(draw, rx, ry, sz, col, 1)

# ── 6. HORIZONTAL RULE — thin gold line dividing canvas thirds ───────────────
y_rule = 680
draw.line([(80, y_rule), (W - 80, y_rule)], fill=GOLD_DIM, width=1)

# Sub-rule, offset
draw.line([(80, y_rule + 6), (400, y_rule + 6)], fill=GOLD_DIM, width=1)

# ── 7. VERTICAL ACCENT LINE — left margin ─────────────────────────────────────
draw.line([(68, 80), (68, y_rule - 10)], fill=RUST, width=2)
draw.line([(64, 80), (72, 80)], fill=RUST, width=2)
draw.line([(64, y_rule - 10), (72, y_rule - 10)], fill=RUST, width=2)

# ── 8. TYPOGRAPHY ─────────────────────────────────────────────────────────────
# Main headline: "Tu marca," — Italiana (editorial serif)
f_headline   = load_font("Italiana-Regular.ttf", 112)
f_headline2  = load_font("Italiana-Regular.ttf", 112)
f_sub        = load_font("InstrumentSans-Regular.ttf", 28)
f_tag        = load_font("InstrumentSans-Regular.ttf", 22)
f_label      = load_font("Jura-Light.ttf", 16)

# "Tu marca," — top right area
tx1, ty1 = 520, 130
draw.text((tx1, ty1), "Tu marca,", font=f_headline, fill=CREAM)

# "bordada." — below, gold
tx2, ty2 = 520, 248
draw.text((tx2, ty2), "bordada.", font=f_headline2, fill=GOLD)

# Thin separator dots
for i in range(5):
    draw.ellipse([tx1 + i*22, ty2 + 128, tx1 + i*22 + 4, ty2 + 132], fill=GOLD_DIM)

# ── 9. BOTTOM BLOCK ──────────────────────────────────────────────────────────
# "KORMAN" — mono spaced, small caps feel
f_brand = load_font("ArsenalSC-Regular.ttf", 42)
draw.text((80, y_rule + 32), "KORMAN", font=f_brand, fill=CREAM)

# "ETIQUETAS BORDADAS" — tiny label
draw.text((80, y_rule + 84), "ETIQUETAS  BORDADAS", font=f_label, fill=GOLD_DIM)

# Handle @
draw.text((80, y_rule + 116), "@kormanetiquetas", font=f_tag, fill=GOLD)

# ── 10. CORNER MARKS — registration cross, bottom right ──────────────────────
cx_reg, cy_reg = W - 90, H - 90
r_reg = 12
draw.ellipse([cx_reg-r_reg, cy_reg-r_reg, cx_reg+r_reg, cy_reg+r_reg], outline=GOLD_DIM, width=1)
draw.line([(cx_reg - 20, cy_reg), (cx_reg + 20, cy_reg)], fill=GOLD_DIM, width=1)
draw.line([(cx_reg, cy_reg - 20), (cx_reg, cy_reg + 20)], fill=GOLD_DIM, width=1)

# Small coordinate label
draw.text((cx_reg - 28, cy_reg + 18), "01 · BA", font=f_label, fill=GOLD_DIM)

# ── 11. FINE MARGIN BORDER ────────────────────────────────────────────────────
margin = 28
draw.rectangle([margin, margin, W - margin, H - margin], outline=(45, 40, 35), width=1)

# ── SAVE ─────────────────────────────────────────────────────────────────────
out_path = OUT + "korman-post-01-tu-marca-bordada.png"
img.save(out_path, "PNG", dpi=(300, 300))
print(f"Saved: {out_path}")
print(f"Size: {img.size}")
