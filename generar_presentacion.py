#!/usr/bin/env python3
"""
KORMAN ETIQUETAS — Presentación ejecutiva
Layout conservador y controlado. Nada se superpone. Nada se sale de la página.
"""
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
import io, os, textwrap

OUT      = "/home/user/Marketing-y-empresa-/docs-pdf/KORMAN-Presentacion-Ejecutiva.pdf"
LOGO_DIR = "/home/user/Marketing-y-empresa-/.agents/design/logo/"
POSTS    = "/home/user/Marketing-y-empresa-/posts_v4/"
FOTOS    = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"

PW, PH = A4   # 595.27 x 841.89 pts
M = 1.8*cm    # margen

# Colores
BK = (8/255,   8/255,   8/255)
WH = (252/255, 250/255, 246/255)
GR = (130/255, 128/255, 124/255)
DG = (48/255,  46/255,  42/255)
AC = (195/255, 188/255, 174/255)

# ── helpers ────────────────────────────────────────────────────────────────────

def load_image(path, max_w_pt, max_h_pt):
    """Carga imagen PIL y devuelve (ImageReader, w_pt, h_pt) escalado para caber."""
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    iw, ih = img.size
    scale = min(max_w_pt / iw, max_h_pt / ih)
    return ImageReader(buf), iw * scale, ih * scale

def hline(c, y, x0=None, x1=None, color=DG, lw=0.4):
    x0 = x0 or M
    x1 = x1 or PW - M
    c.setStrokeColorRGB(*color)
    c.setLineWidth(lw)
    c.line(x0, y, x1, y)

def txt(c, text, x, y, font="Helvetica", size=9, color=WH):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text)

def txt_c(c, text, y, font="Helvetica", size=9, color=WH):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawCentredString(PW/2, y, text)

def txt_r(c, text, x, y, font="Helvetica", size=9, color=WH):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawRightString(x, y, text)

def fill(c, color=BK):
    c.setFillColorRGB(*color)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)

def header_bar(c, left_text, right_text=""):
    """Barra superior negra con texto."""
    c.setFillColorRGB(*DG)
    c.rect(0, PH - 1.6*cm, PW, 1.6*cm, fill=1, stroke=0)
    txt(c, left_text,  M, PH - 1.0*cm, size=7.5, color=AC, font="Helvetica-Bold")
    if right_text:
        txt_r(c, right_text, PW - M, PH - 1.0*cm, size=7, color=GR)

def multiline(c, text, x, y, font="Helvetica", size=9, color=WH, max_chars=72, line_h=None):
    """Dibuja texto con wrap. Devuelve y final."""
    if line_h is None:
        line_h = size * 1.55
    lines = textwrap.wrap(text, max_chars)
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    for line in lines:
        c.drawString(x, y, line)
        y -= line_h
    return y

# ── PÁGINA: PORTADA ────────────────────────────────────────────────────────────
def page_portada(c):
    fill(c, BK)

    # Franja crema arriba
    c.setFillColorRGB(*AC)
    c.rect(0, PH - 0.35*cm, PW, 0.35*cm, fill=1, stroke=0)

    # Logo centrado
    r, lw, lh = load_image(LOGO_DIR + "korman-logo-v2-horizontal-blanco.png",
                            10*cm, 3.5*cm)
    c.drawImage(r, (PW - lw)/2, PH*0.60, lw, lh, mask="auto")

    hline(c, PH*0.56, x0=2.5*cm, x1=PW-2.5*cm, color=DG, lw=0.6)

    txt_c(c, "ESTRATEGIA DE MARKETING DIGITAL", PH*0.52, size=9, color=GR)
    txt_c(c, "PLAN DE CONTENIDO E IDENTIDAD VISUAL", PH*0.47, size=12, color=WH, font="Helvetica-Bold")

    hline(c, PH*0.43, x0=3*cm, x1=PW-3*cm, color=DG)

    # Datos empresa — tabla simple
    datos = [
        ("Empresa",    "KORMAN Etiquetas Bordadas"),
        ("Rubro",      "Fabricación de etiquetas bordadas personalizadas"),
        ("Ubicación",  "Colegiales, Buenos Aires, Argentina"),
        ("Fundación",  "1980  ·  46 años de trayectoria"),
        ("Fecha",      "Junio 2026"),
    ]
    y_d = PH * 0.39
    for k, v in datos:
        txt(c, k + ":", PW/2 - 6.5*cm, y_d, size=8, color=GR)
        txt(c, v,       PW/2 - 2.8*cm, y_d, size=8, color=WH, font="Helvetica-Bold")
        y_d -= 0.6*cm

    # Franja inferior
    c.setFillColorRGB(*DG)
    c.rect(0, 0, PW, 2.2*cm, fill=1, stroke=0)
    txt_c(c, "CONFIDENCIAL  ·  USO INTERNO  ·  KORMAN ETIQUETAS BORDADAS",
          1.4*cm, size=7, color=AC, font="Helvetica-Bold")
    txt_c(c, "Instagram: @kormanetiquetas   ·   WhatsApp: +54 9 11 4475-6233",
          0.8*cm, size=7.5, color=GR)

    c.showPage()

