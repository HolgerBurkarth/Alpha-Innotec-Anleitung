"""Erzeugt die Galerie Symbol-Library.html und die Einzel-SVGs in symbole/.

Aufruf: python display/galerie.py
Für die Foto-Vergleiche wird Pillow benötigt; ohne Pillow entfallen sie.
"""
import base64
import html
import io
from pathlib import Path

import anzeigen
import lcd

HIER = Path(__file__).resolve().parent
FOTOS = HIER.parent / "m"

# Ausschnitte der Fotos: Datei, Bereich in Pixeln
VORLAGEN = {
    "info": ("MainMenu.jpeg", (68, 4, 125, 80)),
    "heizung": ("MainMenu.jpeg", (130, 9, 187, 78)),
    "warmwasser": ("MainMenu.jpeg", (195, 14, 246, 73)),
    "lueftung": ("Menu-Aircondition.jpeg", (0, 1, 54, 72)),
    "werkzeug": ("MainMenu.jpeg", (315, 6, 373, 80)),
    "zurueck": ("Menu-OkCancel.jpeg", (6, 18, 53, 77)),
    "weiter": ("Overview.jpeg", (139, 118, 156, 138)),
    "ok": ("Menu-OkCancel.jpeg", (114, 18, 160, 77)),
    "verwerfen": ("Menu-OkCancel.jpeg", (220, 18, 265, 77)),
    "sonne": ("Menu-AC-Daily.jpeg", (168, 7, 202, 46)),
    "mond": ("Menu-AC-Nightly.jpeg", (176, 7, 199, 44)),
    "kaestchen_leer": ("Menu-TimeMode.jpeg", (249, 90, 268, 115)),
    "kaestchen_an": ("Menu-TimeMode.jpeg", (250, 63, 269, 87)),
    "party_aus": ("Overview.jpeg", (50, 90, 82, 128)),
    "plus": ("Overview.jpeg", (116, 73, 124, 83)),
    "minus": ("Overview.jpeg", (115, 122, 123, 130)),
}


def foto(datei, bereich, hoehe=72):
    try:
        from PIL import Image
    except ImportError:
        return ""
    bild = Image.open(FOTOS / datei).convert("RGB").crop(bereich)
    f = hoehe / bild.height
    bild = bild.resize((max(1, round(bild.width * f)), hoehe), Image.LANCZOS)
    puffer = io.BytesIO()
    bild.save(puffer, "PNG")
    daten = base64.b64encode(puffer.getvalue()).decode()
    return f'<img alt="Foto vom Gerät" src="data:image/png;base64,{daten}">'


def kachel(name, s):
    normal = lcd.svg(lcd.symbol(name, 0, 0, 24), 24, 24, massstab=3, rand=3)
    invers = ""
    if s.get("markierbar", True):
        bild = lcd.svg(lcd.symbol(name, 0, 0, 24, invers=True), 24, 24, massstab=3, rand=3)
        invers = f'<figure>{bild}<figcaption>Markiert</figcaption></figure>'
    vorlage = ""
    if name in VORLAGEN:
        vorlage = f'<figure>{foto(*VORLAGEN[name])}<figcaption>Foto</figcaption></figure>'
    marke = '<span class="marke">aus Foto abgeleitet, am Gerät nicht gesehen</span>' if s["herkunft"] != "Foto" else ""
    return (
        '<article class="kachel">'
        f'<div class="bilder">{vorlage}<figure>{normal}<figcaption>Normal</figcaption></figure>'
        f'{invers}</div>'
        f'<h3>{html.escape(s["titel"])}</h3>'
        f'<p>{html.escape(s["ort"])}</p>'
        f'<code>{name}</code>{marke}</article>'
    )


def zeichensatz():
    gruppen = [
        ("Ziffern und Zeichen", "0123456789 :.,-+()/°%"),
        ("Großbuchstaben", "ABCDEFGHIJKLMNOPQRSTUVWXYZ ÄÖÜ"),
        ("Kleinbuchstaben", "abcdefghijklmnopqrstuvwxyz äöüß"),
    ]
    aus = []
    for titel, zeichen in gruppen:
        b = len(zeichen) * lcd.ZELLE_B
        bild = lcd.svg(lcd.text(zeichen, 0, 0), b, 9, massstab=4, rand=3)
        aus.append(f'<h3>{titel}</h3><div class="breit">{bild}</div>')
    return "".join(aus)


def zeitbausteine():
    faelle = [
        ("Keine Markierung", None),
        ("Zeile gewählt", "zeile"),
        ("Stunde Beginn", "von_stunde"),
        ("Minute Beginn", "von_minute"),
        ("Stunde Ende", "bis_stunde"),
        ("Minute Ende", "bis_minute"),
    ]
    aus = []
    for titel, marke in faelle:
        bild = lcd.svg(lcd.zeitzeile(1, "5:00", "12:30", 0, 0, marke=marke), 96, 8, massstab=3, rand=4)
        hinweis = "" if marke in (None, "zeile") else '<span class="marke">Darstellung angenommen</span>'
        aus.append(f'<article class="kachel zeit">{bild}<h3>{titel}</h3>{hinweis}</article>')
    return "".join(aus)


