"""Erzeugt Aushang.pdf: eine A4-Seite für neben die Anlage, mit QR-Code zur Anleitung.

Aufruf: python display/aushang.py
Der Inhalt steht bewusst hier und nicht in der README, er muss auf eine Seite passen.
"""
import pdf
import qr

LINK = "https://github.com/HolgerBurkarth/Alpha-Innotec-Anleitung"


def sym(name, alt):
    return f'<img class="sym" src="display/symbole/{name}.svg" alt="{alt}">'


PFEIL = sym("weiter_markiert", "Pfeil")
LUEFTUNG = sym("lueftung", "Lüftungssymbol")
ZU = '<span class="w">›</span>'

CSS = """
@page{size:A4;margin:12mm 14mm}
*{box-sizing:border-box}
body{margin:0;font:12pt/1.3 "Segoe UI",Arial,sans-serif;color:#1c1c1c}
h1{font-size:25pt;line-height:1.1;margin:0 0 2pt}
.unter{font-size:14pt;margin:0 0 9pt}
h2{font-size:14.5pt;margin:11pt 0 5pt;border-bottom:1.5pt solid #5b7a4a;padding-bottom:1pt}
.oben{display:flex;gap:14pt;align-items:center}
.oben img{height:2.8cm;flex:none}
.oben p{margin:0 0 5pt}
table{border-collapse:collapse;width:100%}
td{border:.6pt solid #b8bdb2;padding:4pt 6pt;vertical-align:top}
td:first-child{width:27%;font-weight:600;background:#eef3e9}
.sym{height:15pt;vertical-align:-3pt}
.w{color:#5b7a4a;font-weight:700;padding:0 1pt}
ul{margin:0;padding-left:15pt}
li{margin:0 0 2pt}
.rot{border-left:3pt solid #b3261e;background:#fbeeec;padding:6pt 9pt;margin:10pt 0 0}
.fuss{display:flex;gap:14pt;align-items:center;margin-top:11pt;border:1pt solid #5b7a4a;padding:7pt 10pt}
.qr{width:3.4cm;height:3.4cm;flex:none}
.qr svg{display:block}
.fuss strong.t{font-size:15pt;display:block}
.fuss p{margin:0 0 3pt}
.url{font-size:9.5pt;overflow-wrap:anywhere}
"""

INHALT = f"""
<h1>Wärmepumpe: Das Wichtigste</h1>
<p class="unter">Die Anlage läuft von selbst. <strong>Im Alltag müsst ihr nichts tun.</strong></p>

<div class="oben">
  <img src="m/anzeige/start.svg" alt="Startanzeige">
  <div>
    <p><strong>So sieht es normal aus:</strong> links steht <strong>Auto</strong>, rechts ein kleiner Wert, zum Beispiel −1.0°C.</p>
    <p><strong>Drehknopf:</strong> <strong>Drehen</strong> wählt aus, <strong>Drücken</strong> bestätigt.
    Passiert nichts, kurz warten und noch einmal drücken.</p>
  </div>
</div>

<h2>Was tun?</h2>
<table>
<tr><td>Zu kalt oder zu warm</td><td>Den Wert rechts <strong>einen</strong> Schritt ändern: <strong>[+]</strong> wärmer, <strong>[−]</strong> kühler. Dann <strong>einen Tag warten</strong>.</td></tr>
<tr><td>Luft ist stickig</td><td>Stoßlüftung: {PFEIL} {ZU} {LUEFTUNG} {ZU} Stosslüftung {ZU} Aktivieren {ZU} Haken. Hört nach etwa einer Stunde von selbst auf.</td></tr>
<tr><td>Draußen stinkt es</td><td>{PFEIL} {ZU} {LUEFTUNG} {ZU} Betriebsart {ZU} <strong>Aus</strong>. Danach unbedingt wieder <strong>Automatik</strong> wählen.</td></tr>
<tr><td>„Wärmepumpe steht“, Lüftung still</td><td>Normal. Es wird gerade keine Wärme gebraucht, und die Lüftung läuft nach Plan nur zeitweise.</td></tr>
<tr><td>Kein warmes Wasser</td><td>Nach viel Verbrauch ein bis zwei Stunden warten. Nach einem halben Tag Fachbetrieb anrufen.</td></tr>
<tr><td>Anzeige dunkel</td><td>Nach Stromausfall eine Stunde warten. Sonst eine ausgelöste Sicherung der Wärmepumpe <strong>einmal</strong> einschalten.</td></tr>
</table>

<h2>Bitte nicht</h2>
<ul>
<li>Die Anlage ausschalten oder die Sicherung abschalten, auch nicht im Sommer oder im Urlaub.</li>
<li>Das Menü Einstellungen {sym("werkzeug", "Schraubenschlüssel")} öffnen.</li>
<li>Mehrmals hintereinander am Wert drehen. Die Fußbodenheizung braucht Stunden.</li>
</ul>

<h2>Einmal im Jahr</h2>
<ul>
<li><strong>Spätestens im Oktober:</strong> Die Lüftung muss im Winter-Zustand sein und auf <strong>Automatik</strong> stehen. Wie das geht, steht in der ganzen Anleitung.</li>
</ul>

<div class="rot"><strong>Störung, Wasser am Boden oder Heizung fällt aus:</strong> Foto der Anzeige machen, nichts verstellen, nicht ausschalten.
Fachbetrieb suchen: Aufkleber am Gerät, alte Rechnungen oder Hersteller ait-deutschland (alpha innotec), <strong>Telefon 09228 9906-0</strong>.</div>

<div class="fuss">
  <div class="qr">{qr.svg(LINK)}</div>
  <div>
    <strong class="t">Die ganze Anleitung</strong>
    <p>Mit dem Handy scannen: Umbau der Lüftung für Winter und Sommer, Filter, Lüftungspläne und wen man anruft.</p>
    <p class="url">{LINK}</p>
  </div>
</div>
"""


def main():
    seite = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Wärmepumpe: Aushang</title>'
             f"<style>{CSS}</style></head><body>{INHALT}</body></html>")
    pdf.drucken(seite, pdf.WURZEL / "Aushang.pdf")


if __name__ == "__main__":
    main()