# ── PÁGINA: ÍNDICE ─────────────────────────────────────────────────────────────
def page_indice(c):
    fill(c, BK)
    header_bar(c, "KORMAN ETIQUETAS  ·  PRESENTACIÓN EJECUTIVA", "ÍNDICE")

    y = PH - 2.6*cm
    txt(c, "CONTENIDO", M, y, font="Helvetica-Bold", size=10, color=AC)
    hline(c, y - 0.35*cm)
    y -= 1.2*cm

    secciones = [
        ("01", "La Empresa",       "Historia, producto, capacidad de producción y proceso de pedido"),
        ("02", "El Mercado",       "Análisis de competidores, ventajas y cliente objetivo"),
        ("03", "Identidad Visual", "Logo aprobado, paleta de colores y tipografía"),
        ("04", "Posts Instagram",  "6 posts producidos — diseño y estrategia de contenido"),
        ("05", "Banco de Fotos",   "37 fotos de etiquetas reales procesadas profesionalmente"),
        ("06", "Plan de Acción",   "Pasos concretos ordenados por prioridad y plazo"),
    ]

    for num, titulo, desc in secciones:
        # Número
        c.setFillColorRGB(*DG)
        c.rect(M, y - 0.85*cm, 1.5*cm, 1.1*cm, fill=1, stroke=0)
        txt(c, num, M + 0.28*cm, y - 0.45*cm, font="Helvetica-Bold", size=11, color=AC)

        # Texto
        txt(c, titulo, M + 1.9*cm, y - 0.1*cm, font="Helvetica-Bold", size=11, color=WH)
        txt(c, desc,   M + 1.9*cm, y - 0.55*cm, font="Helvetica", size=8, color=GR)

        hline(c, y - 1.05*cm, color=DG)
        y -= 1.6*cm

    c.showPage()

# ── PÁGINA: SECCIÓN HEADER ─────────────────────────────────────────────────────
def page_seccion(c, num, titulo, subtitulo):
    fill(c, BK)
    # Franja lateral
    c.setFillColorRGB(*DG)
    c.rect(0, 0, 0.5*cm, PH, fill=1, stroke=0)
    # Número fantasma
    c.setFont("Helvetica-Bold", 180)
    c.setFillColorRGB(18/255, 16/255, 12/255)
    c.drawString(1.5*cm, PH/2 - 6*cm, num)
    # Título
    txt(c, titulo.upper(), 1.5*cm, PH/2 + 1.2*cm,
        font="Helvetica-Bold", size=28, color=WH)
    hline(c, PH/2 + 0.4*cm, x0=1.5*cm, color=AC, lw=1.5)
    txt(c, subtitulo, 1.5*cm, PH/2 - 0.4*cm, font="Helvetica", size=10, color=GR)
    c.showPage()

