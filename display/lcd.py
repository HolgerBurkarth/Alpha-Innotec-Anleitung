"""Vektor-Nachbildung der Anzeige der Alpha-Innotec-Wärmepumpe.

Enthält Symbole, eine Strichschrift und Bausteine für Anzeigen (Listen,
Zeiteingabe, Skala). Alles wird als reines SVG ausgegeben und braucht weder
Schriftarten noch Zusatzpakete.

Beispiel:
    from lcd import svg, symbol, zeitzeile
    bild = symbol("sonne", 40, 0, 14) + zeitzeile(1, "5:00", "5:30", 0, 20, marke="zeile")
    open("winter.svg", "w", encoding="utf-8").write(svg(bild, 96, 30, rand=4))
"""

LCD_HG = "#C8D5BC"   # Hintergrund der Anzeige
LCD_VG = "#28331F"   # Dunkle Bildpunkte

ZELLE_B = 6          # Breite einer Schriftzelle
ZELLE_H = 10         # Zeilenabstand

# ---------------------------------------------------------------------------
# Schrift: Striche auf einem Raster 5 x 7, Unterlängen bis y = 8.
# Punkte sind Linienzüge, ";" trennt Linienzüge, ein einzelner Punkt ist ein Tupfen.
# ---------------------------------------------------------------------------
_O = "1,0 3,0 4,1 4,5 3,6 1,6 0,5 0,1 1,0"
_A = "0,6 0,1.5 1.5,0 2.5,0 4,1.5 4,6 ; 0,3.7 4,3.7"
_U = "0,0 0,5 1,6 3,6 4,5 4,0"
_a = "0.5,2 3,2 4,3 4,6 ; 4,3.8 1,3.8 0,4.8 1,6 3,6 4,5"
_o = "1,2 3,2 4,3 4,5 3,6 1,6 0,5 0,3 1,2"
_u = "0,2 0,5 1,6 3,6 4,5 ; 4,2 4,6"

