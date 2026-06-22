#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Portfolio de producción
PDF con todo lo generado: logos, posts, fotos procesadas.
"""
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, io

OUT   = "/home/user/Marketing-y-empresa-/docs-pdf/KORMAN-Portfolio-Produccion.pdf"
LOGO_DIR  = "/home/user/Marketing-y-empresa-/.agents/design/logo/"
POSTS_DIR = "/home/user/Marketing-y-empresa-/posts_v4/"
FOTOS_DIR = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"

W, H = A4  # 595 x 842 pts

BLACK  = (8/255,   8/255,   8/255)
WHITE  = (252/255, 250/255, 246/255)
GRAY   = (150/255, 148/255, 144/255)
DKGRAY = (50/255,  48/255,  44/255)

def pil_to_reader(path):
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf), img.size

def draw_page_header(c, title, subtitle=None, page_num=None):
    """Barra de cabecera negra en cada página."""
    c.setFillColorRGB(*BLACK)
    c.rect(0, H - 1.8*cm, W, 1.8*cm, fill=1, stroke=0)
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(1.2*cm, H - 1.1*cm, title.upper())
    if subtitle:
        c.setFont("Helvetica", 7)
        c.setFillColorRGB(*GRAY)
        c.drawString(1.2*cm, H - 1.55*cm, subtitle)
    if page_num:
        c.setFont("Helvetica", 7)
        c.setFillColorRGB(*GRAY)
        c.drawRightString(W - 1.2*cm, H - 1.1*cm, f"{page_num}")

def draw_section_label(c, text, y):
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(*GRAY)
    c.drawString(1.2*cm, y, text.upper())
    c.setStrokeColorRGB(*GRAY)
    c.setLineWidth(0.3)
    c.line(1.2*cm + c.stringWidth(text.upper(), "Helvetica", 7) + 6, y + 3,
           W - 1.2*cm, y + 3)

def fit_image(reader, img_size, max_w, max_h):
    """Escala imagen manteniendo aspecto dentro de max_w x max_h."""
    iw, ih = img_size
    scale = min(max_w / iw, max_h / ih)
    return iw * scale, ih * scale

c = rl_canvas.Canvas(OUT, pagesize=A4)

# ═══════════════════════════════════════════════════════════════════════════════
# PORTADA
# ═══════════════════════════════════════════════════════════════════════════════
c.setFillColorRGB(*BLACK)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Logo horizontal blanco centrado
logo_path = LOGO_DIR + "korman-logo-v2-horizontal-blanco.png"
reader, size = pil_to_reader(logo_path)
lw, lh = fit_image(reader, size, 12*cm, 4*cm)
c.drawImage(reader, (W - lw)/2, H/2 - lh/2 + 1.5*cm, lw, lh, mask="auto")

# Línea fina
c.setStrokeColorRGB(*DKGRAY)
c.setLineWidth(0.5)
c.line(2*cm, H/2 - 0.8*cm, W - 2*cm, H/2 - 0.8*cm)

# Subtítulo portada
c.setFillColorRGB(*GRAY)
c.setFont("Helvetica", 9)
txt = "PORTFOLIO DE PRODUCCIÓN  ·  IDENTIDAD VISUAL Y CONTENIDO DIGITAL"
c.drawCentredString(W/2, H/2 - 1.6*cm, txt)

c.setFont("Helvetica", 8)
c.drawCentredString(W/2, H/2 - 2.3*cm, "Buenos Aires  ·  desde 1980  ·  19.06.2026")

# Índice abajo
c.setFillColorRGB(*DKGRAY)
c.setFont("Helvetica-Bold", 7)
items = ["01  LOGOTIPO Y VERSIONES", "02  POSTS INSTAGRAM — TIPOS DE ETIQUETAS",
         "03  POSTS INSTAGRAM — HISTORIA", "04  FOTOS PROCESADAS — REFERENCIA"]
for i, item in enumerate(items):
    c.setFillColorRGB(*GRAY)
    c.drawCentredString(W/2, 3.5*cm - i*0.55*cm, item)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════════
# PÁG 2 — LOGOS (versiones)
# ═══════════════════════════════════════════════════════════════════════════════
draw_page_header(c, "KORMAN ETIQUETAS — Portfolio de Producción", "01 · Logotipo y versiones", "2")

logos = [
    (LOGO_DIR + "korman-logo-v2-horizontal-negro.png",  "Horizontal — fondo blanco",   (1, 1, 1)),
    (LOGO_DIR + "korman-logo-v2-horizontal-blanco.png", "Horizontal — fondo negro",    BLACK),
    (LOGO_DIR + "korman-logo-v2-avatar.png",            "Avatar Instagram / WhatsApp", (1, 1, 1)),
    (LOGO_DIR + "korman-watermark-negro.png",           "Watermark negro",             (0.92, 0.92, 0.9)),
    (LOGO_DIR + "korman-watermark-blanco.png",          "Watermark blanco",            BLACK),
]

y_start = H - 2.4*cm
draw_section_label(c, "Versiones del logotipo aprobado", y_start - 0.5*cm)

y = y_start - 1.2*cm
for i, (path, label, bg) in enumerate(logos):
    if not os.path.exists(path):
        continue
    row = i % 2
    col = i // 2 if i < 4 else 0
    # Layout: 2 columnas para los 2 primeros, luego centrado
    box_w = (W - 3.2*cm) / 2
    box_h = 5.5*cm

    if i < 4:
        x = 1.2*cm + col * (box_w + 0.8*cm)
        by = y - (row * (box_h + 1.0*cm))
    else:
        x = (W - box_w) / 2
        by = y - 2 * (box_h + 1.0*cm)

    # Fondo del cuadro
    c.setFillColorRGB(*bg)
    c.roundRect(x, by - box_h, box_w, box_h, 4, fill=1, stroke=0)

    # Imagen
    reader, size = pil_to_reader(path)
    iw, ih = fit_image(reader, size, box_w - 1.2*cm, box_h - 1.4*cm)
    ix = x + (box_w - iw) / 2
    iy = by - box_h + (box_h - ih) / 2 + 0.3*cm
    c.drawImage(reader, ix, iy, iw, ih, mask="auto")

    # Label
    label_color = WHITE if bg == BLACK or bg == (0,0,0) else GRAY
    c.setFillColorRGB(*GRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + box_w/2, by - box_h - 0.4*cm, label)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════════
# PÁG 3 — POSTS TIPOS DE ETIQUETAS (2x2)
# ═══════════════════════════════════════════════════════════════════════════════
draw_page_header(c, "KORMAN ETIQUETAS — Portfolio de Producción",
                 "02 · Posts Instagram — Serie: Tipos de etiquetas bordadas", "3")

posts_serie1 = [
    (POSTS_DIR + "01-tafeta.png",          "01 · TAFETA",          "Económica · para etiquetas internas"),
    (POSTS_DIR + "02-alta-definicion.png", "02 · ALTA DEFINICIÓN", "Nítida · colores intensos · la más elegida"),
    (POSTS_DIR + "03-triple-densidad.png", "03 · TRIPLE DENSIDAD", "Mayor relieve · presencia · efecto premium"),
    (POSTS_DIR + "04-texturada.png",       "04 · TEXTURADA",       "Relieve especial · para marcas que se diferencian"),
]

draw_section_label(c, "Serie: Tipos de etiquetas bordadas", H - 2.4*cm - 0.5*cm)

cols = 2
box_w = (W - 3.2*cm) / cols
box_h = box_w  # cuadrado 1:1

y_top = H - 3.2*cm

for i, (path, title, subtitle) in enumerate(posts_serie1):
    col = i % cols
    row = i // cols
    x = 1.2*cm + col * (box_w + 0.8*cm)
    y = y_top - row * (box_h + 1.4*cm)

    if os.path.exists(path):
        reader, size = pil_to_reader(path)
        iw, ih = fit_image(reader, size, box_w, box_h)
        c.drawImage(reader, x + (box_w - iw)/2, y - ih, iw, ih)

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColorRGB(*BLACK)
    c.drawString(x, y - box_h - 0.45*cm, title)
    c.setFont("Helvetica", 6.5)
    c.setFillColorRGB(*GRAY)
    c.drawString(x, y - box_h - 0.85*cm, subtitle)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════════
# PÁG 4 — POSTS HISTORIA (2 posts + descripción)
# ═══════════════════════════════════════════════════════════════════════════════
draw_page_header(c, "KORMAN ETIQUETAS — Portfolio de Producción",
                 "03 · Posts Instagram — Serie: Historia", "4")

posts_historia = [
    (POSTS_DIR + "05-historia-1980.png", "05 · 1980",    "Así empezó KORMAN ETIQUETAS en Buenos Aires"),
    (POSTS_DIR + "06-historia-46-anos.png", "06 · 46 AÑOS", "El mismo oficio · la misma dedicación"),
]

draw_section_label(c, "Serie: Historia de la empresa", H - 2.4*cm - 0.5*cm)

box_w = (W - 3.2*cm) / 2
box_h = box_w
y_top = H - 3.2*cm

for i, (path, title, subtitle) in enumerate(posts_historia):
    x = 1.2*cm + i * (box_w + 0.8*cm)
    if os.path.exists(path):
        reader, size = pil_to_reader(path)
        iw, ih = fit_image(reader, size, box_w, box_h)
        c.drawImage(reader, x + (box_w - iw)/2, y_top - ih, iw, ih)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColorRGB(*BLACK)
    c.drawString(x, y_top - box_h - 0.45*cm, title)
    c.setFont("Helvetica", 6.5)
    c.setFillColorRGB(*GRAY)
    c.drawString(x, y_top - box_h - 0.85*cm, subtitle)

# Nota de diseño
note_y = y_top - box_h - 2.2*cm
draw_section_label(c, "Filosofía de diseño aplicada", note_y)
note_y -= 0.8*cm
c.setFont("Helvetica", 8)
c.setFillColorRGB(*DKGRAY)
notas = [
    "Filosofía: «Silencio Textil» — inspirada en Toteme, COS, The Row.",
    "Paleta: negro profundo #080808 · blanco roto #FCFAF6 · gris cálido #969490.",
    "Tipografía: BricolageGrotesque Bold (títulos) + InstrumentSans Regular (subtítulos).",
    "Estructura: texto en zona superior · foto/etiqueta en zona inferior.",
    "Reglas de contenido: títulos en MAYÚSCULAS · sin puntos · una idea por post.",
    "Pendiente: incorporar foto real de etiqueta en cada post (Tommy confirma cuál va en cada uno).",
]
for nota in notas:
    c.drawString(1.2*cm, note_y, f"·  {nota}")
    note_y -= 0.5*cm

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════════
# PÁG 5 — FOTOS PROCESADAS (3x2)
# ═══════════════════════════════════════════════════════════════════════════════
draw_page_header(c, "KORMAN ETIQUETAS — Portfolio de Producción",
                 "04 · Fotos procesadas — Etiquetas de referencia (fondo removido)", "5")

fotos = [
    (FOTOS_DIR + "beditorial-editorial-negro.jpg",  "Beditorial"),
    (FOTOS_DIR + "givenchy-denim-negro.jpg",        "Givenchy"),
    (FOTOS_DIR + "balmain-cadena-negro.jpg",        "Balmain"),
    (FOTOS_DIR + "tough-jeansmith-negro.jpg",       "Tough Jeansmith"),
    (FOTOS_DIR + "pierre-cardin-negro.jpg",         "Pierre Cardin"),
    (FOTOS_DIR + "elmo-dorada-negro.jpg",           "Elmo — hilo dorado"),
]

draw_section_label(c, "Las 6 mejores — fondo negro KORMAN", H - 2.4*cm - 0.5*cm)

cols = 3
box_w = (W - (cols + 1) * 0.7*cm) / cols
box_h = box_w
y_top = H - 3.2*cm

for i, (path, label) in enumerate(fotos):
    col = i % cols
    row = i // cols
    x = 0.7*cm + col * (box_w + 0.7*cm)
    y = y_top - row * (box_h + 1.0*cm)

    if os.path.exists(path):
        reader, size = pil_to_reader(path)
        iw, ih = fit_image(reader, size, box_w, box_h)
        c.drawImage(reader, x + (box_w - iw)/2, y - ih, iw, ih)

    c.setFont("Helvetica", 6.5)
    c.setFillColorRGB(*GRAY)
    c.drawCentredString(x + box_w/2, y - box_h - 0.35*cm, label)

c.showPage()

c.save()
print(f"✓  Portfolio generado: {OUT}")