# ── PÁGINA: LA EMPRESA ─────────────────────────────────────────────────────────
def page_empresa(c):
    fill(c, BK)
    header_bar(c, "01  ·  LA EMPRESA", "KORMAN ETIQUETAS BORDADAS")

    # Columna izquierda
    CL = M
    CR = PW/2 + 0.4*cm
    CW = PW/2 - M - 0.6*cm
    y = PH - 2.6*cm

    # — QUIÉNES SOMOS
    txt(c, "QUIÉNES SOMOS", CL, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, x0=CL, x1=CL+CW, color=DG)
    y -= 0.8*cm

    parrafo = ("KORMAN Etiquetas Bordadas es una empresa familiar argentina con 46 años de "
               "trayectoria en la fabricación de etiquetas bordadas personalizadas para marcas "
               "de ropa. Fundada en 1980 en Buenos Aires, combina experiencia artesanal con "
               "maquinaria suiza de última generación.")
    y = multiline(c, parrafo, CL, y, size=8.5, color=WH, max_chars=50, line_h=13)
    y -= 0.5*cm

    # — DATOS CLAVE
    txt(c, "DATOS CLAVE", CL, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, x0=CL, x1=CL+CW, color=DG)
    y -= 0.8*cm

    datos = [
        ("Fundación",    "1980 — Buenos Aires"),
        ("Trayectoria",  "46 años en el rubro"),
        ("Ubicación",    "Colegiales, CABA"),
        ("Envíos",       "Todo el país"),
        ("Maquinaria",   "Suiza de alta tecnología"),
        ("Terminaciones","Soldado, doblado, apresto"),
        ("Plazo",        "15 a 20 días hábiles"),
        ("Instagram",    "@kormanetiquetas"),
        ("WhatsApp",     "+54 9 11 4475-6233"),
    ]
    for k, v in datos:
        txt(c, k + ":", CL, y, size=8, color=GR)
        txt(c, v, CL + 2.8*cm, y, size=8, color=WH, font="Helvetica-Bold")
        y -= 0.52*cm

    # Columna derecha — TIPOS DE ETIQUETA
    y2 = PH - 2.6*cm
    txt(c, "TIPOS DE ETIQUETA BORDADA", CR, y2, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y2 - 0.28*cm, x0=CR, x1=PW-M, color=DG)
    y2 -= 0.8*cm

    tipos = [
        ("TAFETA",
         "La más económica. Ideal para etiquetas internas, "
         "talles y cuidado de prendas."),
        ("ALTA DEFINICIÓN",
         "La más elegida. Doble densidad, colores intensos y "
         "nítidos. Mejor relación precio/calidad."),
        ("TRIPLE DENSIDAD",
         "Mayor volumen y relieve. Efecto premium. Ideal para "
         "logos con detalle."),
        ("TEXTURADA",
         "La más exclusiva. Relieve y textura especial para "
         "marcas de nivel muy premium."),
    ]
    for nombre, desc in tipos:
        txt(c, nombre, CR, y2, font="Helvetica-Bold", size=9, color=WH)
        y2 -= 0.45*cm
        y2 = multiline(c, desc, CR, y2, size=8, color=GR, max_chars=46, line_h=12)
        y2 -= 0.4*cm

    # — PROCESO
    txt(c, "PROCESO DE PEDIDO", CR, y2, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y2 - 0.28*cm, x0=CR, x1=PW-M, color=DG)
    y2 -= 0.8*cm

    pasos_p = [
        "1.  Cliente envía su logo o diseño",
        "2.  KORMAN produce boceto digital a escala real",
        "3.  Cliente aprueba el boceto",
        "4.  Producción en 15 a 20 días hábiles",
        "5.  Entrega con terminación y apresto incluidos",
    ]
    for p in pasos_p:
        txt(c, p, CR, y2, size=8.5, color=WH)
        y2 -= 0.52*cm

    # Nota pie
    hline(c, 1.4*cm, color=DG)
    txt(c, "PRECIOS: Varían según diseño, tejido, tamaño, terminación y cantidad. Nunca se publica precio. Toda consulta se cotiza individualmente por WhatsApp.",
        M, 0.85*cm, size=6.5, color=GR)

    c.showPage()

