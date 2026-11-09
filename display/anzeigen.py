"""Erzeugt die Anzeigen für die Anleitung als SVG in m/anzeige/.

Aufruf: python display/anzeigen.py
Eine neue Anzeige ist ein weiterer Eintrag in ANZEIGEN.
"""
from pathlib import Path

import lcd

ZIEL = Path(__file__).resolve().parent.parent / "m" / "anzeige"
BREITE, HOEHE = 145, 96
LISTE_X = 28
LISTE_Y = (30, 41, 52, 63)

WINTER_SONNE = [("5:00", "5:30"), ("12:30", "13:15")]
WINTER_MOND = [("17:30", "18:00"), ("0:00", "0:00")]


def anzeige(inhalt, hoehe=HOEHE, breite=BREITE):
    return lcd.svg(inhalt, breite, hoehe, massstab=3, rand=3)


def start(wert="-1.0°C", position=5):
    x = 8
    t = [
        lcd.text("Auto", x + 18, 16),
        lcd.symbol("party_aus", x + 14, 42, 30),
        lcd.balken(x + 54, 6, 0.9, 84),
        lcd.skala(x + 62, 17, felder=10, position=position, breite=14, feldhoehe=6.5),
        lcd.symbol("plus", x + 80, 18, 10),
        lcd.symbol("heizung", x + 106, 7, 18),
        lcd.text(wert, x + 83, 40),
        lcd.balken(x + 58, 49.7, 66, 0.9),
        lcd.symbol("minus", x + 80, 70, 10),
        lcd.symbol("weiter", x + 105, 68, 18, invers=True),
    ]
    return anzeige("".join(t))


def hauptmenue():
    t = [
        lcd.text("Wärmepumpe steht", 26, 8),
        lcd.text("seit:   06:08:06", 26, 18),
        lcd.text("keine Anforderung", 26, 29),
    ]
    for name, x in (("info", 26), ("heizung", 44), ("warmwasser", 62), ("lueftung", 80), ("werkzeug", 98)):
        t.append(lcd.symbol(name, x, 62, 17, invers=name == "lueftung"))
    t.append(lcd.symbol("zurueck", 7, 72, 19))
    t.append(lcd.text("Lüftung", 29, 84))
    return anzeige("".join(t))


def kopf(ueberschrift, sym="lueftung", gr=1.32):
    return lcd.symbol(sym, 5, 6.5, 22) + lcd.titel(ueberschrift, LISTE_X, 7, BREITE - 9, gr=gr)


def menue_lueftung(markiert):
    t = [kopf("Lüftung"), lcd.symbol("zurueck", 7, 73, 20)]
    for i, zeile in enumerate(("Betriebsart", "Zeitschaltprogramm", "Stosslüftung", "Informationen")):
        t.append(lcd.listenzeile(zeile, LISTE_X, LISTE_Y[i], BREITE - LISTE_X - 9, markiert=i == markiert))
    return anzeige("".join(t))


def stosslueftung(knopf=None):
    t = [kopf("Stosslüftung")]
    zeilen = ("Aktivieren", "Beenden", "STL ist beendet")
    for i, zeile in enumerate(zeilen):
        t.append(lcd.listenzeile(zeile, LISTE_X, LISTE_Y[i], BREITE - LISTE_X - 9, markiert=i == 0 and knopf is None))
    t.append(lcd.knoepfe(72, markiert=knopf))
    return anzeige("".join(t))


def betriebsart(gewaehlt):
    t = [kopf("Betriebsart:"), lcd.symbol("zurueck", 7, 73, 20)]
    for i, zeile in enumerate(("Automatik", "Party", "Ferien", "Aus")):
        an = zeile == gewaehlt
        t.append(lcd.listenzeile(zeile, LISTE_X, LISTE_Y[i], BREITE - LISTE_X - 9, markiert=an, kaestchen=an))
    return anzeige("".join(t))


def schaltzeiten():
    t = [kopf("Schaltzeiten")]
    zeilen = (("Woche(Mo-So)", True), ("5+2(Mo-Fr,Sa-So)", False), ("Tage(Mo,Di,...)", False))
    for i, (zeile, an) in enumerate(zeilen):
        t.append(lcd.listenzeile(zeile, LISTE_X, LISTE_Y[i], BREITE - LISTE_X - 9, markiert=i == 0, kaestchen=an))
    t.append(lcd.knoepfe(72))
    return anzeige("".join(t))


def woche(sym, zeilen, marke=None, unten=False, knopf=None):
    t = [lcd.symbol("lueftung_uhr", 5, 6.5, 22), lcd.titel("Lüftung Woche", LISTE_X, 7, BREITE - 9, gr=1.32)]
    t.append(lcd.text("Montag - Sonntag", LISTE_X, 29))
    t.append(lcd.rollbalken(13, 30, 39, position=1 if unten else 0))
    t.append(lcd.symbol(sym, 69, 37.2, 12))
    for i, (von, bis) in enumerate(zeilen):
        m = marke[1] if marke and marke[0] == i and knopf is None else None
        t.append(lcd.zeitzeile(i + 1, von, bis, 30, 51 + i * 10.5, marke=m))
    if unten:
        t.append(lcd.knoepfe(73, markiert=knopf))
    else:
        t.append(lcd.symbol("zurueck", 9, 73, 20))
    return anzeige("".join(t))


def dreiecke():
    """Schemazeichnung des Formstücks nach Betriebsanleitung Seite 28."""
    gross = "M46 12V82H116L92 58L98 52L72 26L66 32L46 12Z"
    klein = "M54 6H122V74L100 52L106 46L78 18L72 24L54 6Z"
    t = [
        f'<path d="{gross}" fill="{lcd.LCD_VG}"/>',
        f'<path d="{klein}" fill="#6F7F63"/>',
        lcd.text("gross", 8, 64),
        lcd.text("klein", 124, 28, gr=0.9),
    ]
    return lcd.svg("".join(t), 156, 88, massstab=3, rand=3, hg="#FFFFFF")


ANZEIGEN = {
    "dreiecke": dreiecke,
    "start": start,
    "hauptmenue": hauptmenue,
    "lueftung-betriebsart": lambda: menue_lueftung(0),
    "lueftung-zeitprogramm": lambda: menue_lueftung(1),
    "lueftung-stosslueftung": lambda: menue_lueftung(2),
    "stoss-aktivieren": stosslueftung,
    "stoss-speichern": lambda: stosslueftung("ok"),
    "betriebsart-automatik": lambda: betriebsart("Automatik"),
    "betriebsart-aus": lambda: betriebsart("Aus"),
    "schaltzeiten": schaltzeiten,
    "woche-sonne": lambda: woche("sonne", WINTER_SONNE, (0, "zeile")),
    "woche-sonne-stunde": lambda: woche("sonne", WINTER_SONNE, (0, "von_stunde")),
    "woche-mond": lambda: woche("mond", WINTER_MOND, (0, "zeile"), unten=True),
    "woche-speichern": lambda: woche("mond", WINTER_MOND, unten=True, knopf="ok"),
}


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for alt in ZIEL.glob("*.svg"):
        alt.unlink()
    for name, baue in ANZEIGEN.items():
        (ZIEL / f"{name}.svg").write_text(baue(), encoding="utf-8")
    print(len(ANZEIGEN), "Anzeigen in", ZIEL)


if __name__ == "__main__":
    main()
