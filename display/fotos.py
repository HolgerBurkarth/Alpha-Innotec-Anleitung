"""Verkleinert Fotos für die Anleitung nach m/foto/ und entfernt die Metadaten.

Aufruf: python display/fotos.py <Ordner mit den Originalen>
Bereich: Ausschnitt in Anteilen von Breite und Höhe (links, oben, rechts, unten).
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

ZIEL = Path(__file__).resolve().parent.parent / "m" / "foto"

FOTOS = {
    "bedienfeld": ("IMG_2494.jpeg", (0, 0, 1, 1)),
    "deckel-oeffnen": ("IMG_2569.jpeg", (0.3, 0.16, 1, 0.72)),
    "winter-platte-unten": ("IMG_2570.jpeg", (0, 0, 1, 1)),
    "sommer-platte-drin": ("IMG_2571.jpeg", (0, 0, 1, 1)),
    "filter": ("IMG_2575.jpeg", (0, 0, 1, 1)),
    "sommer-dreieck": ("IMG_2572.jpeg", (0.15, 0, 1, 0.5)),
}


def main(quelle):
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, (datei, b) in FOTOS.items():
        bild = ImageOps.exif_transpose(Image.open(Path(quelle) / datei)).convert("RGB")
        w, h = bild.size
        bild = bild.crop((int(b[0] * w), int(b[1] * h), int(b[2] * w), int(b[3] * h)))
        bild.thumbnail((1000, 1000), Image.LANCZOS)
        bild.save(ZIEL / f"{name}.jpg", quality=80, optimize=True)
    print(len(FOTOS), "Fotos in", ZIEL)


if __name__ == "__main__":
    main(sys.argv[1])