# ── PÁGINA: EL MERCADO ─────────────────────────────────────────────────────────
def page_mercado(c):
    fill(c, BK)
    header_bar(c, "02  ·  EL MERCADO", "ANÁLISIS DE COMPETENCIA Y POSICIONAMIENTO")

    y = PH - 2.6*cm
    txt(c, "COMPETIDORES ANALIZADOS", M, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, color=DG)
    y -= 0.9*cm

    comps = [
        ("PRINTMAX SRL",      "Marca consolidada, catálogo amplio",
                              "Sin Instagram activo. No atiende emprendedores ni pedidos chicos."),
        ("BESTLABELS",        "Precio visible, mínimo 100 unidades, e-commerce",
                              "Internacional, sin producción local ni asesoramiento."),
        ("IMPORTACIÓN CHINA", "Precio bajo por unidad en grandes cantidades",
                              "Mínimo 500–1.000 u. Demora 60–90 días. Sin revisión previa. Riesgo alto."),
        ("INFORMALES (IG)",   "Respuesta rápida, precio bajo",
                              "Mínimos en metros (400–500m). Calidad variable. Sin garantía de plazos."),
    ]
    for nombre, fortaleza, debilidad in comps:
        txt(c, nombre, M, y, font="Helvetica-Bold", size=9, color=WH)
        y -= 0.42*cm
        txt(c, "+ " + fortaleza, M + 0.3*cm, y, size=8, color=GR)
        y -= 0.38*cm
        txt(c, "– " + debilidad, M + 0.3*cm, y, size=8, color=(180/255, 100/255, 90/255))
        hline(c, y - 0.3*cm, color=DG)
        y -= 0.75*cm

    y -= 0.2*cm
    txt(c, "NUESTRAS VENTAJAS COMPETITIVAS", M, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, color=DG)
    y -= 0.85*cm

    ventajas = [
        "46 años de experiencia — nadie en el mercado local tiene esa trayectoria",
        "Maquinaria suiza de alta tecnología — calidad de nivel internacional",
        "Sin mínimos altos — trabajamos con marcas que arrancan",
        "Boceto digital aprobado antes de producir — cero sorpresas",
        "Entrega en 15–20 días — versus 60–90 días de China",
        "Producción local en CABA — Industria Argentina",
        "Asesoramiento personalizado — no somos un e-commerce frío",
    ]
    for v in ventajas:
        txt(c, "✓  " + v, M, y, size=8.5, color=WH)
        y -= 0.5*cm

    y -= 0.3*cm
    txt(c, "CLIENTE OBJETIVO", M, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, color=DG)
    y -= 0.85*cm

    clientes = [
        "Emprendedoras de moda y marcas de ropa emergentes en CABA y GBA",
        "Diseñadoras independientes que lanzan su primera colección",
        "Marcas consolidadas que quieren mejorar la calidad de su etiqueta",
        "Línea bebé y niños — etiquetas con colores suaves y diseños tiernos",
        "Empresas que necesitan etiquetas de talle, cuidado o instrucciones de lavado",
    ]
    for cl in clientes:
        txt(c, "·  " + cl, M, y, size=8.5, color=GR)
        y -= 0.5*cm

    hline(c, 1.4*cm, color=DG)
    txt(c, "Análisis realizado con Firecrawl — scraping real de sitios de competidores — Junio 2026",
        M, 0.85*cm, size=6.5, color=GR)
    c.showPage()

