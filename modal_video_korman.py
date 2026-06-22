#!/usr/bin/env python3
"""
KORMAN — Generador de video cinematográfico con Modal + LTX-Video 2
Genera escenas tipo Higgsfield: persona en shopping, mirando etiqueta bordada.

Uso: python modal_video_korman.py
"""

import modal
import os

app = modal.App("korman-video")

# Imagen con todas las dependencias para LTX-Video
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.1.0",
        "torchvision",
        "diffusers>=0.30.0",
        "transformers>=4.40.0",
        "accelerate>=0.30.0",
        "sentencepiece",
        "imageio[ffmpeg]",
        "imageio-ffmpeg",
        "numpy",
        "pillow",
        "huggingface_hub",
    )
)

# Volumen para cachear el modelo (no re-descargarlo cada vez)
vol = modal.Volume.from_name("korman-models", create_if_missing=True)

PROMPTS = {
    "shopping": (
        "Cinematic close-up of elegant hands browsing through clothing racks in a high-end boutique, "
        "soft warm lighting, shallow depth of field, hand picks up a luxurious garment and turns it over "
        "to reveal a beautifully embroidered label, slow motion, 4K, fashion film aesthetic, "
        "warm golden tones, Buenos Aires boutique"
    ),
    "label_detail": (
        "Extreme close-up macro shot of a perfectly embroidered fabric label on premium clothing, "
        "threads catching warm light, fabric texture visible, elegant and luxurious feel, "
        "cinematic color grading, slow reveal, 4K fashion photography aesthetic"
    ),
    "atelier": (
        "Cinematic shot inside a professional embroidery atelier in Buenos Aires, "
        "machines creating intricate embroidered labels, warm workshop lighting, "
        "skilled artisan hands guiding fabric, slow motion details, "
        "documentary style, warm tones, 4K"
    ),
}

@app.function(
    image=image,
    gpu="A10G",
    timeout=600,
    volumes={"/models": vol},
    secrets=[modal.Secret.from_name("huggingface-secret", required=False)],
)
def generate_video(prompt_key: str = "shopping", num_frames: int = 49, fps: int = 8):
    import torch
    import imageio
    import numpy as np
    from diffusers import LTXPipeline
    from diffusers.utils import export_to_video

    prompt = PROMPTS.get(prompt_key, PROMPTS["shopping"])
    print(f"Generando video: {prompt_key}")
    print(f"Prompt: {prompt[:80]}...")

    # Cargar modelo (se cachea en el volumen)
    model_id = "Lightricks/LTX-Video"
    cache_dir = "/models/ltx-video"

    print("Cargando modelo LTX-Video...")
    pipe = LTXPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        cache_dir=cache_dir,
    )
    pipe = pipe.to("cuda")
    pipe.enable_model_cpu_offload()

    print(f"Generando {num_frames} frames...")
    output = pipe(
        prompt=prompt,
        negative_prompt=(
            "low quality, blurry, distorted, ugly, bad anatomy, "
            "watermark, text, logo, nsfw"
        ),
        num_frames=num_frames,
        width=768,
        height=432,
        num_inference_steps=50,
        guidance_scale=7.5,
        generator=torch.Generator("cuda").manual_seed(42),
    )

    frames = output.frames[0]  # list of PIL images

    # Convertir a bytes para devolver
    import tempfile, io
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        tmp_path = f.name

    export_to_video(frames, tmp_path, fps=fps)

    with open(tmp_path, "rb") as f:
        video_bytes = f.read()

    print(f"Video generado: {len(video_bytes)//1024} KB")
    return video_bytes


@app.local_entrypoint()
def main():
    import sys

    # Elegir escena: shopping, label_detail, atelier
    scene = sys.argv[1] if len(sys.argv) > 1 else "shopping"

    print(f"\nGenerando escena: {scene}")
    print("Esto tarda ~3-5 minutos en el cloud GPU...\n")

    video_bytes = generate_video.remote(prompt_key=scene)

    output_path = f"korman_{scene}.mp4"
    with open(output_path, "wb") as f:
        f.write(video_bytes)

    print(f"\n✓ Video guardado: {output_path}")
    print(f"  Tamaño: {len(video_bytes)//1024} KB")
    print(f"\nAbrilo con el reproductor de Windows.")