GLYPHEN = {
    "A": _A,
    "B": "0,0 3,0 4,1 4,2 3,3 0,3 ; 3,3 4,4 4,5 3,6 0,6 0,0",
    "C": "4,1 3,0 1,0 0,1 0,5 1,6 3,6 4,5",
    "D": "0,0 3,0 4,1 4,5 3,6 0,6 0,0",
    "E": "4,0 0,0 0,6 4,6 ; 0,3 3,3",
    "F": "4,0 0,0 0,6 ; 0,3 3,3",
    "G": "4,1 3,0 1,0 0,1 0,5 1,6 3,6 4,5 4,3 2,3",
    "H": "0,0 0,6 ; 4,0 4,6 ; 0,3 4,3",
    "I": "1,0 3,0 ; 2,0 2,6 ; 1,6 3,6",
    "J": "2,0 4,0 ; 3,0 3,5 2,6 1,6 0,5",
    "K": "0,0 0,6 ; 4,0 0,3.6 ; 1.3,2.5 4,6",
    "L": "0,0 0,6 4,6",
    "M": "0,6 0,0 2,3 4,0 4,6",
    "N": "0,6 0,0 4,6 4,0",
    "O": _O,
    "P": "0,6 0,0 3,0 4,1 4,2 3,3 0,3",
    "Q": _O + " ; 2.5,4.5 4,6",
    "R": "0,6 0,0 3,0 4,1 4,2 3,3 0,3 ; 2,3 4,6",
    "S": "4,1 3,0 1,0 0,1 0,2 1,3 3,3 4,4 4,5 3,6 1,6 0,5",
    "T": "0,0 4,0 ; 2,0 2,6",
    "U": _U,
    "V": "0,0 0,3 2,6 4,3 4,0",
    "W": "0,0 0,6 2,3.2 4,6 4,0",
    "X": "0,0 4,6 ; 4,0 0,6",
    "Y": "0,0 2,3 4,0 ; 2,3 2,6",
    "Z": "0,0 4,0 0,6 4,6",
    "Ä": _A.replace("0,6 0,1.5 1.5,0 2.5,0 4,1.5 4,6", "0,6 0,2.5 1.5,1 2.5,1 4,2.5 4,6").replace("0,3.7 4,3.7", "0,4.3 4,4.3") + " ; 1,-0.4 ; 3,-0.4",
    "Ö": "1,1 3,1 4,2 4,5 3,6 1,6 0,5 0,2 1,1 ; 1,-0.4 ; 3,-0.4",
    "Ü": "0,1 0,5 1,6 3,6 4,5 4,1 ; 1,-0.4 ; 3,-0.4",
    "a": _a,
    "b": "0,0 0,6 3,6 4,5 4,3 3,2 0,2",
    "c": "4,2 1,2 0,3 0,5 1,6 4,6",
    "d": "4,0 4,6 1,6 0,5 0,3 1,2 4,2",
    "e": "0,4 4,4 4,3 3,2 1,2 0,3 0,5 1,6 3.5,6",
    "f": "4,0 2.2,0 1.2,1 1.2,6 ; 0,3 3.2,3",
    "g": "4,2 1,2 0,3 0,4 1,5 4,5 ; 4,2 4,7 3,8 1,8",
    "h": "0,0 0,6 ; 0,3 1,2 3,2 4,3 4,6",
    "i": "1,2 2,2 2,6 ; 1,6 3,6 ; 2,0.2",
    "j": "2,2 3,2 3,7 2,8 1,8 ; 3,0.2",
    "k": "0,0 0,6 ; 3.5,2 0,4.3 ; 1.4,3.3 4,6",
    "l": "1,0 2,0 2,6 ; 1,6 3,6",
    "m": "0,6 0,2 ; 0,3 1,2 2,3 2,6 ; 2,3 3,2 4,3 4,6",
    "n": "0,6 0,2 ; 0,3 1,2 3,2 4,3 4,6",
    "o": _o,
    "p": "0,8 0,2 3,2 4,3 4,4 3,5 0,5",
    "q": "4,8 4,2 1,2 0,3 0,4 1,5 4,5",
    "r": "0,6 0,2 ; 0,3 1,2 3,2 4,3",
    "s": "4,2 1,2 0,3 1,4 3,4 4,5 3,6 0,6",
    "t": "1.2,0 1.2,5 2.2,6 4,6 ; 0,2 3.2,2",
    "u": _u,
    "v": "0,2 2,6 4,2",
    "w": "0,2 1,6 2,3.5 3,6 4,2",
    "x": "0,2 4,6 ; 4,2 0,6",
    "y": "0,2 0,4 1,5 4,5 ; 4,2 4,7 3,8 1,8",
    "z": "0,2 4,2 0,6 4,6",
    "ä": _a + " ; 1,0.4 ; 3,0.4",
    "ö": _o + " ; 1,0.4 ; 3,0.4",
    "ü": _u + " ; 1,0.4 ; 3,0.4",
    "ß": "0,6 0,1 1,0 3,0 4,1 4,2 3,3 ; 3,3 4,4 4,5 3,6 1,6",
    "0": _O + " ; 1,5 3,1",   # Null mit Schrägstrich wie am Gerät
    "1": "1,1 2,0 2,6 ; 1,6 3,6",
    "2": "0,1 1,0 3,0 4,1 4,2 0,6 4,6",
    "3": "0,1 1,0 3,0 4,1 4,2 3,3 1.5,3 ; 3,3 4,4 4,5 3,6 1,6 0,5",
    "4": "3,6 3,0 0,4 4,4",
    "5": "4,0 0,0 0,2.5 3,2.5 4,3.5 4,5 3,6 1,6 0,5",
    "6": "3.5,0 2,0 0,2 0,5 1,6 3,6 4,5 4,4 3,3 0,3",
    "7": "0,0 4,0 1.5,6",
    "8": "1,0 3,0 4,1 4,2 3,3 1,3 0,2 0,1 1,0 ; 1,3 0,4 0,5 1,6 3,6 4,5 4,4 3,3",
    "9": "0.5,6 2,6 4,4 4,1 3,0 1,0 0,1 0,2 1,3 4,3",
    ":": "1.7,1.4 2.3,1.4 2.3,2.2 1.7,2.2 1.7,1.4 ; 1.7,4.4 2.3,4.4 2.3,5.2 1.7,5.2 1.7,4.4",
    ".": "1.7,5.6 2.3,5.6 2.3,6 1.7,6 1.7,5.6",
    ",": "2,5.6 2,6.4 1.3,7.5",
    "-": "0.5,3 3.5,3",
    "−": "0.5,3 3.5,3",
    "+": "2,1 2,5 ; 0,3 4,3",
    "(": "3,0 2,1 1.5,2 1.5,4 2,5 3,6",
    ")": "1,0 2,1 2.5,2 2.5,4 2,5 1,6",
    "/": "0,6 4,0",
    "°": "1,0 2,0 2.6,0.6 2.6,1.2 2,1.8 1,1.8 0.4,1.2 0.4,0.6 1,0",
    "%": "0,6 4,0 ; 0.5,0.5 ; 3.5,5.5",
    "!": "2,0 2,4 ; 2,6",
    "?": "0,1 1,0 3,0 4,1 4,2 2,3.5 2,4.2 ; 2,6",
    "=": "0.5,2 3.5,2 ; 0.5,4 3.5,4",
    "_": "0,7 4,7",
    " ": "",
}