# ── PÁGINA: IDENTIDAD VISUAL ───────────────────────────────────────────────────
def page_identidad(c):
    fill(c, BK)
    header_bar(c, "03  ·  IDENTIDAD VISUAL", "LOGO · PALETA · TIPOGRAFÍA")

    # Logo versión negra (sobre blanco)
    y = PH - 2.5*cm
    txt(c, "LOGO APROBADO", M, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, color=DG)
    y -= 0.6*cm

    # Caja blanca para logo negro
    box_h = 2.8*cm
    box_w = (PW - 2*M - 0.6*cm) / 2

    c.setFillColorRGB(*WH)
    c.rect(M, y - box_h, box_w, box_h, fill=1, stroke=0)
    r, lw, lh = load_image(LOGO_DIR + "korman-logo-v2-horizontal-negro.png",
                            box_w - 1.2*cm, box_h - 0.8*cm)
    c.drawImage(r, M + (box_w - lw)/2, y - box_h + (box_h - lh)/2, lw, lh, mask="auto")

    # Caja negra con borde para logo blanco
    bx2 = M + box_w + 0.6*cm
    c.setFillColorRGB(*BK)
    c.setStrokeColorRGB(*DG)
    c.setLineWidth(0.5)
    c.rect(bx2, y - box_h, box_w, box_h, fill=1, stroke=1)
    r2, lw2, lh2 = load_image(LOGO_DIR + "korman-logo-v2-horizontal-blanco.png",
                               box_w - 1.2*cm, box_h - 0.8*cm)
    c.drawImage(r2, bx2 + (box_w - lw2)/2, y - box_h + (box_h - lh2)/2, lw2, lh2, mask="auto")

    txt(c, "Versión negra — web y documentos", M, y - box_h - 0.38*cm, size=7, color=GR)
    txt(c, "Versión blanca — Instagram y fondos oscuros", bx2, y - box_h - 0.38*cm, size=7, color=GR)

    # Avatar
    y -= box_h + 1.0*cm
    av_size = 2.0*cm
    c.setFillColorRGB(*WH)
    c.circle(M + av_size/2, y - av_size/2, av_size/2, fill=1, stroke=0)
    r3, lw3, lh3 = load_image(LOGO_DIR + "korman-logo-v2-avatar.png", av_size, av_size)
    c.drawImage(r3, M, y - av_size, av_size, av_size, mask="auto")
    txt(c, "Avatar Instagram / WhatsApp", M + av_size + 0.4*cm, y - av_size/2 + 0.15*cm,
        size=8, color=GR)

    # Paleta
    y -= av_size + 0.8*cm
    txt(c, "PALETA DE COLORES", M, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, color=DG)
    y -= 0.75*cm

    paleta = [
        (BK,                            "#080808", "Negro profundo",  "Fondo principal de todos los posts"),
        (WH,                            "#FCFAF6", "Blanco roto",     "Texto principal"),
        ((150/255,148/255,144/255),     "#969490", "Gris cálido",     "Subtítulos y labels"),
        (DG,                            "#373531", "Gris oscuro",     "Separadores y detalles"),
    ]
    sw = (PW - 2*M - 0.3*cm*3) / 4
    sh = 1.2*cm
    for i, (rgb, hex_v, nombre, uso) in enumerate(paleta):
        px = M + i*(sw + 0.3*cm)
        c.setFillColorRGB(*rgb)
        if rgb == WH:
            c.setStrokeColorRGB(*DG); c.setLineWidth(0.3)
            c.rect(px, y - sh, sw, sh, fill=1, stroke=1)
        else:
            c.rect(px, y - sh, sw, sh, fill=1, stroke=0)
        txt(c, hex_v,  px, y - sh - 0.38*cm, size=7, color=GR)
        txt(c, nombre, px, y - sh - 0.7*cm,  size=7, color=WH, font="Helvetica-Bold")
        # uso en 2 líneas si es largo
        palabras = uso.split()
        linea1 = " ".join(palabras[:3])
        linea2 = " ".join(palabras[3:])
        txt(c, linea1, px, y - sh - 1.0*cm, size=6.5, color=GR)
        if linea2:
            txt(c, linea2, px, y - sh - 1.3*cm, size=6.5, color=GR)

    # Tipografía
    y -= sh + 1.8*cm
    txt(c, "TIPOGRAFÍA", M, y, font="Helvetica-Bold", size=8, color=AC)
    hline(c, y - 0.28*cm, color=DG)
    y -= 0.8*cm

    typos = [
        ("Helvetica-Bold", 26, "ABCDE 123",  "BricolageGrotesque Bold",  "Títulos de posts · Logo"),
        ("Helvetica",      17, "ABCDEFGH",   "InstrumentSans Regular",   "Subtítulos · Cuerpo"),
        ("Helvetica",      11, "ABCDEFGHIJK","Jura Light",               "Labels · Secciones"),
    ]
    for font_s, size_s, sample, real, uso in typos:
        c.setFont(font_s, size_s)
        c.setFillColorRGB(*WH)
        c.drawString(M, y, sample)
        txt(c, real, M + 5.5*cm, y, font="Helvetica-Bold", size=8, color=AC)
        txt(c, uso,  M + 5.5*cm, y - 0.42*cm, size=7.5, color=GR)
        hline(c, y - 0.72*cm, color=DG)
        y -= 1.1*cm

    hline(c, 1.4*cm, color=DG)
    txt(c, "Filosofía de diseño «Silencio Textil»: espacio como material, tipografía monumental, paleta en absolutos. Inspiración: Toteme, COS, The Row.",
        M, 0.85*cm, size=6.5, color=GR)
    c.showPage()

