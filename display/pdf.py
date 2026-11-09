"""Erzeugt aus README.md die Druckfassung Anleitung.pdf.

Aufruf: python display/pdf.py
Braucht Microsoft Edge oder Google Chrome, aber keine Zusatzpakete.
Der Umsetzer versteht nur die Markdown-Elemente, die die README benutzt.
"""
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent

CSS = """
@page{size:A4;margin:14mm 15mm}
body{font:11pt/1.42 "Segoe UI",Arial,sans-serif;color:#1c1c1c}
h1{font-size:21pt;margin:0 0 6pt;line-height:1.15}
h2{font-size:15pt;margin:14pt 0 6pt;border-bottom:1.5pt solid #5b7a4a;padding-bottom:2pt;break-after:avoid}
h3{font-size:12pt;margin:10pt 0 3pt;break-after:avoid}
h4{font-size:11pt;margin:8pt 0 2pt;break-after:avoid}
p{margin:0 0 6pt}
table{border-collapse:collapse;width:100%;margin:4pt 0 8pt;font-size:10pt;break-inside:auto}
tr{break-inside:avoid}
th,td{border:.6pt solid #b8bdb2;padding:3pt 5pt;text-align:left;vertical-align:top}
th{background:#e9eee3}
img{max-width:100%}
td img[src$=".jpg"]{max-height:5cm;display:block}
p.bild{break-inside:avoid;margin:4pt 0 8pt}
p.bild img{max-height:3.2cm;width:auto;margin-right:8pt}
p.bild img[src$=".jpg"]{max-height:4.2cm}
p.bild img[src*="bedienfeld"]{max-height:7.5cm}
.li{display:flex;gap:5pt;margin:0 0 3pt;break-inside:avoid}
.li>span{flex:none;min-width:12pt}
.hinweis{border-left:3pt solid #b3261e;background:#fbeeec;padding:5pt 8pt;margin:6pt 0 8pt;break-inside:avoid}
.hinweis.tip{border-color:#5b7a4a;background:#eef3e9}
code{font:10pt Consolas,monospace}
"""


def anker(s):
    return re.sub(r"[^\w\- ]", "", s.strip().lower(), flags=re.U).replace(" ", "-")


def inline(s):
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    s = re.sub(r"\[([^\]]+)\]\((#[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"(?<![\w/])_([^_]+)_(?![\w/])", r"<em>\1</em>", s)
    return s


def tabelle(zeilen):
    def zellen(z):
        return [c.strip() for c in z.strip().strip("|").split("|")]
    kopf = "".join(f"<th>{inline(c)}</th>" for c in zellen(zeilen[0]))
    rumpf = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in zellen(z)) + "</tr>" for z in zeilen[2:])
    return f"<table><thead><tr>{kopf}</tr></thead><tbody>{rumpf}</tbody></table>"


def umsetzen(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    zeilen = text.splitlines()
    aus, i = [], 0
    while i < len(zeilen):
        z = zeilen[i].strip()
        if not z:
            i += 1
        elif z.startswith("<div"):
            aus.append(z)
            i += 1
        elif z.startswith("|"):
            block = []
            while i < len(zeilen) and zeilen[i].strip().startswith("|"):
                block.append(zeilen[i])
                i += 1
            aus.append(tabelle(block))
        elif m := re.match(r"(#{1,4}) (.+)", z):
            n = len(m[1])
            aus.append(f'<h{n} id="{anker(m[2])}">{inline(m[2])}</h{n}>')
            i += 1
        elif z.startswith(">"):
            block = []
            while i < len(zeilen) and zeilen[i].strip().startswith(">"):
                block.append(zeilen[i].strip().lstrip(">").strip())
                i += 1
            art = "tip" if block[0] in ("[!TIP]", "[!NOTE]") else ""
            if block[0].startswith("[!"):
                block = block[1:]
            aus.append(f'<div class="hinweis {art}">{inline(" ".join(block))}</div>')
        elif z.startswith("!["):
            aus.append(f'<p class="bild">{inline(z)}</p>')
            i += 1
        elif m := re.match(r"(\d+\.|-) (.+)", z):
            marke = "•" if m[1] == "-" else m[1]
            aus.append(f'<div class="li"><span>{marke}</span><div>{inline(m[2])}</div></div>')
            i += 1
        else:
            aus.append(f"<p>{inline(z)}</p>")
            i += 1
    return "\n".join(aus)


def browser():
    kandidaten = [
        Path(os.environ.get("ProgramFiles(x86)", "")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("ProgramFiles", "")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("ProgramFiles", "")) / "Google/Chrome/Application/chrome.exe",
    ]
    for k in kandidaten:
        if k.exists():
            return str(k)
    for name in ("google-chrome", "chromium", "chromium-browser"):
        if pfad := shutil.which(name):
            return pfad
    raise SystemExit("Weder Edge noch Chrome gefunden.")


def drucken(seite, ziel):
    """Schreibt eine HTML-Seite als PDF. Bilder sind relativ zum Repo-Ordner."""
    html = WURZEL / f".druck-{ziel.stem}.html"
    html.write_text(seite, encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory() as profil:
            subprocess.run(
                [browser(), "--headless=new", "--disable-gpu", f"--user-data-dir={profil}",
                 *(["--no-sandbox"] if os.name != "nt" else []), "--no-pdf-header-footer", f"--print-to-pdf={ziel}", html.as_uri()],
                check=True, timeout=120, capture_output=True)
    finally:
        html.unlink(missing_ok=True)
    print("Geschrieben:", ziel, ziel.stat().st_size, "Bytes")


def main():
    inhalt = umsetzen((WURZEL / "README.md").read_text(encoding="utf-8"))
    seite = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Wärmepumpe: Anleitung</title>'
             f"<style>{CSS}</style></head><body>{inhalt}</body></html>")
    drucken(seite, WURZEL / "Anleitung.pdf")


if __name__ == "__main__":
    main()
