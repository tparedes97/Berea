"""Acerca el cian de la portada al turquesa del logo, sin tocar las zonas en gris.

Lee originales/portada-tech.png y escribe web/assets/portada-tech.png.
    pip install pillow numpy
    python scripts/ajustar_portada.py [intensidad]   # 0 = original, 1 = ajuste completo
Solo cambia el color: la composición, la persona y la ciudad quedan iguales.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
k = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

rgb = np.asarray(Image.open(RAIZ / "originales/portada-tech.png").convert("RGB")).astype(np.float32) / 255
mx, mn = rgb.max(2), rgb.min(2)
l = (mx + mn) / 2
d = mx - mn
s = np.where(d == 0, 0, d / (1 - np.abs(2 * l - 1) + 1e-6))
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
h = np.select([mx == r, mx == g], [((g - b) / (d + 1e-6)) % 6, (b - r) / (d + 1e-6) + 2], (r - g) / (d + 1e-6) + 4) * 60
h = np.where(d == 0, 0, h)

# Peso: 0 en grises (persona, ciudad), 1 en el cian saturado del vidrio y los gráficos.
# Se mide por croma (intensidad absoluta del color), que no se dispara en los blancos,
# y se suaviza para que la transición no deje manchas.
w = np.clip((d - 0.05) / 0.28, 0, 1)
w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255 * k
h2 = h + (180 - h) * 0.9 * w            # tono hacia el turquesa del logo (180°)
l2 = l * (1 - 0.26 * w)                 # menos pastel, más profundo
s2 = s * (1 - 0.06 * w)

c = (1 - np.abs(2 * l2 - 1)) * s2
x = c * (1 - np.abs((h2 / 60) % 2 - 1))
m = l2 - c / 2
seg = (h2 // 60).astype(int) % 6
z = np.zeros_like(c)
tabla = [(c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x)]
out = np.zeros_like(rgb)
for i, (a1, a2, a3) in enumerate(tabla):
    sel = seg == i
    for ch, val in enumerate((a1, a2, a3)):
        out[..., ch][sel] = (val + m)[sel]
Image.fromarray((np.clip(out, 0, 1) * 255 + .5).astype(np.uint8)).save(RAIZ / "web/assets/portada-tech.png", optimize=True)
print("Portada ajustada con intensidad", k)
