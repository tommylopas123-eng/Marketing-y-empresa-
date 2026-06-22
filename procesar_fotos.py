#!/usr/bin/env python3
"""
Procesa las mejores fotos de etiquetas:
- Remueve el fondo
- Centra la etiqueta en fondo negro (para posts KORMAN)
- También guarda versión con fondo blanco (versátil)
"""
from rembg import remove
from PIL import Image, ImageFilter, ImageEnhance
import os

UPLOADS = "/root/.claude/uploads/7455119c-d613-5489-af46-388434342115/"
OUT     = "/home/user/Marketing-y-empresa-/assets/fotos-procesadas/"
os.makedirs(OUT, exist_ok=True)

# Las 8 mejores fotos para usar en posts (archivo → nombre limpio)
FOTOS = {
    "a56e1d1f-32a67dad1c1c4324b2431308377f4079.jpeg": "beditorial-editorial",
    "1aeaeb7d-d299e2515deb4984aa0f82c52607eade.jpeg": "givenchy-denim",
    "834826db-808ee85a30eb423fa38ce5406c339f63.jpeg": "balmain-cadena",
    "afac5d63-11c957025ded4b5f973a0142401d3a82.jpeg": "tough-jeansmith",
    "6c9baf9b-861c4bcb62dc4ff18d13f13b35c26d91.jpeg": "camps-1983-abanico",
    "0d0b315d-f64ed688d9344ab1a1d92bbaa4dbdf3e.jpeg": "converse-hilo",
    "6500124e-3e739db032844d89a7a5c8d7b0558dc0.jpeg": "pierre-cardin",
    "0869f20a-2ebfd91057ac43b191083387cb7078cd.jpeg": "elmo-dorada",
    # Extra — muy buenas
    "4eb566eb-11054289c9154e6e86618b067cf31b7e.jpeg": "wet-etonic",
    "01952ab9-baf774640f0e46b1913c0a05205e2ba3.jpeg": "nxlevel",
    "3b855dde-a0f6c6988cda45d29d93b53ddc545c0d.jpeg": "camp-script",
    "edd4033c-06ff04166a9646f1896e236a2eb0abf8.jpeg": "precioux-girls",
}

def procesar(src_path, nombre):
    print(f"  Procesando {nombre}...", end=" ")
    try:
        img = Image.open(src_path).convert("RGBA")

        # Remover fondo → resultado con canal alpha
        resultado = remove(img)

        # ── Versión NEGRA (para posts Instagram KORMAN) ────────────────────
        size = 800
        canvas_negro = Image.new("RGBA", (size, size), (8, 8, 8, 255))

        # Escalar la etiqueta para que ocupe ~75% del canvas
        et = resultado.copy()
        et.thumbnail((int(size * 0.78), int(size * 0.78)), Image.LANCZOS)

        # Centrar
        x = (size - et.width) // 2
        y = (size - et.height) // 2
        canvas_negro.paste(et, (x, y), et)

        negro_rgb = canvas_negro.convert("RGB")
        negro_rgb.save(OUT + f"{nombre}-negro.jpg", "JPEG", quality=95)

        # ── Versión BLANCA (versátil) ────────────────────────────────────────
        canvas_blanco = Image.new("RGBA", (size, size), (250, 248, 244, 255))
        canvas_blanco.paste(et, (x, y), et)
        blanco_rgb = canvas_blanco.convert("RGB")
        blanco_rgb.save(OUT + f"{nombre}-blanco.jpg", "JPEG", quality=95)

        # ── Versión TRANSPARENTE (PNG con alpha) ─────────────────────────────
        resultado.save(OUT + f"{nombre}-transparente.png", "PNG")

        print(f"✓")
    except Exception as e:
        print(f"✗ Error: {e}")

print("Procesando fotos de etiquetas...\n")
for archivo, nombre in FOTOS.items():
    src = UPLOADS + archivo
    if os.path.exists(src):
        procesar(src, nombre)
    else:
        print(f"  ✗ No encontrado: {archivo}")

print(f"\n✓ Fotos procesadas en {OUT}")
