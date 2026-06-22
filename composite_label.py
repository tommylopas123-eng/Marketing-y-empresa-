#!/usr/bin/env python3
"""
Composite Givenchy embroidered label onto the boutique photo,
replacing the "Docena Portartilleria" label.

Usage:
  python composite_label.py

Inputs:
  assets/boutique-denim.jpg          (la foto que mandaste de Higgsfield)
  assets/fotos-procesadas/givenchy-denim-transparente.png  (etiqueta Givenchy)

Output:
  assets/boutique-givenchy-composite.jpg
"""

from PIL import Image, ImageEnhance
import numpy as np

# ─── Load ───────────────────────────────────────────────────────────────────
bg_path = "assets/boutique-denim.jpg"
label_path = "assets/fotos-procesadas/givenchy-denim-transparente.png"

bg = Image.open(bg_path).convert("RGBA")
label = Image.open(label_path).convert("RGBA")

bg_w, bg_h = bg.size
print(f"Background: {bg_w}x{bg_h}")
print(f"Label original: {label.size}")

# ─── Target region ──────────────────────────────────────────────────────────
# The "Docena Portartilleria" label bounding box in the photo
# (measured at 828x1472 native resolution)
# Adjust these if the output looks off
TARGET_LEFT   = 248
TARGET_TOP    = 518
TARGET_RIGHT  = 518
TARGET_BOTTOM = 775

target_w = TARGET_RIGHT - TARGET_LEFT   # ~270
target_h = TARGET_BOTTOM - TARGET_TOP   # ~257

# Scale target to actual image size (in case it was resized)
scale_x = bg_w / 828
scale_y = bg_h / 1472

tl = int(TARGET_LEFT   * scale_x)
tt = int(TARGET_TOP    * scale_y)
tr = int(TARGET_RIGHT  * scale_x)
tb = int(TARGET_BOTTOM * scale_y)
tw = tr - tl
th = tb - tt

print(f"Target box: ({tl},{tt}) -> ({tr},{tb})  [{tw}x{th}]")

# ─── Resize label to fit the target box ─────────────────────────────────────
label_aspect = label.width / label.height  # ~1.26  (wider than tall)

# Fit label inside target maintaining aspect ratio — fill width
new_w = tw
new_h = int(new_w / label_aspect)

if new_h > th:
    new_h = th
    new_w = int(new_h * label_aspect)

label_resized = label.resize((new_w, new_h), Image.LANCZOS)
print(f"Label resized to: {new_w}x{new_h}")

# ─── Slightly darken the label to match ambient light of the scene ───────────
# The boutique photo is fairly dark/moody; a pure-white label would pop too much
label_r, label_g, label_b, label_a = label_resized.split()
label_rgb = Image.merge("RGB", (label_r, label_g, label_b))
label_rgb = ImageEnhance.Brightness(label_rgb).enhance(0.88)
label_r, label_g, label_b = label_rgb.split()
label_resized = Image.merge("RGBA", (label_r, label_g, label_b, label_a))

# ─── Center label inside the target box ─────────────────────────────────────
paste_x = tl + (tw - new_w) // 2
paste_y = tt + (th - new_h) // 2

# ─── Paste with alpha mask ───────────────────────────────────────────────────
# First paint a white rectangle to cover the original label
white_rect = Image.new("RGBA", (tw, th), (240, 238, 232, 255))
bg.paste(white_rect, (tl, tt))

# Then paste the Givenchy label on top
bg.paste(label_resized, (paste_x, paste_y), label_resized)

# ─── Save ────────────────────────────────────────────────────────────────────
out = bg.convert("RGB")
out_path = "assets/boutique-givenchy-composite.jpg"
out.save(out_path, quality=95)
print(f"\n✓ Guardado: {out_path}")
print(f"  Abrir con: start {out_path}")