# ── PÁGINA: POSTS (3 posts por página × 2 páginas) ────────────────────────────
def page_posts(c):
    posts_data = [
        (POSTS+"01-tafeta.png",          "TAFETA",          "ETIQUETA BORDADA · 01", "Económica · para etiquetas internas"),
        (POSTS+"02-alta-definicion.png", "ALTA DEFINICIÓN", "ETIQUETA BORDADA · 02", "Nítida · colores intensos · la más elegida"),
        (POSTS+"03-triple-densidad.png", "TRIPLE DENSIDAD", "ETIQUETA BORDADA · 03", "Mayor relieve · presencia · efecto premium"),
        (POSTS+"04-texturada.png",       "TEXTURADA",       "ETIQUETA BORDADA · 04", "Relieve especial · para marcas que se diferencian"),
        (POSTS+"05-historia-1980.png",   "1980",            "HISTORIA · 01",         "Así empezó KORMAN ETIQUETAS en Buenos Aires"),
        (POSTS+"06-historia-46-anos.png","46 AÑOS",         "HISTORIA · 02",         "El mismo oficio · la misma dedicación"),
    ]

    # Página 1: posts 1-3
    for start, serie_label in [(0, "SERIE: TIPOS DE ETIQUETAS BORDADAS"),
                                (3, "SERIE: HISTORIA DE LA EMPRESA")]:
        fill(c, BK)
        header_bar(c, "04  ·  POSTS INSTAGRAM — " + serie_label)

        # 3 posts en fila
        batch = posts_data[start:start+3]
        n = len(batch)
        pad = 0.4*cm
        post_w = (PW - 2*M - pad*(n-1)) / n
        post_h = post_w  # cuadrado

        top_y = PH - 2.3*cm
        # centrar verticalmente en el espacio disponible
        space = top_y - 3.2*cm  # espacio para el post + labels
        if post_h > space - 1.2*cm:
            post_h = space - 1.2*cm
            post_w = post_h

        # re-centrar horizontalmente
        total_w = post_w*n + pad*(n-1)
        x_start = (PW - total_w)/2

        for i, (path, tit, lbl, sub) in enumerate(batch):
            px = x_start + i*(post_w + pad)
            py_top = top_y - 0.2*cm
            if os.path.exists(path):
                r, iw, ih = load_image(path, post_w, post_h)
                # dibujar desde py_top hacia abajo
                c.drawImage(r, px, py_top - ih, iw, ih)
                label_y = py_top - ih - 0.45*cm
            else:
                label_y = py_top - post_h - 0.45*cm

            txt(c, lbl, px, label_y,       size=6.5, color=GR)
            txt(c, tit, px, label_y-0.4*cm, size=9, color=WH, font="Helvetica-Bold")
            txt(c, sub, px, label_y-0.8*cm, size=7, color=GR)

        # Nota pie
        hline(c, 1.7*cm, color=DG)
        nota = ("Formato: 1080 × 1080 px · 300 dpi · PNG alta calidad  ·  "
                "Pendiente: incorporar foto real de etiqueta en cada post")
        txt(c, nota, M, 1.1*cm, size=6.5, color=GR)
        c.showPage()