def vergleich(titel, datei, bild):
    bereich = {"Menu-AC-Daily.jpeg": (0, 0, 399, 127)}.get(datei)
    if bereich is None:
        from PIL import Image
        bereich = (0, 0) + Image.open(FOTOS / datei).size
    return (f'<article class="vergleich"><h3>{titel}</h3><div class="paar">'
            f'<figure>{foto(datei, bereich, 150)}<figcaption>Foto</figcaption></figure>'
            f'<figure>{bild}<figcaption>Nachbau</figcaption></figure></div></article>')


CSS = """
:root{--bg:#f6f7f4;--karte:#fff;--text:#20261d;--leise:#626b5c;--linie:#dfe3da;--marke:#8a4b08;--markebg:#fdf1df}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#171a15;--karte:#22261f;--text:#eef1ea;--leise:#a4ad9d;--linie:#373d33;--marke:#ffcf94;--markebg:#40301c}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,"Segoe UI",sans-serif}
main{max-width:1120px;margin:auto;padding:24px 16px 56px}
h1{font-size:28px;line-height:1.2;margin:0 0 6px}
h2{font-size:20px;margin:36px 0 12px;border-top:1px solid var(--linie);padding-top:20px}
h3{font-size:15px;margin:10px 0 2px}
p{margin:0;color:var(--leise);font-size:14px}
.raster{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}
.kachel,.vergleich{background:var(--karte);border:1px solid var(--linie);border-radius:8px;padding:12px;min-width:0}
.bilder,.paar{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap}
figure{margin:0;text-align:center}
figcaption{font-size:12px;color:var(--leise);margin-top:3px}
figure img,figure svg{display:block;border-radius:4px;max-width:100%;height:auto}
code{font:12px Consolas,monospace;color:var(--leise)}
.marke{display:inline-block;margin-left:6px;padding:1px 6px;font-size:12px;border-radius:4px;color:var(--marke);background:var(--markebg)}
.breit{overflow-x:auto}.breit svg{display:block;border-radius:4px}
.zeit svg{display:block;max-width:100%;height:auto;border-radius:4px}
.spalten{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:12px}
@media (max-width:440px){.spalten{grid-template-columns:1fr}.raster{grid-template-columns:1fr}}
"""


def main():
    ziel = HIER / "symbole"
    ziel.mkdir(exist_ok=True)
    for alt in ziel.glob("*.svg"):
        alt.unlink()
    anzahl = 0
    for name, s in lcd.SYMBOLE.items():
        (ziel / f"{name}.svg").write_text(
            lcd.svg(lcd.symbol(name, 0, 0, 24), 24, 24, massstab=4, rand=2), encoding="utf-8")
        anzahl += 1
        if s.get("markierbar", True):
            (ziel / f"{name}_markiert.svg").write_text(
                lcd.svg(lcd.symbol(name, 0, 0, 24, invers=True), 24, 24, massstab=4, rand=2), encoding="utf-8")
            anzahl += 1

    kacheln = "".join(kachel(n, s) for n, s in lcd.SYMBOLE.items())
    skala_bild = lcd.svg(lcd.skala(4, 0, felder=10, position=5, nulllinie=5), 20, 60, massstab=3, rand=4)
    winter = anzeigen.ANZEIGEN["woche-sonne"]()
    nacht = anzeigen.ANZEIGEN["woche-mond"]()
    seite = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Symbol-Library</title><style>{CSS}</style></head><body><main>
<h1>Symbol-Library der Wärmepumpen-Anzeige</h1>
<p>Alle Symbole sind Vektorgrafiken und den Fotos vom Gerät nachgezeichnet. „Markiert“ ist die helle Darstellung auf dunklem Grund.</p>
<h2>Symbole ({len(lcd.SYMBOLE)})</h2><div class="raster">{kacheln}</div>
<h2>Schrift</h2><p>Eigene Strichschrift mit der durchgestrichenen Null des Geräts. Sie braucht keine installierte Schriftart.</p>{zeichensatz()}
<h2>Bausteine Zeiteingabe</h2><div class="raster">{zeitbausteine()}</div>
<h2>Skala</h2><div class="kachel" style="display:inline-block">{skala_bild}</div>
<h2>Vergleich mit dem Gerät</h2><div class="spalten">
{vergleich("Stärkere Stufe, Winter-Plan", "Menu-AC-Daily.jpeg", winter)}
{vergleich("Schwächere Stufe, Winter-Plan", "Menu-AC-Nightly.jpeg", nacht)}
{vergleich("Auswahl Schaltzeiten", "Menu-TimeMode.jpeg", anzeigen.ANZEIGEN["schaltzeiten"]())}
{vergleich("Menü Lüftung", "Menu-Aircondition.jpeg", anzeigen.ANZEIGEN["lueftung-zeitprogramm"]())}
</div></main></body></html>"""
    (HIER / "Symbol-Library.html").write_text(seite, encoding="utf-8")
    print("Geschrieben:", HIER / "Symbol-Library.html", "und", anzahl, "SVG-Dateien")


if __name__ == "__main__":
    main()