def _zuege(zeichen):
    roh = GLYPHEN.get(zeichen, GLYPHEN["?"])
    for teil in roh.split(";"):
        punkte = [tuple(float(v) for v in p.split(",")) for p in teil.split()]
        if len(punkte) == 1:          # Tupfen
            x, y = punkte[0]
            punkte = [(x, y), (x + 0.01, y)]
        if punkte:
            yield punkte


def _z(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def text(s, x, y, gr=1.0, farbe=LCD_VG, staerke=0.95):
    """Schreibt s ab Zellenposition (x, y). gr vergrößert die Schrift."""
    d = []
    for i, zeichen in enumerate(s):
        ox = x + i * ZELLE_B * gr
        for zug in _zuege(zeichen):
            d.append("M" + "L".join(f"{_z(ox + px * gr)} {_z(y + py * gr)}" for px, py in zug))
    if not d:
        return ""
    return (f'<path d="{"".join(d)}" fill="none" stroke="{farbe}" stroke-width="{_z(staerke * gr)}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def balken(x, y, b, h, farbe=LCD_VG):
    return f'<rect x="{_z(x)}" y="{_z(y)}" width="{_z(b)}" height="{_z(h)}" fill="{farbe}"/>'


# ---------------------------------------------------------------------------
# Symbole auf einer Fläche 24 x 24.
# rahmen: Umriss, der bei „invers“ gefüllt wird; koerper: Inhalt.
# herkunft: "Foto" = am Gerät belegt, "abgeleitet" = aus einem Foto hergeleitet.
# ---------------------------------------------------------------------------
_F = 'fill="currentColor" stroke="none"'
_BOX = '<rect x="2" y="2" width="20" height="20"/>'
_HAKEN = '<path d="M6.5 13.5L9.5 18L17.5 6.5"/>'

_ACHTECK = '<path d="M7 1.6H17L22 6.6V17.4L17 22.4H7L2 17.4V6.6Z"/>'
_PROPELLER = ('<g stroke-width="1.6">'
              '<path d="M12 12C12.4 8.4 14 5.4 16.6 5.2C19 5.1 19.4 8.2 17.4 9.9C15.8 11.2 13.6 11.8 12 12Z"/>'
              '<path d="M12 12C11.6 15.6 10 18.6 7.4 18.8C5 18.9 4.6 15.8 6.6 14.1C8.2 12.8 10.4 12.2 12 12Z"/>'
              '</g>'
              f'<circle cx="12" cy="12" r="1.5" {_F}/>')

_GLAESER = (
    '<g stroke-width="1.4">'
    '<path d="M1 7.5C1 11 3.5 13.6 6.4 13.6S10.8 12 11 9"/>'
    '<path d="M6.4 13.6V21.5M2.5 22.8Q6.4 20.5 10.5 22.8"/>'
    '<path d="M23 7.5C23 11 20.5 13.6 17.6 13.6S13.2 12 13 9"/>'
    '<path d="M17.6 13.6V21.5M13.5 22.8Q17.6 20.5 21.5 22.8"/>'
    '</g>'
    f'<g {_F}>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="0.55"/>' for x, y in
              ((4, 4), (6, 2.8), (8.2, 5.4), (5, 7), (15.6, 5.4), (18, 2.8), (20, 4.4), (18.4, 7)))
    + '</g>'
)

SYMBOLE = {
    "info": {
        "titel": "Informationen", "ort": "Hauptmenü M1", "herkunft": "Foto",
        "koerper": '<circle cx="12" cy="12" r="8.6"/><path d="M12 1.2V3.4M12 20.6V22.8"/>'
                   f'<circle cx="12" cy="7.8" r="1.3" {_F}/>'
                   '<path d="M10.2 11H12.2V16.4M10 16.6H14.6"/>',
    },
    "heizung": {
        "titel": "Fußbodenheizung", "ort": "Hauptmenü M2, Startanzeige", "herkunft": "Foto",
        "koerper": '<g stroke-width="2.4" stroke-linecap="butt">'
                   '<path d="M1.5 6H22.5M1.5 18.2H22.5"/>'
                   '<path d="M4.8 2.5V21.7M9.6 2.5V21.7M14.4 2.5V21.7M19.2 2.5V21.7"/></g>',
    },
    "warmwasser": {
        "titel": "Warmwasser", "ort": "Hauptmenü M3", "herkunft": "Foto",
        "koerper": '<g stroke-linecap="butt" stroke-linejoin="round">'
                   '<path d="M6.5 4.2H16" stroke-width="2.8"/>'
                   '<path d="M11.6 4.2V13" stroke-width="3.6"/>'
                   '<path d="M5 23V18.2Q5 14.6 9 14.6H19" stroke-width="4.4"/>'
                   '<path d="M20.4 8V21" stroke-width="3.6"/></g>',
    },
    "lueftung": {
        "titel": "Lüftung", "ort": "Hauptmenü M4, Kopf des Lüftungsmenüs", "herkunft": "Foto",
        "rahmen": _ACHTECK, "koerper": _PROPELLER,
    },
    "lueftung_uhr": {
        "titel": "Lüftung, Zeitplan", "ort": "Kopf der Zeiteingabe", "herkunft": "Foto", "markierbar": False,
        "rahmen": _ACHTECK,
        "koerper": _PROPELLER + f'<circle cx="7" cy="7" r="5.6" fill="{LCD_HG}" stroke-width="1.4"/>'
                                '<path d="M7 3.8V7L9.4 8.4" stroke-width="1.2"/>',
    },
    "werkzeug": {
        "titel": "Einstellungen", "ort": "Hauptmenü M5", "herkunft": "Foto",
        "koerper": '<g stroke-width="2.2">'
                   '<path d="M21 2.2H17.4L15.4 4.4V8.8L17.2 10.6H20.6L22.6 8.4"/>'
                   '<path d="M8 16L15.8 8.6" stroke-width="3"/>'
                   '<path d="M1.6 21.4V17.4L3.6 15.6H7.2L9 17.6V20.4L6.4 22.8H4.2"/></g>',
    },
    "zurueck": {
        "titel": "Zurück", "ort": "Hauptmenü, Abfrage am Ende", "herkunft": "Foto",
        "rahmen": _BOX,
        "koerper": f'<path d="M5.6 12L11.6 6.2V9.4H18.4V14.6H11.6V17.8Z" {_F}/>',
    },
    "weiter": {
        "titel": "Ins Menü", "ort": "Startanzeige", "herkunft": "Foto",
        "rahmen": _BOX,
        "koerper": f'<path d="M18.4 12L12.4 6.2V9.4H5.6V14.6H12.4V17.8Z" {_F}/>',
    },
    "ok": {
        "titel": "Speichern", "ort": "Abfrage am Ende", "herkunft": "Foto",
        "rahmen": _BOX, "koerper": _HAKEN,
    },
    "verwerfen": {
        "titel": "Verwerfen", "ort": "Abfrage am Ende", "herkunft": "Foto",
        "rahmen": _BOX, "koerper": _HAKEN + '<path d="M6.2 6.2L17.8 17.8"/>',
    },
    "sonne": {
        "titel": "Stärkere Stufe", "ort": "Zeitplan", "herkunft": "Foto",
        "koerper": '<circle cx="12" cy="12" r="3.6"/>'
                   '<path d="M12 1.5V6M12 18V22.5M4.4 4.4L8.6 8.6M15.4 15.4L19.6 19.6M19.6 4.4L15.4 8.6M8.6 15.4L4.4 19.6"/>',
    },
    "mond": {
        "titel": "Schwächere Stufe", "ort": "Zeitplan", "herkunft": "Foto",
        "koerper": '<path d="M16.5 2C10 3 5.8 7 5.8 12S10 21 16.5 22C13.2 19 11.4 15.8 11.4 12S13.2 5 16.5 2Z"/>',
    },
    "kaestchen_leer": {
        "titel": "Nicht gewählt", "ort": "Auswahl Schaltzeiten", "herkunft": "Foto",
        "rahmen": '<rect x="3.5" y="3.5" width="17" height="17"/>', "koerper": "",
        "markierbar": False,
    },
    "kaestchen_an": {
        "titel": "Gewählt", "ort": "Auswahl Schaltzeiten", "herkunft": "Foto",
        "rahmen": '<rect x="3.5" y="3.5" width="17" height="17"/>',
        "koerper": '<path d="M8 8L16 16M16 8L8 16"/>',
    },
    "party_aus": {
        "titel": "Party nicht aktiv", "ort": "Startanzeige", "herkunft": "Foto",
        "koerper": _GLAESER + '<path d="M1 1L23 23.2M22.6 1.2L1.8 23.4"/>',
    },
    "party": {
        "titel": "Party aktiv", "ort": "vermutlich Startanzeige", "herkunft": "abgeleitet",
        "koerper": _GLAESER,
    },
    "plus": {
        "titel": "Wärmer", "ort": "Startanzeige", "herkunft": "Foto",
        "koerper": '<path d="M12 4.5V19.5M4.5 12H19.5" stroke-width="3.6" stroke-linecap="butt"/>',
    },
    "minus": {
        "titel": "Kühler", "ort": "Startanzeige", "herkunft": "Foto",
        "koerper": '<path d="M4.5 12H19.5" stroke-width="3.6" stroke-linecap="butt"/>',
    },
}


def symbol(name, x=0, y=0, groesse=24, invers=False, vg=LCD_VG, hg=LCD_HG):
    """Setzt ein Symbol. invers = markierte Darstellung (hell auf dunkel)."""
    s = SYMBOLE[name]
    rahmen = s.get("rahmen")
    attr = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    if invers:
        flaeche = rahmen or '<rect x="0" y="0" width="24" height="24" rx="2"/>'
        inhalt = f'<g color="{vg}" fill="{vg}" stroke="{vg}" stroke-width="1.8" stroke-linejoin="round">{flaeche}</g>'
        inhalt += f'<g color="{hg}" {attr}>{s["koerper"]}</g>'
    else:
        inhalt = f'<g color="{vg}" {attr}>{rahmen or ""}{s["koerper"]}</g>'
    return f'<g transform="translate({_z(x)} {_z(y)}) scale({_z(groesse / 24)})">{inhalt}</g>'


def svg(inhalt, breite, hoehe, massstab=3, hg=LCD_HG, rand=0):
    """Rahmt Inhalt als eigenständiges SVG. hg=None lässt den Hintergrund frei."""
    b, h = breite + 2 * rand, hoehe + 2 * rand
    flaeche = f'<rect x="{-rand}" y="{-rand}" width="{b}" height="{h}" fill="{hg}"/>' if hg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-rand} {-rand} {b} {h}" '
            f'width="{b * massstab}" height="{h * massstab}">{flaeche}{inhalt}</svg>')


