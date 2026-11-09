"""QR-Code als Vektorgrafik (SVG), ohne Zusatzpakete.

Byte-Modus, Fehlerkorrektur M, Versionen 1 bis 6 (bis 106 Zeichen).
Das reicht für einen Link. Aufruf aus Python: qr.svg("https://…")
"""

# Version: (Codewörter gesamt, Korrektur-Codewörter je Block, Blöcke, Ausrichtungsmuster)
VERSIONEN = {
    1: (26, 10, 1, None), 2: (44, 16, 1, 18), 3: (70, 26, 1, 22),
    4: (100, 18, 2, 26), 5: (134, 24, 2, 30), 6: (172, 16, 4, 34),
}

EXP = [0] * 512
LOG = [0] * 256
_x = 1
for _i in range(255):
    EXP[_i] = _x
    LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    EXP[_i] = EXP[_i - 255]


def mal(a, b):
    return EXP[LOG[a] + LOG[b]] if a and b else 0


def korrektur(daten, n):
    """Reed-Solomon-Rest: n Korrektur-Codewörter zu den Daten."""
    gen = [1]
    for i in range(n):
        neu = [0] * (len(gen) + 1)
        for j, k in enumerate(gen):
            neu[j] ^= k
            neu[j + 1] ^= mal(k, EXP[i])
        gen = neu
    rest = [0] * n
    for b in daten:
        f = b ^ rest[0]
        rest = rest[1:] + [0]
        for j in range(n):
            rest[j] ^= mal(gen[j + 1], f)
    return rest


def codewoerter(text, version):
    gesamt, ec, bloecke, _ = VERSIONEN[version]
    kapazitaet = gesamt - ec * bloecke
    roh = text.encode("utf-8")
    bits = "0100" + f"{len(roh):08b}" + "".join(f"{b:08b}" for b in roh)
    bits += "0" * min(4, kapazitaet * 8 - len(bits))
    bits += "0" * (-len(bits) % 8)
    daten = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    fuell = [0xEC, 0x11]
    while len(daten) < kapazitaet:
        daten.append(fuell[(len(daten) - len(bits) // 8) % 2])
    groesse = kapazitaet // bloecke
    teile = [daten[i * groesse:(i + 1) * groesse] for i in range(bloecke)]
    rest = [korrektur(t, ec) for t in teile]
    aus = [t[i] for i in range(groesse) for t in teile]
    aus += [r[i] for i in range(ec) for r in rest]
    return aus


def maske_an(m, x, y):
    return (
        (x + y) % 2, y % 2, x % 3, (x + y) % 3, (x // 3 + y // 2) % 2,
        x * y % 2 + x * y % 3, (x * y % 2 + x * y % 3) % 2, ((x + y) % 2 + x * y % 3) % 2,
    )[m] == 0


def raster(text, version, maske):
    n = 17 + 4 * version
    feld = [[False] * n for _ in range(n)]
    fest = [[False] * n for _ in range(n)]

    def setze(x, y, an):
        feld[y][x] = an
        fest[y][x] = True

    for i in range(n):
        setze(6, i, i % 2 == 0)
        setze(i, 6, i % 2 == 0)
    for mx, my in ((3, 3), (n - 4, 3), (3, n - 4)):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                x, y = mx + dx, my + dy
                if 0 <= x < n and 0 <= y < n:
                    d = max(abs(dx), abs(dy))
                    setze(x, y, d not in (2, 4))
    pos = VERSIONEN[version][3]
    if pos:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                setze(pos + dx, pos + dy, max(abs(dx), abs(dy)) != 1)

    daten = maske  # Fehlerkorrektur M hat die Kennung 00
    rest = daten
    for _ in range(10):
        rest = (rest << 1) ^ ((rest >> 9) * 0x537)
    format_bits = ((daten << 10) | rest) ^ 0x5412
    bit = lambda i: (format_bits >> i) & 1 == 1
    for i in range(6):
        setze(8, i, bit(i))
    setze(8, 7, bit(6))
    setze(8, 8, bit(7))
    setze(7, 8, bit(8))
    for i in range(9, 15):
        setze(14 - i, 8, bit(i))
    for i in range(8):
        setze(n - 1 - i, 8, bit(i))
    for i in range(8, 15):
        setze(8, n - 15 + i, bit(i))
    setze(8, n - 8, True)

    folge = "".join(f"{b:08b}" for b in codewoerter(text, version))
    i = 0
    for rechts in range(n - 1, 0, -2):
        if rechts <= 6:
            rechts -= 1
        hoch = (rechts + 1) & 2 == 0
        for v in range(n):
            y = n - 1 - v if hoch else v
            for x in (rechts, rechts - 1):
                if not fest[y][x]:
                    wert = i < len(folge) and folge[i] == "1"
                    i += 1
                    feld[y][x] = wert != maske_an(maske, x, y)
    return feld


def strafe(feld):
    n = len(feld)
    gesamt = 0
    zeilen = feld + [[feld[y][x] for y in range(n)] for x in range(n)]
    for z in zeilen:
        lauf = 1
        for a, b in zip(z, z[1:]):
            if a == b:
                lauf += 1
                if lauf == 5:
                    gesamt += 3
                elif lauf > 5:
                    gesamt += 1
            else:
                lauf = 1
        s = "".join("1" if m else "0" for m in z)
        for muster in ("10111010000", "00001011101"):
            start = s.find(muster)
            while start >= 0:
                gesamt += 40
                start = s.find(muster, start + 1)
    for y in range(n - 1):
        for x in range(n - 1):
            if feld[y][x] == feld[y][x + 1] == feld[y + 1][x] == feld[y + 1][x + 1]:
                gesamt += 3
    dunkel = sum(map(sum, feld))
    return gesamt + 10 * ((abs(dunkel * 20 - n * n * 10) + n * n - 1) // (n * n) - 1)


def erzeugen(text):
    """Liefert das Raster (Liste von Zeilen mit True für dunkel)."""
    laenge = len(text.encode("utf-8"))
    for version, (gesamt, ec, bloecke, _) in VERSIONEN.items():
        if laenge + 2 <= gesamt - ec * bloecke:
            return min((raster(text, version, m) for m in range(8)), key=strafe)
    raise ValueError("Text ist zu lang für diesen QR-Erzeuger.")


def svg(text, breite="100%"):
    feld = erzeugen(text)
    n = len(feld) + 8  # vier Module Ruhezone auf jeder Seite
    pfad = "".join(f"M{x + 4} {y + 4}h1v1h-1z" for y, z in enumerate(feld) for x, an in enumerate(z) if an)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{breite}" '
            f'shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/>'
            f'<path d="{pfad}" fill="#000"/></svg>')