# ── PÁGINA: FOTOS PROCESADAS ───────────────────────────────────────────────────
def page_fotos(c):
    fill(c, BK)
    header_bar(c, "05  ·  BANCO DE FOTOS PROCESADAS", "FONDO REMOVIDO CON IA — 12 ETIQUETAS")

    mejores = [
        (FOTOS+"beditorial-editorial-negro.jpg", "Beditorial"),
        (FOTOS+"givenchy-denim-negro.jpg",       "Givenchy"),
        (FOTOS+"balmain-cadena-negro.jpg",       "Balmain"),
        (FOTOS+"tough-jeansmith-negro.jpg",      "Tough Jeansmith"),
        (FOTOS+"pierre-cardin-negro.jpg",        "Pierre Cardin"),
        (FOTOS+"elmo-dorada-negro.jpg",          "Elmo — hilo dorado"),
        (FOTOS+"camp-script-negro.jpg",          "Camp"),
        (FOTOS+"converse-hilo-negro.jpg",        "Converse"),
        (FOTOS+"wet-etonic-negro.jpg",           "Wet Etonic"),
        (FOTOS+"nxlevel-negro.jpg",              "NX Level"),
        (FOTOS+"precioux-girls-negro.jpg",       "Precioux Girls"),
        (FOTOS+"camps-1983-abanico-negro.jpg",   "Camps 1983"),
    ]

    cols = 4
    rows = 3
    pad  = 0.35*cm
    fw   = (PW - 2*M - pad*(cols-1)) / cols
    fh   = fw
    y_top = PH - 2.3*cm

    for i, (path, lbl) in enumerate(mejores):
        col = i % cols
        row = i // cols
        fx = M + col*(fw + pad)
        fy = y_top - row*(fh + 0.9*cm)
        if os.path.exists(path):
            r, iw, ih = load_image(path, fw, fh)
            c.drawImage(r, fx + (fw-iw)/2, fy - ih, iw, ih)
        txt_c(c, lbl, fy - fh - 0.35*cm, size=6.5, color=GR)
        # corregir posición x para centrar bajo la imagen
        c.setFont("Helvetica", 6.5)
        c.setFillColorRGB(*GR)
        c.drawCentredString(fx + fw/2, fy - fh - 0.38*cm, lbl)

    hline(c, 1.4*cm, color=DG)
    txt(c, "37 fotos recibidas · 12 procesadas con IA · versiones negro, blanco y PNG transparente · listas para incorporar a los posts",
        M, 0.85*cm, size=6.5, color=GR)
    c.showPage()

# ── PÁGINA: PLAN DE ACCIÓN ─────────────────────────────────────────────────────
def page_plan(c):
    fill(c, BK)
    header_bar(c, "06  ·  PLAN DE ACCIÓN", "PASOS ORDENADOS POR PRIORIDAD")

    y = PH - 2.6*cm

    etapas = [
        ("INMEDIATO — Esta semana", [
            "Tommy confirma qué etiqueta va en cada post → se incorpora la foto real",
            "Actualizar bio de Instagram: nuevo texto + link de WhatsApp",
            "Cambiar foto de perfil por el avatar diseñado",
            "Publicar los 6 posts producidos (uno por día o cada dos días)",
        ]),
        ("CORTO PLAZO — Próximas 2 semanas", [
            "Tommy pasa fotos del taller y las máquinas suizas para más contenido",
            "Producir 6 posts adicionales: bebé/regalos, proceso, urgencia, testimonios",
            "Configurar WhatsApp Business con mensajes automáticos de bienvenida",
            "Conectar Instagram API para publicación programada automática",
        ]),
        ("MEDIANO PLAZO — Próximo mes", [
            "Outreach: identificar 50 marcas de ropa en CABA para contactar por DM",
            "Producir Reels: video del proceso de fabricación en el taller",
            "Publicar comparación KORMAN vs importar desde China",
            "Recolectar testimonios de clientes actuales para prueba social",
        ]),
        ("LARGO PLAZO — 2 a 3 meses", [
            "Web propia: landing page con portfolio y formulario de cotización",
            "Google Business Profile para aparecer en búsquedas locales de CABA",
            "Meta Ads (Instagram) una vez que el contenido orgánico funcione",
            "Meta: 1.500 seguidores · 4%+ engagement · 10+ consultas WhatsApp por semana",
        ]),
    ]

    for etapa, items in etapas:
        # Barra de etapa
        c.setFillColorRGB(*DG)
        c.rect(M, y - 0.5*cm, PW - 2*M, 0.5*cm, fill=1, stroke=0)
        txt(c, etapa, M + 0.2*cm, y - 0.32*cm, font="Helvetica-Bold", size=8, color=AC)
        y -= 0.5*cm + 0.35*cm

        for item in items:
            txt(c, "·  " + item, M + 0.3*cm, y, size=8.5, color=WH)
            y -= 0.5*cm
        y -= 0.3*cm

    hline(c, y - 0.1*cm, color=DG)
    y -= 0.7*cm
    txt(c, "META PRINCIPAL: 5 marcas nuevas como clientes en 3 meses — generando consultas desde Instagram hacia WhatsApp.",
        M, y, size=8, color=AC, font="Helvetica-Bold")

    hline(c, 1.4*cm, color=DG)
    txt(c, "Todo el progreso se documenta y actualiza en cada sesión de trabajo.",
        M, 0.85*cm, size=6.5, color=GR)
    c.showPage()