# ---------------------------------------------------------------------------
# Bausteine
# ---------------------------------------------------------------------------
def titel(s, x=0, y=0, breite=128, gr=1.32):
    """Überschrift mit Linie darunter, wie in den Menüs."""
    return text(s, x, y, gr=gr, staerke=1.4) + balken(x, y + 15.5, breite - x, 1.6)


def rollbalken(x, y, hoehe, position=0.5):
    """Senkrechter Rollbalken mit Pfeilen. position von 0 (oben) bis 1 (unten)."""
    mitte = x + 3.5
    knopf = y + 8 + (hoehe - 22) * position
    return (f'<path d="M{_z(mitte)} {y}L{x + 6.5} {y + 4.5}H{x + 0.5}Z" fill="{LCD_VG}"/>'
            f'<path d="M{_z(mitte)} {y + hoehe}L{x + 6.5} {y + hoehe - 4.5}H{x + 0.5}Z" fill="{LCD_VG}"/>'
            + balken(mitte - 0.4, y + 5, 0.8, hoehe - 10)
            + balken(mitte - 1.6, knopf, 3.2, 6))


def knoepfe(y, x_werte=(9, 49, 89), groesse=20, markiert=None):
    """Zurück, Speichern, Verwerfen am unteren Rand. markiert: Name des gewählten Knopfs."""
    namen = ("zurueck", "ok", "verwerfen")
    return "".join(symbol(n, x, y, groesse, invers=n == markiert) for n, x in zip(namen, x_werte))


