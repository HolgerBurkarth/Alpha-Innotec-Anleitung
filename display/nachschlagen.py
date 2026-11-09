"""Erzeugt Nachschlagebuch.pdf aus Nachschlagebuch.md.

Aufruf: python display/nachschlagen.py
Umbau, Monate und Lüftungspläne kommen aus der README, es gibt sie also nur einmal.
"""
import re
from urllib.parse import quote

import anzeigen
import aushang
import pdf
import qr

README = (pdf.WURZEL / "README.md").read_text(encoding="utf-8")
UMBRUCH = r'\s*<div style="page-break-after: always;"></div>\s*$'

CSS = """
th,td{padding:2pt 5pt}
.plan{display:flex;gap:12pt;align-items:center;break-inside:avoid;margin:0 0 9pt}
.gh{float:right;width:2.8cm;margin:0 0 4pt 10pt;text-align:center;font-size:8pt;line-height:1.15}
.gh a{color:inherit;text-decoration:none}
.gh svg{display:block}
.plan .name{width:3.4cm;flex:none}
.plan .name strong{font-size:13pt;display:block}
.plan .name span{font-size:10pt}
.plan svg{height:3.4cm;width:auto;display:block}
"""


def abschnitt(titel):
    """Holt einen Abschnitt samt Überschrift aus der README."""
    m = re.search(rf"^(#+) {re.escape(titel)}\s*$", README, re.M)
    if not m:
        raise SystemExit(f"Abschnitt nicht in der README gefunden: {titel}")
    rest = README[m.end():]
    ende = re.search(rf"^#{{1,{len(m[1])}}} ", rest, re.M)
    return m[0] + re.sub(UMBRUCH, "\n", rest[:ende.start()] if ende else rest)


def link(titel=None):
    """GitHub-Adresse der ganzen Anleitung oder eines Abschnitts."""
    if not titel:
        return aushang.LINK
    abschnitt(titel)  # meldet einen Fehler, wenn es den Abschnitt nicht gibt
    return f"{aushang.LINK}#{quote(pdf.anker(titel), safe='-')}"


def github(titel=None):
    """Klickbarer QR-Code zu GitHub, steht rechts neben dem Text."""
    url = link(titel)
    wort = "Dieses Kapitel" if titel else "Ganze Anleitung"
    return f'<div class="gh"><a href="{url}">{qr.svg(url)}{wort} auf GitHub</a></div>'


def einfuegen(m):
    """Setzt einen README-Abschnitt ein, auf Wunsch mit QR-Code unter der Überschrift."""
    teil = abschnitt(m[1])
    if m[2]:
        kopf, rest = teil.split("\n", 1)
        teil = f"{kopf}\n\n{github(m[1])}\n{rest}"
    return teil


def uhrzeit(s):
    """05:00 wird wie am Gerät zu 5:00."""
    return re.sub(r"^0(\d:)", r"\1", s)


def plaene():
    """Liest die Pläne aus der README und zeichnet je Plan beide Anzeigen."""
    monate = {}
    for monat, plan in re.findall(r"^\| ([^|*]+?) \| [^|]+ \| [^|]*?Plan (\w+)", abschnitt("Monat für Monat"), re.M):
        monate.setdefault(plan, []).append(monat)

    werte, name = {}, None
    zeile = r"^\| (?:\*\*(\w+)\*\*)? *\| \d \| (\S+) – (\S+) \| (\S+) – (\S+) \|"
    for plan, von1, bis1, von2, bis2 in re.findall(zeile, abschnitt("Die Lüftungspläne"), re.M):
        name = plan or name
        sonne, mond = werte.setdefault(name, ([], []))
        sonne.append((uhrzeit(von1), uhrzeit(bis1)))
        mond.append((uhrzeit(von2), uhrzeit(bis2)))
    if set(werte) != set(monate) or not werte:
        raise SystemExit(f"Pläne und Monate passen nicht zusammen: {sorted(werte)} / {sorted(monate)}")

    aus = []
    for name, (sonne, mond) in werte.items():
        aus.append(f'<div class="plan"><div class="name"><strong>Plan {name}</strong>'
                   f'<span>{", ".join(monate[name])}</span></div>'
                   f'{anzeigen.woche("sonne", sonne)}{anzeigen.woche("mond", mond, unten=True)}</div>')
    return "\n".join(aus)


def main():
    text = (pdf.WURZEL / "Nachschlagebuch.md").read_text(encoding="utf-8")
    text = re.sub(r"<!--\s*aus-readme:\s*(.+?)(\s*\|\s*github)?\s*-->", einfuegen, text)
    text = re.sub(r"<!--\s*github(?::\s*(.+?))?\s*-->", lambda m: github(m[1]), text)
    text = re.sub(r"<!--\s*lueftungsplaene\s*-->", lambda m: plaene(), text)
    seite = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Wärmepumpe: Nachschlagebuch</title>'
             f"<style>{pdf.CSS}{CSS}</style></head><body>{pdf.umsetzen(text)}</body></html>")
    pdf.drucken(seite, pdf.WURZEL / "Nachschlagebuch.pdf")


if __name__ == "__main__":
    main()
