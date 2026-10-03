"""Genera favicon e imágenes sociales a partir del logo y las fotos originales.

Solo se necesita si cambian el logo o las fotos. Requiere Pillow:
    pip install pillow
    python scripts/generar_imagenes.py
El logo no se redibuja: se recorta y escala el archivo original.
"""
import json
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web"
A = WEB / "assets"


def simbolo():
    """Recorta el símbolo (la B) del logo original, sin alterarlo."""
    logo = Image.open(A / "logo.png").convert("RGBA")
    zona = logo.crop((0, 0, 400, logo.height))
    return zona.crop(zona.getchannel("A").getbbox())


def cuadrado(img, lado, margen, fondo=None):
    lienzo = Image.new("RGBA", (lado, lado), fondo or (0, 0, 0, 0))
    util = lado - 2 * margen
    esc = min(util / img.width, util / img.height)
    s = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
    lienzo.alpha_composite(s, ((lado - s.width) // 2, (lado - s.height) // 2))
    return lienzo


def recorte(foto, w, h):
    esc = max(w / foto.width, h / foto.height)
    f = foto.resize((round(foto.width * esc), round(foto.height * esc)), Image.LANCZOS)
    x, y = (f.width - w) // 2, (f.height - h) // 2
    return f.crop((x, y, x + w, y + h))


def social(foto, destino):
    """1200x630: logo original sobre blanco a la izquierda, fotografía a la derecha."""
    lienzo = Image.new("RGB", (1200, 630), "white")
    lienzo.paste(recorte(Image.open(foto).convert("RGB"), 700, 630), (500, 0))
    logo = Image.open(A / "logo.png").convert("RGBA")
    esc = 380 / logo.width
    logo = logo.resize((380, round(logo.height * esc)), Image.LANCZOS)
    lienzo.paste(logo, (60, (630 - logo.height) // 2), logo)
    lienzo.save(destino, quality=86)


def main():
    s = simbolo()
    cuadrado(s, 32, 1).save(WEB / "favicon-32.png")
    cuadrado(s, 192, 14).save(WEB / "icon-192.png")
    cuadrado(s, 180, 22, (255, 255, 255, 255)).convert("RGB").save(WEB / "apple-touch-icon.png")
    cuadrado(s, 64, 2).save(WEB / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    og = A / "social"
    og.mkdir(exist_ok=True)
    social(A / "portada-tech.png", og / "inicio.jpg")
    datos = json.loads((RAIZ / "contenido.json").read_text(encoding="utf-8"))
    for srv in datos["servicios"]:
        social(A / f"foto-{srv['foto']}.jpg", og / f"{srv['slug']}.jpg")
    print("Imágenes generadas en web/ y web/assets/social/")


if __name__ == "__main__":
    main()