# ── CONTRAPORTADA ──────────────────────────────────────────────────────────────
def page_cierre(c):
    fill(c, BK)
    c.setFillColorRGB(*AC)
    c.rect(0, PH - 0.35*cm, PW, 0.35*cm, fill=1, stroke=0)

    r, lw, lh = load_image(LOGO_DIR + "korman-logo-v2-horizontal-blanco.png", 8*cm, 2.5*cm)
    c.drawImage(r, (PW - lw)/2, PH*0.58, lw, lh, mask="auto")

    hline(c, PH*0.54, x0=3*cm, x1=PW-3*cm, color=DG)

    txt_c(c, "El trabajo que ven acá es solo el comienzo.", PH*0.49, size=11, color=WH, font="Helvetica-Bold")
    txt_c(c, "46 años fabricando etiquetas con el mismo oficio.", PH*0.44, size=9, color=GR)
    txt_c(c, "Ahora, con la estrategia y las herramientas para llegar a más marcas.", PH*0.40, size=9, color=GR)

    hline(c, PH*0.34, x0=3*cm, x1=PW-3*cm, color=DG)

    txt_c(c, "CONTACTO COMERCIAL", PH*0.29, size=8, color=AC, font="Helvetica-Bold")
    txt_c(c, "WhatsApp: +54 9 11 4475-6233", PH*0.24, size=10, color=WH)
    txt_c(c, "Instagram: @kormanetiquetas", PH*0.19, size=10, color=WH)
    txt_c(c, "Buenos Aires, Argentina  ·  desde 1980", PH*0.14, size=8.5, color=GR)

    c.setFillColorRGB(*DG)
    c.rect(0, 0, PW, 0.35*cm, fill=1, stroke=0)
    c.showPage()

# ── GENERAR ────────────────────────────────────────────────────────────────────
c = rl_canvas.Canvas(OUT, pagesize=A4)

page_portada(c)
page_indice(c)
page_seccion(c, "01", "La Empresa", "Historia, producto y capacidad de producción")
page_empresa(c)
page_seccion(c, "02", "El Mercado", "Análisis de competidores y posicionamiento")
page_mercado(c)
page_seccion(c, "03", "Identidad Visual", "Logo, paleta de colores y tipografía")
page_identidad(c)
page_seccion(c, "04", "Posts Instagram", "6 posts producidos listos para publicar")
page_posts(c)
page_seccion(c, "05", "Banco de Fotos", "37 fotos de etiquetas procesadas con IA")
page_fotos(c)
page_seccion(c, "06", "Plan de Acción", "Pasos concretos ordenados por prioridad")
page_plan(c)
page_cierre(c)

c.save()
print(f"✓  {OUT}")
