#!/usr/bin/env python3
"""
KORMAN — Posts batch 2 (posts 05-10) + watermark en todos los posts
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

FONTS = "/home/user/Marketing-y-empresa-/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/Marketing-y-empresa-/.agents/design/"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
BLACK    = (8, 8, 8)
OFFWHITE = (250, 248, 244)
GOLD     = (198, 158, 86)
GOLD_DIM = (110, 85, 42)
RUST     = (140, 80, 48)
CREAM    = (235, 224, 200)
GRAY     = (120, 118, 114)
CHARCOAL = (38, 34, 30)

def load_font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except:
        return ImageFont.load_default()

def tracked_width(draw, text, font, tracking=0):
    total = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        total += (bbox[2] - bbox[0]) + tracking
    return max(total - tracking, 0)

def draw_tracked(draw, x, y, text, font, fill, tracking=0):
    cursor = x
    for ch in text:
        draw.text((cursor, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font)
        cursor += (bbox[2] - bbox[0]) + tracking

def base_canvas(bg=BLACK):
    img  = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    for i in range(-H, W+H, 24):
        draw.line([(i, 0), (i + H, H)], fill=(28, 24, 20) if bg == BLACK else (235, 232, 226), width=1)
    draw.rectangle([28, 28, W-28, H-28], outline=(42, 38, 32) if bg == BLACK else (210, 207, 200), width=1)
    return img, draw

def add_watermark(img):
    """Agrega KORMAN watermark abajo a la derecha."""
    draw  = ImageDraw.Draw(img)
    f     = load_font("BricolageGrotesque-Bold.ttf", 28)
    text  = "KORMAN"
    tw    = tracked_width(draw, text, f, 3)
    x     = W - tw - 52
    y     = H - 56
    # fondo semitransparente
    draw.rectangle([x - 10, y - 6, x + tw + 10, y + 34], fill=(8, 8, 8, 180) if True else (0,0,0))
    draw_tracked(draw, x, y, text, f, (180, 178, 174), 3)
    return img

def rust_line(draw, x1, y1, x2, y2):
    draw.line([(x1,y1),(x2,y2)], fill=RUST, width=2)

def stitch_dot_row(draw, y, count=24, color=GOLD_DIM):
    for i in range(count):
        x = 80 + i * ((W - 160) // count)
        draw.ellipse([x-2, y-2, x+2, y+2], fill=color)

# ══════════════════════════════════════════════════════════════════════════════
# POST 05 — Tipos de tejido (educativo carrusel → versión single para IG)
# ══════════════════════════════════════════════════════════════════════════════
def post_05():
    img, draw = base_canvas()
    f_it  = load_font("Italiana-Regular.ttf", 78)
    f_br  = load_font("BricolageGrotesque-Bold.ttf", 38)
    f_sub = load_font("InstrumentSans-Regular.ttf", 24)
    f_sm  = load_font("Jura-Light.ttf", 16)
    f_tag = load_font("InstrumentSans-Regular.ttf", 22)

    # Título
    draw.text((80, 80), "No todas las", font=f_it, fill=CREAM)
    draw.text((80, 168), "etiquetas", font=f_it, fill=GOLD)
    draw.text((80, 256), "son iguales.", font=f_it, fill=CREAM)

    draw.line([(80, 360), (W-80, 360)], fill=GOLD_DIM, width=1)

    # 4 tipos en columnas
    tipos = [
        ("TAFETA",         "Económica · interna",       "Talles y cuidado"),
        ("ALTA DEF.",      "La más usual · nítida",     "Logo y marca propia"),
        ("TRIPLE DENS.",   "Mayor relieve · presencia", "Efecto premium"),
        ("TEXTURADA",      "Relieve especial · única",  "Marcas de lujo"),
    ]
    col_w = (W - 160) // 4
    for i, (nombre, desc, uso) in enumerate(tipos):
        x = 80 + i * col_w
        # Línea vertical separadora
        if i > 0:
            draw.line([(x, 375), (x, 820)], fill=CHARCOAL, width=1)
        pad = 16 if i > 0 else 0
        draw.text((x + pad, 390), nombre, font=load_font("GeistMono-Regular.ttf", 14), fill=GOLD)
        draw.text((x + pad, 424), desc,   font=f_sm, fill=CREAM)
        draw.text((x + pad, 456), uso,    font=f_sm, fill=GRAY)

        # Mini stitch decorativo por tipo
        density = i + 1
        for d in range(density):
            cx_ = x + pad + 12 + d * 18
            cy_ = 520
            r   = 4 + d
            draw.ellipse([cx_-r, cy_-r, cx_+r, cy_+r], outline=GOLD if d == i else GOLD_DIM, width=1)

    stitch_dot_row(draw, 600)

    draw.line([(80, 660), (W-80, 660)], fill=GOLD_DIM, width=1)
    draw.text((80, 690), "¿Cuál es la ideal para tu marca?", font=f_sub, fill=CREAM)
    draw.text((80, 732), "Consultanos y te asesoramos.", font=f_sm, fill=GRAY)

    draw.line([(80, 860), (W-80, 860)], fill=GOLD_DIM, width=1)
    f_brand = load_font("BricolageGrotesque-Bold.ttf", 42)
    draw_tracked(draw, 80, 890, "KORMAN", f_brand, OFFWHITE, 4)
    draw.text((80, 950), "@kormanetiquetas", font=f_tag, fill=GOLD)

    img = add_watermark(img)
    img.save(OUT + "korman-post-05-tipos-tejido.png", "PNG", dpi=(300,300))
    print("✓ post-05-tipos-tejido")

# ══════════════════════════════════════════════════════════════════════════════
# POST 06 — Objeción precio → "Lo que vale una etiqueta con tu logo"
# ══════════════════════════════════════════════════════════════════════════════
def post_06():
    img, draw = base_canvas()
    f_it  = load_font("Italiana-Regular.ttf", 86)
    f_sub = load_font("InstrumentSans-Regular.ttf", 26)
    f_sm  = load_font("Jura-Light.ttf", 16)
    f_tag = load_font("InstrumentSans-Regular.ttf", 22)

    rust_line(draw, 72, 80, 72, 900)

    # Gran cita tipográfica
    draw.text((100, 120), '"¿No me sale', font=f_it, fill=CREAM)
    draw.text((100, 210), 'más caro que', font=f_it, fill=CREAM)
    draw.text((100, 300), 'importar?"', font=f_it, fill=GOLD)

    draw.line([(100, 430), (W-100, 430)], fill=GOLD_DIM, width=1)

    respuesta = [
        "Depende de cómo lo mirés.",
        "",
        "1.000 etiquetas genéricas que no",
        "representan tu marca, que tardaron",
        "3 meses, y que llegaron distintas",
        "a lo que pediste —",
        "¿cuánto te costó eso en realidad?",
    ]
    y = 458
    for linea in respuesta:
        if linea:
            color = GOLD if "cuánto" in linea else CREAM
            draw.text((100, y), linea, font=f_sub if "cuánto" not in linea else load_font("InstrumentSans-Bold.ttf", 26), fill=color)
        y += 44

    stitch_dot_row(draw, y + 30, count=20)

    draw.text((100, y + 60), "Consultanos por WhatsApp.", font=f_sub, fill=CREAM)

    draw.line([(100, 880), (W-100, 880)], fill=GOLD_DIM, width=1)
    f_brand = load_font("BricolageGrotesque-Bold.ttf", 42)
    draw_tracked(draw, 100, 910, "KORMAN", f_brand, OFFWHITE, 4)
    draw.text((100, 968), "@kormanetiquetas", font=f_tag, fill=GOLD)

    img = add_watermark(img)
    img.save(OUT + "korman-post-06-objecion-precio.png", "PNG", dpi=(300,300))
    print("✓ post-06-objecion-precio")

# ══════════════════════════════════════════════════════════════════════════════
# POST 07 — Regalos / ajuar bebé / nombres (segmento B2C)
# ══════════════════════════════════════════════════════════════════════════════
def post_07():
    img, draw = base_canvas()
    random.seed(21)
    f_it   = load_font("Italiana-Regular.ttf", 92)
    f_hand = load_font("NothingYouCouldDo-Regular.ttf", 72)  # estilo manuscrito
    f_sub  = load_font("InstrumentSans-Regular.ttf", 26)
    f_sm   = load_font("Jura-Light.ttf", 16)
    f_tag  = load_font("InstrumentSans-Regular.ttf", 22)

    # Nombre manuscrito grande como elemento visual
    draw.text((80, 80), "Valentina", font=f_hand, fill=(60, 56, 50))
    draw.text((84, 76), "Valentina", font=f_hand, fill=GOLD_DIM)

    draw.text((80, 240), "Hay regalos", font=f_it, fill=CREAM)
    draw.text((80, 332), "que no se", font=f_it, fill=CREAM)
    draw.text((80, 424), "olvidan.", font=f_it, fill=GOLD)

    draw.line([(80, 548), (W-80, 548)], fill=GOLD_DIM, width=1)

    usos = [
        "Ajuar de bebé con el nombre",
        "Ropa de jardín o colegio",
        "Regalos únicos bordados",
        "Detalles que duran para siempre",
    ]
    f_bullet = load_font("InstrumentSans-Regular.ttf", 24)
    for i, u in enumerate(usos):
        y = 572 + i * 58
        draw.ellipse([80, y+10, 88, y+18], fill=RUST)
        draw.text((104, y), u, font=f_bullet, fill=CREAM)

    draw.line([(80, 820), (W-80, 820)], fill=GOLD_DIM, width=1)
    f_brand = load_font("BricolageGrotesque-Bold.ttf", 42)
    draw_tracked(draw, 80, 850, "KORMAN", f_brand, OFFWHITE, 4)
    draw.text((80, 910), "Consultanos por WhatsApp", font=f_sm, fill=GOLD_DIM)
    draw.text((80, 944), "@kormanetiquetas", font=f_tag, fill=GOLD)

    img = add_watermark(img)
    img.save(OUT + "korman-post-07-regalos-bebe.png", "PNG", dpi=(300,300))
    print("✓ post-07-regalos-bebe")

# ══════════════════════════════════════════════════════════════════════════════
# POST 08 — 46 años (proof point de trayectoria)
# ══════════════════════════════════════════════════════════════════════════════
def post_08():
    img, draw = base_canvas()
    f_big  = load_font("BricolageGrotesque-Bold.ttf", 280)
    f_it   = load_font("Italiana-Regular.ttf", 72)
    f_sub  = load_font("InstrumentSans-Regular.ttf", 26)
    f_sm   = load_font("Jura-Light.ttf", 17)
    f_tag  = load_font("InstrumentSans-Regular.ttf", 22)

    # "46" enorme como elemento gráfico
    bbox = draw.textbbox((0,0), "46", font=f_big)
    tw   = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 80), "46", font=f_big, fill=(28, 24, 20))

    # Encima del número grande, el texto real
    draw.text((80, 160), "46 años", font=f_it, fill=GOLD)
    draw.text((80, 248), "fabricando", font=f_it, fill=CREAM)
    draw.text((80, 336), "etiquetas.", font=f_it, fill=CREAM)

    stitch_dot_row(draw, 450)

    draw.line([(80, 480), (W-80, 480)], fill=GOLD_DIM, width=1)

    datos = [
        ("1980", "Fundación de la empresa"),
        ("Suiza", "Maquinaria de alta tecnología"),
        ("CABA", "Producción local, sin intermediarios"),
        ("2026", "Seguimos, crecemos, mejoramos"),
    ]
    f_num  = load_font("GeistMono-Regular.ttf", 14)
    f_dato = load_font("InstrumentSans-Regular.ttf", 22)
    for i, (num, label) in enumerate(datos):
        y = 504 + i * 72
        draw.text((80,  y), num,   font=f_num,  fill=RUST)
        draw.text((160, y), label, font=f_dato, fill=CREAM)

    draw.line([(80, 800), (W-80, 800)], fill=GOLD_DIM, width=1)
    f_brand = load_font("BricolageGrotesque-Bold.ttf", 42)
    draw_tracked(draw, 80, 830, "KORMAN", f_brand, OFFWHITE, 4)
    draw.text((80, 888), "Buenos Aires · desde 1980", font=f_sm, fill=GRAY)
    draw.text((80, 924), "@kormanetiquetas", font=f_tag, fill=GOLD)

    img = add_watermark(img)
    img.save(OUT + "korman-post-08-46-anos.png", "PNG", dpi=(300,300))
    print("✓ post-08-46-anos")

# ══════════════════════════════════════════════════════════════════════════════
# POST 09 — Prueba social (marcas clientes)
# ══════════════════════════════════════════════════════════════════════════════
def post_09():
    img, draw = base_canvas()
    f_it   = load_font("Italiana-Regular.ttf", 78)
    f_br   = load_font("BricolageGrotesque-Bold.ttf", 28)
    f_sub  = load_font("InstrumentSans-Regular.ttf", 24)
    f_sm   = load_font("Jura-Light.ttf", 15)
    f_tag  = load_font("InstrumentSans-Regular.ttf", 22)

    rust_line(draw, 72, 80, 72, 860)

    draw.text((100, 100), "Marcas que", font=f_it, fill=CREAM)
    draw.text((100, 188), "confiaron.", font=f_it, fill=GOLD)

    draw.line([(100, 300), (W-100, 300)], fill=GOLD_DIM, width=1)

    clientes = [
        "Sugar", "Tomineto", "Clotti",
        "Veli", "Nicole Jeans", "Aripa",
        "Mini Kiwi", "Gitca",
    ]

    # Grid de nombres de clientes — efecto catálogo
    f_client = load_font("InstrumentSans-Regular.ttf", 30)
    f_dot    = load_font("Jura-Light.ttf", 14)
    col = 2
    for i, c in enumerate(clientes):
        row_ = i // col
        col_ = i % col
        x = 100 + col_ * 460
        y = 330 + row_ * 90
        draw.text((x, y), c, font=f_client, fill=CREAM if i % 2 == 0 else OFFWHITE)
        # Subrayado fino
        cw = draw.textbbox((0,0), c, font=f_client)
        draw.line([(x, y+36), (x + cw[2]-cw[0], y+36)], fill=GOLD_DIM, width=1)

    stitch_dot_row(draw, 720, count=22)

    draw.line([(100, 760), (W-100, 760)], fill=GOLD_DIM, width=1)
    draw.text((100, 790), "Tu marca podría ser la próxima.", font=f_sub, fill=CREAM)
    draw.text((100, 834), "Escribinos por WhatsApp.", font=f_sm, fill=GOLD_DIM)

    draw.line([(100, 880), (W-100, 880)], fill=GOLD_DIM, width=1)
    f_brand = load_font("BricolageGrotesque-Bold.ttf", 42)
    draw_tracked(draw, 100, 910, "KORMAN", f_brand, OFFWHITE, 4)
    draw.text((100, 968), "@kormanetiquetas", font=f_tag, fill=GOLD)

    img = add_watermark(img)
    img.save(OUT + "korman-post-09-prueba-social.png", "PNG", dpi=(300,300))
    print("✓ post-09-prueba-social")

# ══════════════════════════════════════════════════════════════════════════════
# POST 10 — Urgencia/lanzamiento ("Tu lanzamiento no puede esperar")
# ══════════════════════════════════════════════════════════════════════════════
def post_10():
    img, draw = base_canvas()
    f_it   = load_font("Italiana-Regular.ttf", 86)
    f_br   = load_font("BricolageGrotesque-Bold.ttf", 36)
    f_sub  = load_font("InstrumentSans-Regular.ttf", 26)
    f_sm   = load_font("Jura-Light.ttf", 16)
    f_tag  = load_font("InstrumentSans-Regular.ttf", 22)
    f_mono = load_font("GeistMono-Regular.ttf", 14)

    # Número de días — elemento gráfico central
    f_days = load_font("BricolageGrotesque-Bold.ttf", 200)
    bbox   = draw.textbbox((0,0), "15", font=f_days)
    tw     = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 60), "15", font=f_days, fill=(28, 24, 20))

    draw.text((80, 100), "15 a 20 días.", font=f_it, fill=GOLD)
    draw.text((80, 192), "Eso es lo que", font=f_it, fill=CREAM)
    draw.text((80, 284), "tardamos.", font=f_it, fill=CREAM)

    draw.line([(80, 400), (W-80, 400)], fill=GOLD_DIM, width=1)

    lineas = [
        "No 60 días. No 90 días.",
        "No \"cuando llegue el barco\".",
        "",
        "Producción local en CABA.",
        "Boceto digital aprobado por vos.",
        "Entrega real, con fecha real.",
    ]
    y = 428
    for l in lineas:
        if l:
            bold = "Producción" in l or "Boceto" in l or "Entrega" in l
            f_u  = load_font("InstrumentSans-Bold.ttf", 26) if bold else f_sub
            col  = CREAM if bold else (160, 158, 154)
            draw.text((80, y), l, font=f_u, fill=col)
        y += 52

    stitch_dot_row(draw, y + 20, count=18)

    draw.line([(80, 840), (W-80, 840)], fill=GOLD_DIM, width=1)
    f_brand = load_font("BricolageGrotesque-Bold.ttf", 42)
    draw_tracked(draw, 80, 870, "KORMAN", f_brand, OFFWHITE, 4)
    draw.text((80, 930), "Consultanos hoy → link en bio", font=f_sm, fill=GOLD_DIM)
    draw.text((80, 960), "@kormanetiquetas", font=f_tag, fill=GOLD)

    img = add_watermark(img)
    img.save(OUT + "korman-post-10-urgencia.png", "PNG", dpi=(300,300))
    print("✓ post-10-urgencia")

# ══════════════════════════════════════════════════════════════════════════════
# WATERMARK en los 4 posts anteriores
# ══════════════════════════════════════════════════════════════════════════════
def add_watermark_to_existing():
    posts = [
        "korman-post-01-tu-marca-bordada.png",
        "korman-post-02-sin-minimos.png",
        "korman-post-03-proceso.png",
        "korman-post-04-local-vs-china.png",
    ]
    for p in posts:
        path = OUT + p
        if os.path.exists(path):
            img = Image.open(path)
            img = add_watermark(img)
            img.save(path, "PNG", dpi=(300,300))
            print(f"✓ watermark → {p}")

# ── Run ───────────────────────────────────────────────────────────────────────
print("Generando posts 05–10...")
post_05()
post_06()
post_07()
post_08()
post_09()
post_10()
print("\nAgregando watermark a posts anteriores...")
add_watermark_to_existing()
print("\n✓ Batch 2 completo — 10 posts totales listos.")