def listenzeile(s, x, y, breite, markiert=False, kaestchen=None):
    """Menüzeile. kaestchen: None, True (gewählt) oder False (nicht gewählt)."""
    teile = []
    textbreite = breite - (11 if kaestchen is not None else 0)
    if markiert:
        teile.append(balken(x - 1, y - 1.6, textbreite + 1, 10.2))
    teile.append(text(s, x, y, farbe=LCD_HG if markiert else LCD_VG))
    if kaestchen is not None:
        name = "kaestchen_an" if kaestchen else "kaestchen_leer"
        teile.append(symbol(name, x + breite - 9, y - 1.4, groesse=9.5, invers=markiert and kaestchen))
    return "".join(teile)


_MARKEN = {
    "von_stunde": (3, 2), "von_minute": (6, 2),
    "bis_stunde": (11, 2), "bis_minute": (14, 2),
}


def zeitzeile(nr, von, bis, x=0, y=0, marke=None):
    """Zeile einer Zeiteingabe, z. B. 1: 5:00 - 5:30.

    marke: None, "zeile", "von_stunde", "von_minute", "bis_stunde", "bis_minute".
    """
    teile = []
    feld = None
    if marke == "zeile":
        teile.append(balken(x - 1, y - 1.6, ZELLE_B * 3 + 1, 10.2))
    elif marke:
        sp, n = _MARKEN[marke]
        feld = marke
        teile.append(balken(x + sp * ZELLE_B - 1, y - 1.6, n * ZELLE_B + 0.6, 10.2))

    def schreibe(s, spalte, hell=False):
        teile.append(text(s, x + spalte * ZELLE_B, y, farbe=LCD_HG if hell else LCD_VG))

    schreibe(f"{nr}:", 0, hell=marke == "zeile")

    for art, wert, ende in (("von", von, 7), ("bis", bis, 15)):
        h, m = wert.split(":")
        schreibe(h.rjust(2), ende - 4, hell=feld == f"{art}_stunde")
        schreibe(":", ende - 2)
        schreibe(m, ende - 1, hell=feld == f"{art}_minute")
    schreibe("-", 9)
    return "".join(teile)


def skala(x, y, felder=10, position=5, breite=12, feldhoehe=6, nulllinie=None):
    """Senkrechte Skala neben dem Wert. position zählt von oben ab 0."""
    teile = [f'<rect x="{x}" y="{y}" width="{breite}" height="{felder * feldhoehe}" '
             f'fill="none" stroke="{LCD_VG}" stroke-width="0.9"/>']
    for i in range(1, felder):
        yy = y + i * feldhoehe
        teile.append(balken(x, yy - 0.4, breite, 0.8))
    if nulllinie is not None:
        teile.append(balken(x - 3, y + nulllinie * feldhoehe - 0.45, breite + 6, 0.9))
    teile.append(balken(x + 3, y + position * feldhoehe + 1.2, breite - 6, feldhoehe - 2.4))
    return "".join(teile)
