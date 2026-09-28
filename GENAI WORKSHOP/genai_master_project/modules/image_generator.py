"""
Text-to-Image Generation & Dynamic Synthetic Artwork Engine
Generates procedurally styled artwork using Pillow with custom dynamic prompts.
"""
from PIL import Image, ImageDraw, ImageFont
import io
import math
import random
from typing import Tuple

class ImageGeneratorEngine:
    @staticmethod
    def generate_artwork(prompt: str, style: str = "Cyberpunk / Futuristic", width: int = 512, height: int = 512) -> bytes:
        img = Image.new("RGB", (width, height), color=(20, 24, 33))
        draw = ImageDraw.Draw(img)

        # Style Palette configuration
        if style == "Cyberpunk / Futuristic":
            colors = [(0, 255, 204), (255, 0, 128), (120, 0, 255), (10, 15, 30)]
        elif style == "Photorealistic Nature":
            colors = [(34, 139, 34), (139, 69, 19), (70, 130, 180), (255, 228, 196)]
        elif style == "Abstract Oil Painting":
            colors = [(255, 99, 71), (255, 215, 0), (75, 0, 130), (0, 128, 128)]
        else:
            colors = [(240, 240, 240), (100, 100, 100), (30, 30, 30), (200, 50, 50)]

        # Procedural Artwork Generation based on prompt seed
        seed = sum(ord(c) for c in prompt)
        random.seed(seed)

        # Draw abstract background geometry
        for _ in range(30):
            c = random.choice(colors)
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            r = random.randint(20, 180)
            draw.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], outline=c, width=random.randint(1, 4))
            draw.line([(x1, y1), (x1 + r, y1 + r)], fill=c, width=random.randint(1, 3))

        # Add Title & Prompt Overlay
        draw.rectangle([10, height - 70, width - 10, height - 10], fill=(0, 0, 0, 180))
        draw.text((20, height - 60), f"Prompt: {prompt[:35]}...", fill=(255, 255, 255))
        draw.text((20, height - 35), f"Style: {style} | GenAI Synthetic Studio", fill=(0, 255, 204))

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
