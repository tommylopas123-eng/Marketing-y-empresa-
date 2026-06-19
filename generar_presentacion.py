#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Presentación ejecutiva para el dueño.
PDF de alta calidad tipo agencia: estrategia, identidad, contenido, próximos pasos.
"""
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io, os

OUT      = "/home/user/Marketing-y-empresa-/docs-pdf/KORMAN-Presentacion-Ejecutiva.pdf"
LOGO_DIR = "/home/user/Marketing-y-empresa-/.agents/design/logo/"
POSTS    = "/home/user/Marketing-y-empresa-/posts_v4/"
FOTOS    = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"

W, H = A4

# Paleta
BK  = (8/255,   8/255,   8/255)
WH  = (252/255, 250/255, 246/255)
GR  = (140/255, 138/255, 134/255)
DG  = (55/255,  53/255,  49/255)
AC  = (200/255, 195/255, 185/255)   # acento crema

def pil_img(path, max_w_cm, max_h_cm):
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    reader = ImageReader(buf)
    iw, ih = img.size
    mw, mh = max_w_cm * cm, max_h_cm * cm
    scale = min(mw / iw, mh / ih)
    return reader, iw * scale, ih * scale

def fill_page(c, color=BK):
    c.setFillColorRGB(*color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def hline(c, y, x0=1.5*cm, x1=None, color=DG, w=0.4):
    if x1 is None: x1 = W - 1.5*cm
    c.setStrokeColorRGB(*color)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)

def label(c, text, x, y, size=7, color=GR, font="Helvetica", tracking=False):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    if tracking:
        # Simular tracking espaciando manualmente
        cx = x
        for ch in text:
            c.drawString(cx, y, ch)
            cx += c.stringWidth(ch, font, size) + 1.2
    else:
        c.drawString(x, y, text)

def title(c, text, x, y, size=28, color=WH, font="Helvetica-Bold"):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text)

def body(c, text, x, y, size=9.5, color=WH, font="Helvetica", max_w=None):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    if max_w:
        # Wrap manual simple
        words = text.split()
        line = ""
        cy = y
        for w_word in words:
            test = (line + " " + w_word).strip()
            if c.stringWidth(test, font, size) < max_w:
                line = test
            else:
                c.drawString(x, cy, line)
                cy -= size * 1.6
                line = w_word
        if line:
            c.drawString(x, cy, line)
        return cy
    else:
        c.drawString(x, y, text)
        return y

def bullet(c, items, x, y, size=9, color=WH, gap=0.52*cm):
    c.setFont("Helvetica", size)
    c.setFillColorRGB(*color)
    for item in items:
        c.drawString(x, y, f"·  {item}")
        y -= gap
    return y

def num_box(c, num, x, y, size=2.2*cm):
    c.setFillColorRGB(*DG)
    c.rect(x, y - size, size, size, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 22)
    c.setFillColorRGB(*AC)
    c.drawCentredString(x + size/2, y - size/2 - 7, num)

def section_header(c, num, titulo, subtitulo, bg=BK):
    fill_page(c, bg)
    # Franja lateral izquierda
    c.setFillColorRGB(*DG)
    c.rect(0, 0, 0.6*cm, H, fill=1, stroke=0)
    # Número grande fantasma
    c.setFont("Helvetica-Bold", 160)
    c.setFillColorRGB(18/255, 16/255, 14/255)
    c.drawString(1.8*cm, H/2 - 5*cm, num)
    # Título
    c.setFont("Helvetica-Bold", 30)
    c.setFillColorRGB(*WH)
    c.drawString(1.8*cm, H/2 + 0.8*cm, titulo.upper())
    hline(c, H/2 - 0.1*cm, x0=1.8*cm, color=AC, w=1.5)
    # Subtítulo
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(*GR)
    c.drawString(1.8*cm, H/2 - 0.9*cm, subtitulo)


c = rl_canvas.Canvas(OUT, pagesize=A4)

# ══════════════════════════════════════════════════════
# PORTADA
# ══════════════════════════════════════════════════════
fill_page(c, BK)

# Franja crema superior delgada
c.setFillColorRGB(*AC)
c.rect(0, H - 0.4*cm, W, 0.4*cm, fill=1, stroke=0)

# Logo
logo = LOGO_DIR + "korman-logo-v2-horizontal-blanco.png"
r, lw, lh = pil_img(logo, 11, 3.5)
c.drawImage(r, (W - lw)/2, H*0.62, lw, lh, mask="auto")

# Línea bajo logo
hline(c, H*0.58, x0=3*cm, x1=W-3*cm, color=DG, w=0.6)

# Tagline principal
c.setFont("Helvetica", 11)
c.setFillColorRGB(*GR)
c.drawCentredString(W/2, H*0.54, "ESTRATEGIA DE MARKETING DIGITAL")

c.setFont("Helvetica-Bold", 13)
c.setFillColorRGB(*WH)
c.drawCentredString(W/2, H*0.49, "PLAN DE CONTENIDO E IDENTIDAD VISUAL")

hline(c, H*0.46, x0=4*cm, x1=W-4*cm, color=DG)

# Datos
datos = [
    ("EMPRESA", "KORMAN Etiquetas Bordadas"),
    ("UBICACIÓN", "Colegiales, Buenos Aires"),
    ("FUNDACIÓN", "1980  ·  46 años de trayectoria"),
    ("FECHA", "Junio 2026"),
]
y_d = H*0.41
for k, v in datos:
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(*GR)
    c.drawCentredString(W/2 - 1*cm, y_d, k)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(*WH)
    c.drawString(W/2 - 0.2*cm, y_d, v)
    y_d -= 0.65*cm

# Franja crema inferior
c.setFillColorRGB(*DG)
c.rect(0, 0, W, 2.8*cm, fill=1, stroke=0)
c.setFont("Helvetica", 7.5)
c.setFillColorRGB(*AC)
c.drawCentredString(W/2, 1.6*cm, "CONFIDENCIAL  ·  USO INTERNO  ·  KORMAN ETIQUETAS BORDADAS")
c.setFont("Helvetica", 7)
c.setFillColorRGB(*GR)
c.drawCentredString(W/2, 0.9*cm, "Instagram: @kormanetiquetas  ·  WhatsApp: +54 9 11 4475-6233")

c.showPage()

# ══════════════════════════════════════════════════════
# ÍNDICE
# ══════════════════════════════════════════════════════
fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-3*cm, W, 3*cm, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 9)
c.setFillColorRGB(*AC)
label(c, "CONTENIDO DE ESTA PRESENTACIÓN", 1.8*cm, H - 1.6*cm, size=9, color=AC, font="Helvetica-Bold", tracking=True)
hline(c, H - 3*cm, color=AC, w=0.5)

secciones = [
    ("01", "LA EMPRESA",         "Quiénes somos, qué fabricamos, nuestra historia"),
    ("02", "EL MERCADO",         "Competencia, oportunidades y posicionamiento estratégico"),
    ("03", "IDENTIDAD VISUAL",   "Logo aprobado, paleta de colores, tipografía, filosofía de diseño"),
    ("04", "CONTENIDO DIGITAL",  "Posts de Instagram producidos — series y estrategia"),
    ("05", "BANCO DE FOTOS",     "37 fotos de etiquetas reales procesadas profesionalmente"),
    ("06", "PLAN DE ACCIÓN",     "Pasos concretos: Instagram, WhatsApp Business, próximos contenidos"),
]

y = H - 4.2*cm
for num, sec, desc in secciones:
    num_box(c, num, 1.8*cm, y + 0.6*cm)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(*WH)
    c.drawString(4.6*cm, y + 0.1*cm, sec)
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*GR)
    c.drawString(4.6*cm, y - 0.5*cm, desc)
    hline(c, y - 1.0*cm, x0=1.8*cm, color=DG)
    y -= 2.1*cm

c.showPage()

# ══════════════════════════════════════════════════════
# 01 — LA EMPRESA
# ══════════════════════════════════════════════════════
section_header(c, "01", "La Empresa", "Historia, producto y capacidad de producción")
c.showPage()

fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-2*cm, W, 2*cm, fill=1, stroke=0)
label(c, "01  ·  LA EMPRESA", 1.5*cm, H-1.2*cm, size=8, color=AC, font="Helvetica-Bold")

# Col izquierda
cx = 1.5*cm
cy = H - 3.0*cm

label(c, "QUIÉNES SOMOS", cx, cy, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, cy - 0.3*cm, x0=cx, x1=10*cm, color=DG)
cy -= 0.9*cm

textos = [
    "KORMAN Etiquetas Bordadas es una empresa familiar argentina",
    "con 46 años de trayectoria en la fabricación de etiquetas",
    "bordadas personalizadas para marcas de ropa.",
    "",
    "Fundada en 1980 en Buenos Aires, combina décadas de",
    "experiencia artesanal con maquinaria suiza de última",
    "generación para ofrecer etiquetas de nivel internacional.",
]
for t in textos:
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*WH if t else GR)
    c.drawString(cx, cy, t)
    cy -= 0.48*cm

cy -= 0.4*cm
label(c, "DATOS CLAVE", cx, cy, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, cy - 0.3*cm, x0=cx, x1=10*cm, color=DG)
cy -= 0.9*cm

datos2 = [
    ("Fundación", "1980 — Buenos Aires"),
    ("Trayectoria", "46 años en el rubro"),
    ("Ubicación", "Colegiales, CABA"),
    ("Distribución", "Todo el país"),
    ("Maquinaria", "Suiza de alta tecnología"),
    ("Terminaciones", "Soldado, doblado, apresto"),
    ("Plazo entrega", "15 a 20 días hábiles"),
    ("Instagram", "@kormanetiquetas"),
    ("WhatsApp", "+54 9 11 4475-6233"),
]
for k, v in datos2:
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColorRGB(*GR)
    c.drawString(cx, cy, k + ":")
    c.setFont("Helvetica", 8.5)
    c.setFillColorRGB(*WH)
    c.drawString(cx + 3.2*cm, cy, v)
    cy -= 0.55*cm

# Col derecha — tipos de etiqueta
rx = 10.5*cm
ry = H - 3.0*cm
label(c, "TIPOS DE ETIQUETA BORDADA", rx, ry, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, ry - 0.3*cm, x0=rx, x1=W-1.5*cm, color=DG)
ry -= 0.9*cm

tipos = [
    ("TAFETA",           "La más económica. Ideal para etiquetas internas,\ntalles y cuidado de prendas. Menor resolución."),
    ("ALTA DEFINICIÓN",  "La más elegida. Doble densidad de pasadas,\ncolores intensos y nítidos. Relación precio/calidad óptima."),
    ("TRIPLE DENSIDAD",  "Mayor volumen y relieve. Efecto premium visible.\nIdeal para logos con detalle y marcas que buscan destacar."),
    ("TEXTURADA",        "La más exclusiva. Relieve y textura especial.\nPara marcas de nivel muy premium."),
]
for nombre, desc in tipos:
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(*WH)
    c.drawString(rx, ry, nombre)
    ry -= 0.42*cm
    for linea in desc.split("\n"):
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(*GR)
        c.drawString(rx, ry, linea)
        ry -= 0.42*cm
    ry -= 0.3*cm

label(c, "PROCESO DE PEDIDO", rx, ry - 0.1*cm, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, ry - 0.4*cm, x0=rx, x1=W-1.5*cm, color=DG)
ry -= 1.0*cm
pasos = ["1. Cliente envía logo o diseño",
         "2. KORMAN produce boceto digital a escala real",
         "3. Cliente aprueba el boceto",
         "4. Producción en 15 a 20 días hábiles",
         "5. Entrega con terminación y apresto incluidos"]
for p in pasos:
    c.setFont("Helvetica", 8.5)
    c.setFillColorRGB(*WH)
    c.drawString(rx, ry, p)
    ry -= 0.5*cm

hline(c, 1.5*cm, color=DG)
label(c, "POLÍTICA DE PRECIOS: El precio varía según diseño, tipo de tejido, tamaño, terminación y cantidad. No se publica precio. Toda consulta se cotiza individualmente por WhatsApp.", 1.5*cm, 0.9*cm, size=7, color=GR)
c.showPage()

# ══════════════════════════════════════════════════════
# 02 — EL MERCADO
# ══════════════════════════════════════════════════════
section_header(c, "02", "El Mercado", "Competencia, posicionamiento y oportunidad")
c.showPage()

fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-2*cm, W, 2*cm, fill=1, stroke=0)
label(c, "02  ·  EL MERCADO", 1.5*cm, H-1.2*cm, size=8, color=AC, font="Helvetica-Bold")

cy = H - 3.0*cm
label(c, "COMPETIDORES ANALIZADOS", 1.5*cm, cy, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, cy - 0.3*cm, color=DG)
cy -= 0.9*cm

competidores = [
    ("PRINTMAX SRL",    "printmax.com.ar",   "Marca consolidada, gama amplia",           "Sin Instagram activo, foco industrial, no atiende emprendedores"),
    ("BESTLABELS",      "bestlabels.ar",      "Precio visible online, mínimo 100 unidades", "Internacional, sin producción local, sin asesoramiento personalizado"),
    ("CHINA (import.)", "—",                  "Precio bajo por unidad en grandes cantidades", "Mínimo 500–1000 u., 60–90 días demora, riesgo de calidad, sin muestra"),
    ("INFORMALES IG",   "Varios perfiles",    "Precio bajo, respuesta rápida",             "Mínimos en metros (400–500m), calidad variable, sin garantía de plazo"),
]

for nombre, url, fortaleza, debilidad in competidores:
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(*WH)
    c.drawString(1.5*cm, cy, nombre)
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(*GR)
    c.drawString(1.5*cm, cy - 0.45*cm, f"+ {fortaleza}")
    c.setFillColorRGB(180/255, 100/255, 90/255)
    c.drawString(1.5*cm, cy - 0.88*cm, f"– {debilidad}")
    hline(c, cy - 1.2*cm, color=DG)
    cy -= 1.55*cm

cy -= 0.2*cm
label(c, "NUESTRA VENTAJA COMPETITIVA", 1.5*cm, cy, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, cy - 0.3*cm, color=DG)
cy -= 0.9*cm

ventajas = [
    "46 años de experiencia — nadie en el mercado tiene esa trayectoria",
    "Maquinaria suiza de alta tecnología — calidad de nivel internacional",
    "Sin mínimos altos — trabajamos con marcas que arrancan",
    "Boceto digital aprobado antes de producir — cero sorpresas",
    "Entrega en 15–20 días — vs. 60–90 días de China",
    "Producción local en CABA — Industria Argentina",
    "Asesoramiento personalizado — no somos un e-commerce frío",
]
for v in ventajas:
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*WH)
    c.drawString(1.5*cm, cy, f"✓  {v}")
    cy -= 0.52*cm

cy -= 0.4*cm
label(c, "CLIENTE OBJETIVO", 1.5*cm, cy, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, cy - 0.3*cm, color=DG)
cy -= 0.9*cm

clientes = [
    "Emprendedoras de moda y marcas de ropa emergentes en CABA y GBA",
    "Diseñadoras independientes que buscan etiquetas para su primera colección",
    "Marcas consolidadas que quieren mejorar la calidad de su etiqueta actual",
    "Marcas de niños y bebé (línea especial con colores suaves y diseños tiernos)",
    "Empresas que necesitan etiquetas de talle, cuidado o instrucciones de lavado",
]
for cl in clientes:
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*GR)
    c.drawString(1.5*cm, cy, f"·  {cl}")
    cy -= 0.52*cm

hline(c, 1.5*cm, color=DG)
label(c, "Análisis realizado con Firecrawl (scraping real de sitios de competidores) — Junio 2026", 1.5*cm, 0.9*cm, size=7, color=GR)
c.showPage()

# ══════════════════════════════════════════════════════
# 03 — IDENTIDAD VISUAL
# ══════════════════════════════════════════════════════
section_header(c, "03", "Identidad Visual", "Logo, paleta, tipografía y filosofía de diseño")
c.showPage()

fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-2*cm, W, 2*cm, fill=1, stroke=0)
label(c, "03  ·  IDENTIDAD VISUAL — LOGO APROBADO", 1.5*cm, H-1.2*cm, size=8, color=AC, font="Helvetica-Bold")

# Logo horizontal negro (sobre fondo crema)
lp = LOGO_DIR + "korman-logo-v2-horizontal-negro.png"
r, lw, lh = pil_img(lp, 9, 3)
bg_x, bg_y = 1.5*cm, H - 5.5*cm
bg_w, bg_h = lw + 2*cm, lh + 1.6*cm
c.setFillColorRGB(*WH)
c.rect(bg_x, bg_y, bg_w, bg_h, fill=1, stroke=0)
c.drawImage(r, bg_x + (bg_w-lw)/2, bg_y + (bg_h-lh)/2, lw, lh, mask="auto")

# Logo horizontal blanco
lp2 = LOGO_DIR + "korman-logo-v2-horizontal-blanco.png"
r2, lw2, lh2 = pil_img(lp2, 9, 3)
bg2_x = bg_x + bg_w + 0.6*cm
c.setFillColorRGB(*BK)
c.setStrokeColorRGB(*DG)
c.setLineWidth(0.5)
c.rect(bg2_x, bg_y, bg_w, bg_h, fill=1, stroke=1)
c.drawImage(r2, bg2_x + (bg_w-lw2)/2, bg_y + (bg_h-lh2)/2, lw2, lh2, mask="auto")

# Avatar
lp3 = LOGO_DIR + "korman-logo-v2-avatar.png"
r3, lw3, lh3 = pil_img(lp3, 3, 3)
av_size = 2.8*cm
av_x = bg2_x + bg_w + 0.6*cm
av_y = bg_y + (bg_h - av_size)/2
c.setFillColorRGB(*WH)
c.circle(av_x + av_size/2, av_y + av_size/2, av_size/2, fill=1, stroke=0)
c.drawImage(r3, av_x, av_y, av_size, av_size, mask="auto")

labels_logo = [
    (bg_x + bg_w/2, bg_y - 0.5*cm, "Versión negra — web y documentos"),
    (bg2_x + bg_w/2, bg_y - 0.5*cm, "Versión blanca — Instagram y fondos oscuros"),
    (av_x + av_size/2, bg_y - 0.5*cm, "Avatar"),
]
for lx, ly, lt in labels_logo:
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(*GR)
    c.drawCentredString(lx, ly, lt)

# Paleta
py = bg_y - 2.0*cm
label(c, "PALETA DE COLORES", 1.5*cm, py, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, py - 0.3*cm, color=DG)
py -= 1.0*cm

paleta = [
    ((8/255, 8/255, 8/255),     "#080808", "Negro profundo", "Fondo principal"),
    ((252/255, 250/255, 246/255), "#FCFAF6", "Blanco roto",  "Texto principal"),
    ((150/255, 148/255, 144/255), "#969490", "Gris cálido",  "Subtítulos y labels"),
    ((55/255, 53/255, 49/255),   "#373531", "Gris oscuro",   "Separadores y detalles"),
]
sw = 2.4*cm
sh = 1.4*cm
px_start = 1.5*cm
for i, (rgb, hex_code, name, use) in enumerate(paleta):
    px = px_start + i * (sw + 0.4*cm)
    c.setFillColorRGB(*rgb)
    if rgb == (252/255, 250/255, 246/255):
        c.setStrokeColorRGB(*DG)
        c.setLineWidth(0.3)
        c.rect(px, py - sh, sw, sh, fill=1, stroke=1)
    else:
        c.rect(px, py - sh, sw, sh, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColorRGB(*GR)
    c.drawString(px, py - sh - 0.45*cm, hex_code)
    c.setFont("Helvetica", 6.5)
    c.drawString(px, py - sh - 0.85*cm, name)
    c.setFont("Helvetica", 6)
    c.drawString(px, py - sh - 1.2*cm, use)

# Tipografía
ty = py - sh - 2.2*cm
label(c, "TIPOGRAFÍA", 1.5*cm, ty, size=7.5, color=AC, font="Helvetica-Bold")
hline(c, ty - 0.3*cm, color=DG)
ty -= 0.9*cm

tipos_typo = [
    ("Helvetica-Bold",    36, "ABCDEFG", "BricolageGrotesque Bold", "Títulos de posts · Logo"),
    ("Helvetica",         20, "ABCDEFGHIJ", "InstrumentSans Regular", "Subtítulos · Cuerpo de texto"),
    ("Helvetica-Oblique", 14, "ABCDEFGHIJKLM", "Jura Light", "Labels · Marcas de sección"),
]
for font_sim, size, sample, real_name, uso in tipos_typo:
    c.setFont(font_sim, size)
    c.setFillColorRGB(*WH)
    c.drawString(1.5*cm, ty, sample)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColorRGB(*AC)
    c.drawString(10*cm, ty + size*0.25, real_name)
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(*GR)
    c.drawString(10*cm, ty + size*0.25 - 0.45*cm, uso)
    ty -= size * 0.6 + 0.5*cm

hline(c, ty - 0.3*cm, color=DG)
ty -= 0.8*cm
label(c, "FILOSOFÍA: «Silencio Textil» — inspirada en Toteme, COS, The Row. Espacio como material. Autoridad tipográfica. Museo.", 1.5*cm, ty, size=7.5, color=GR)
c.showPage()

# ══════════════════════════════════════════════════════
# 04 — CONTENIDO DIGITAL
# ══════════════════════════════════════════════════════
section_header(c, "04", "Contenido Digital", "Posts de Instagram producidos y estrategia de publicación")
c.showPage()

fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-2*cm, W, 2*cm, fill=1, stroke=0)
label(c, "04  ·  CONTENIDO DIGITAL — POSTS INSTAGRAM (6 PRODUCIDOS)", 1.5*cm, H-1.2*cm, size=8, color=AC, font="Helvetica-Bold")

posts_data = [
    (POSTS+"01-tafeta.png",          "TAFETA",          "ETIQUETA BORDADA · 01", "Económica · para etiquetas internas"),
    (POSTS+"02-alta-definicion.png", "ALTA DEFINICIÓN", "ETIQUETA BORDADA · 02", "Nítida · colores intensos · la más elegida"),
    (POSTS+"03-triple-densidad.png", "TRIPLE DENSIDAD", "ETIQUETA BORDADA · 03", "Mayor relieve · presencia · efecto premium"),
    (POSTS+"04-texturada.png",       "TEXTURADA",       "ETIQUETA BORDADA · 04", "Relieve especial · para marcas que se diferencian"),
    (POSTS+"05-historia-1980.png",   "1980",            "HISTORIA · 01",         "Así empezó KORMAN ETIQUETAS en Buenos Aires"),
    (POSTS+"06-historia-46-anos.png","46 AÑOS",         "HISTORIA · 02",         "El mismo oficio · la misma dedicación"),
]

cols = 3
pw = (W - 1.5*cm - 0.5*cm*cols) / cols
ph = pw
y_top = H - 2.6*cm

for i, (path, tit, lbl, sub) in enumerate(posts_data):
    col = i % cols
    row = i // cols
    px = 0.8*cm + col * (pw + 0.5*cm)
    py2 = y_top - row * (ph + 1.5*cm)
    if os.path.exists(path):
        r, iw, ih = pil_img(path, pw/cm, ph/cm)
        c.drawImage(r, px, py2 - ih, iw, ih)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColorRGB(*WH)
    c.drawString(px, py2 - ph - 0.38*cm, tit)
    c.setFont("Helvetica", 6)
    c.setFillColorRGB(*GR)
    c.drawString(px, py2 - ph - 0.72*cm, sub)

# Nota
ny = y_top - 2*(ph + 1.5*cm) - 0.5*cm
hline(c, ny, color=DG)
ny -= 0.6*cm
notas_p = [
    "·  Formato: 1080 × 1080 px · 300 dpi · PNG de alta calidad",
    "·  Pendiente: incorporar foto real de etiqueta en cada post (Tommy confirma cuál va en cada uno)",
    "·  Cada post tiene caption listo con hashtags para copiar y pegar al publicar",
]
for n in notas_p:
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(*GR)
    c.drawString(1.5*cm, ny, n)
    ny -= 0.48*cm

c.showPage()

# ══════════════════════════════════════════════════════
# 05 — BANCO DE FOTOS
# ══════════════════════════════════════════════════════
section_header(c, "05", "Banco de Fotos", "37 fotos de etiquetas reales procesadas profesionalmente")
c.showPage()

fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-2*cm, W, 2*cm, fill=1, stroke=0)
label(c, "05  ·  BANCO DE FOTOS PROCESADAS — LAS 8 MEJORES", 1.5*cm, H-1.2*cm, size=8, color=AC, font="Helvetica-Bold")

mejores = [
    (FOTOS+"beditorial-editorial-negro.jpg", "Beditorial"),
    (FOTOS+"givenchy-denim-negro.jpg",       "Givenchy"),
    (FOTOS+"balmain-cadena-negro.jpg",       "Balmain"),
    (FOTOS+"tough-jeansmith-negro.jpg",      "Tough Jeansmith"),
    (FOTOS+"pierre-cardin-negro.jpg",        "Pierre Cardin"),
    (FOTOS+"elmo-dorada-negro.jpg",          "Elmo — hilo dorado"),
    (FOTOS+"camp-script-negro.jpg",          "Camp"),
    (FOTOS+"converse-hilo-negro.jpg",        "Converse"),
]

cols = 4
fw = (W - 1.0*cm - 0.4*cm*(cols-1)) / cols
fh = fw
fy_top = H - 2.6*cm

for i, (path, lbl) in enumerate(mejores):
    col = i % cols
    row = i // cols
    fx = 0.5*cm + col*(fw + 0.4*cm)
    fy = fy_top - row*(fh + 0.9*cm)
    if os.path.exists(path):
        r, iw, ih = pil_img(path, fw/cm, fh/cm)
        c.drawImage(r, fx, fy - ih, iw, ih)
    c.setFont("Helvetica", 6.5)
    c.setFillColorRGB(*GR)
    c.drawCentredString(fx + fw/2, fy - fh - 0.35*cm, lbl)

ny = fy_top - 2*(fh + 0.9*cm) - 0.6*cm
hline(c, ny, color=DG)
ny -= 0.6*cm
c.setFont("Helvetica", 8)
c.setFillColorRGB(*GR)
c.drawString(1.5*cm, ny, "·  37 fotos recibidas · 12 procesadas · Fondo removido con IA · Disponibles en versión negro, blanco y transparente PNG")
ny -= 0.5*cm
c.drawString(1.5*cm, ny, "·  Listas para incorporar a los posts de Instagram reemplazando el placeholder actual")
c.showPage()

# ══════════════════════════════════════════════════════
# 06 — PLAN DE ACCIÓN
# ══════════════════════════════════════════════════════
section_header(c, "06", "Plan de Acción", "Pasos concretos ordenados por prioridad")
c.showPage()

fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-2*cm, W, 2*cm, fill=1, stroke=0)
label(c, "06  ·  PLAN DE ACCIÓN — FASE 1", 1.5*cm, H-1.2*cm, size=8, color=AC, font="Helvetica-Bold")

cy = H - 3.0*cm

pasos_plan = [
    ("INMEDIATO",  "Esta semana", [
        "Tommy confirma qué etiqueta real va en cada post → se incorpora la foto",
        "Actualizar bio de Instagram con nuevo texto y link de WhatsApp",
        "Cambiar foto de perfil por el avatar generado",
        "Publicar los 6 posts producidos (uno por día o cada dos días)",
    ]),
    ("CORTO PLAZO", "Próximas 2 semanas", [
        "Tommy pasa fotos del taller y las máquinas suizas",
        "Producir 6 posts adicionales: bebé/regalos, urgencia, proceso, testimonios",
        "Configurar WhatsApp Business con mensajes automáticos",
        "Conectar Instagram API para publicación automática",
    ]),
    ("MEDIANO PLAZO", "Próximo mes", [
        "Estrategia de outreach: identificar 50 marcas de ropa en CABA para contactar",
        "Producir contenido de Reels: proceso de fabricación en video",
        "Publicar página de comparación KORMAN vs China en web o bio",
        "Conseguir testimonios de clientes actuales para prueba social",
    ]),
    ("LARGO PLAZO", "2–3 meses", [
        "Lanzar web propia: landing page con portfolio y formulario de cotización",
        "Google Business Profile para aparecer en búsquedas locales de CABA",
        "Meta Ads (Instagram) cuando el contenido orgánico esté funcionando",
        "Meta: 1.500 seguidores · 4%+ engagement · 10+ consultas WhatsApp/semana",
    ]),
]

for etapa, tiempo, items in pasos_plan:
    c.setFillColorRGB(*DG)
    c.rect(1.5*cm, cy - 0.55*cm, W - 3*cm, 0.55*cm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(*AC)
    c.drawString(1.8*cm, cy - 0.38*cm, etapa)
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(*GR)
    c.drawRightString(W - 1.8*cm, cy - 0.38*cm, tiempo)
    cy -= 0.55*cm + 0.3*cm
    for item in items:
        c.setFont("Helvetica", 8.5)
        c.setFillColorRGB(*WH)
        c.drawString(1.8*cm, cy, f"·  {item}")
        cy -= 0.5*cm
    cy -= 0.3*cm

hline(c, cy, color=DG)
cy -= 0.6*cm
label(c, "META PRINCIPAL: 5 marcas nuevas como clientes en 3 meses — generando consultas desde Instagram hacia WhatsApp.", 1.5*cm, cy, size=8, color=GR)
c.showPage()

# ══════════════════════════════════════════════════════
# CONTRAPORTADA
# ══════════════════════════════════════════════════════
fill_page(c, BK)
c.setFillColorRGB(*DG)
c.rect(0, H-0.4*cm, W, 0.4*cm, fill=1, stroke=0)

r, lw, lh = pil_img(LOGO_DIR+"korman-logo-v2-horizontal-blanco.png", 8, 2.5)
c.drawImage(r, (W-lw)/2, H*0.55, lw, lh, mask="auto")
hline(c, H*0.51, x0=3*cm, x1=W-3*cm, color=DG)

c.setFont("Helvetica", 9)
c.setFillColorRGB(*GR)
c.drawCentredString(W/2, H*0.47, "Gracias por su atención.")
c.setFont("Helvetica-Bold", 11)
c.setFillColorRGB(*WH)
c.drawCentredString(W/2, H*0.42, "El trabajo que ven acá es solo el comienzo.")

c.setFont("Helvetica", 8.5)
c.setFillColorRGB(*GR)
lineas = [
    "46 años fabricando etiquetas con el mismo oficio y dedicación.",
    "Ahora, con la estrategia y las herramientas para llegar a más marcas.",
]
for i, l in enumerate(lineas):
    c.drawCentredString(W/2, H*0.36 - i*0.6*cm, l)

hline(c, H*0.28, x0=3*cm, x1=W-3*cm, color=DG)

c.setFont("Helvetica-Bold", 8)
c.setFillColorRGB(*AC)
c.drawCentredString(W/2, H*0.23, "CONTACTO COMERCIAL")
c.setFont("Helvetica", 9)
c.setFillColorRGB(*WH)
c.drawCentredString(W/2, H*0.18, "WhatsApp: +54 9 11 4475-6233")
c.drawCentredString(W/2, H*0.13, "Instagram: @kormanetiquetas")
c.drawCentredString(W/2, H*0.08, "Buenos Aires, Argentina")

c.setFillColorRGB(*DG)
c.rect(0, 0, W, 0.4*cm, fill=1, stroke=0)
c.showPage()

c.save()
print(f"✓  Presentación ejecutiva generada: {OUT}")
