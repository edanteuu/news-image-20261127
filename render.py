#!/usr/bin/env python3
"""Render the v2 entry image for make.fun bounty news-image-20261127.

Draws one 1024x1024 broadsheet summing up Friday 27 November 2026:
40 verified stories across 10 regions, 3 lead cards with data-viz scenes,
10 illustrated medium panels, a numbers sidebar, a UTC timeline, a schematic
map, a 27-item list and a date-check strip. Pillow, build time only.
The graded program is main.py (stdlib only), which copies entry.png to the
output directory. All 40 stories were verified as happening, or first
reported, on Friday 27 November 2026 in some time zone; labels are
OFFICIAL (confirmed by an authority), REPORTED (named outlet) or CLAIM
(one party's claim, not independently confirmed). Research cutoff:
27 Nov 2026 23:59 UTC. Run: python3 render.py
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (96, 96, 96)
FAINT = (238, 234, 222)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY = (16, 42, 80)
TEAL = (14, 90, 90)
GOLD = (184, 134, 11)
SKY = (214, 230, 242)
GREEN = (28, 120, 60)
PURPLE = (96, 60, 140)
ORANGE = (200, 100, 20)
BROWN = (120, 80, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Wrap text to a pixel width; returns a list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if not words:
            lines.append("")
    return lines


def draw_wrapped(d, xy, text, fnt, fill, width, leading=None, max_lines=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    lines = wrap(d, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y, len(lines)


def truncate(d, text, fnt, width):
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "\u2026"


TAG_COLOUR = {"OFFICIAL": NAVY, "REPORTED": TEAL, "CLAIM": RED}

# ---------------- verified story data (27 Nov 2026, full day) ----------------
# Leads: n, city, field, tag, source, colour, art, headline, deck, stat line
LEADS = [
    dict(n=1, city="NEW YORK", field="MARKETS", tag="REPORTED", source="AP",
         colour=NAVY, art="sp",
         headline="Wall St caps its best week since April 2025",
         deck="S&P +1.60% to 7,297.49; Nasdaq +2.31%, Dow +1.18%.",
         stat="WEEK: S&P +5.6% \u00b7 NASDAQ +6.7%"),
    dict(n=2, city="BRUSSELS", field="ECB", tag="OFFICIAL", source="CONSILIUM",
         colour=TEAL, art="ecb",
         headline="EU names De Cos next ECB president",
         deck="De Cos succeeds Lagarde on 7 Feb 2027.",
         stat="ANNOUNCED 00:30 UTC"),
    dict(n=3, city="WELLINGTON", field="ELECTION", tag="REPORTED", source="ELECTORAL COMMISSION",
         colour=RED, art="parliament",
         headline="NZ coalition falls one seat short in final count",
         deck="National, ACT, NZ First: 65/130.",
         stat="66 NEEDED FOR A MAJORITY"),
]

# Medium panels: n, city, region, tag, source, art, headline, deck
MEDIUM = [
    dict(n=4, city="LUDZA", region="EUROPE", tag="REPORTED", source="Reuters \u00b7 ERR",
         art="drone", headline="Drones breach Latvia; NATO jets scramble",
         deck="Drone enters Latvia; Estonia alerts."),
    dict(n=5, city="NEW YORK", region="N AMERICA", tag="REPORTED", source="Adobe",
         art="market", headline="Black Friday opens: $12.9bn day ahead",
         deck="Adobe forecasts $12.9bn online sales."),
    dict(n=6, city="TOKYO", region="E ASIA", tag="REPORTED", source="Reuters",
         art="tokyo", headline="Tokyo inflation 2.9%; Nikkei jumps 2.11%",
         deck="Core CPI at 16-mo high; Nikkei 58,711."),
    dict(n=7, city="HORMUZ", region="MID EAST", tag="CLAIM", source="IRGC \u00b7 Fars",
         art="tanker", headline="Iran says tanker hit its mines in Hormuz",
         deck="IRGC: tanker hit mines; second turned back."),
    dict(n=8, city="MADRID", region="EUROPE", tag="REPORTED", source="Reuters",
         art="rally", headline="Spain's campaign ends; vote Sunday",
         deck="\u201cI can't conceive of us losing\u201d \u2014 PM."),
    dict(n=9, city="BOGOR", region="SE ASIA", tag="OFFICIAL", source="Basarnas",
         art="mine", headline="Indonesia mine: toll rises to 27",
         deck="All 13 dead identified; 14 still missing."),
    dict(n=10, city="WALLDORF", region="EUROPE", tag="REPORTED", source="Bloomberg",
         art="sap", headline="SAP weighs 10,000+ job cuts in AI push",
         deck="SAP plans ~9% cuts; no decision yet."),
    dict(n=11, city="ULLEUNG", region="E ASIA", tag="REPORTED", source="Reuters",
         art="boat", headline="Seoul sends six North Koreans home; one stays",
         deck="Six fishermen repatriated by sea; the seventh stays."),
    dict(n=12, city="MELBOURNE", region="OCEANIA", tag="REPORTED", source="AFL",
         art="footy", headline="North Melbourne seal AFLW three-peat, 44-18",
         deck="Kangaroos beat Melbourne in the rain."),
    dict(n=13, city="MARSEILLE", region="EUROPE", tag="REPORTED", source="AFP",
         art="stadium", headline="Macron condemns Marseille",
         deck="Five Levski fans in hospital; UEFA probes."),
]

# List: n, region, headline, source, tag
MORE = [
    (14, "EUROPE", "EU budget deadlock", "Consilium", "OFFICIAL"),
    (15, "MID EAST", "Iran denies strike", "NY Post", "CLAIM"),
    (16, "E ASIA", "Taiwan final day; 26 jets", "Reuters", "REPORTED"),
    (17, "E ASIA", "Kim vows bigger arsenal", "KCNA \u00b7 AP", "REPORTED"),
    (18, "GLOBAL", "Gold off 15-mo low", "CNBC", "REPORTED"),
    (19, "GLOBAL", "Amazon strike, 20+ nations", "UNI Global", "REPORTED"),
    (20, "EUROPE", "Serbia picks president", "AP", "REPORTED"),
    (21, "MID EAST", "Antonelli tops practice", "F1", "REPORTED"),
    (22, "N AMERICA", "Storm: 500,000+ out", "Reuters", "REPORTED"),
    (23, "GLOBAL", "Seaborne trade to flatline", "UNCTAD", "REPORTED"),
    (24, "N AMERICA", "Strobe Talbott dies at 80", "Wire", "REPORTED"),
    (25, "AFRICA", "Egypt detains driver", "Wire", "OFFICIAL"),
    (26, "EUROPE", "France cyber warning", "Wire", "REPORTED"),
    (27, "EUROPE", "Meloni: EU 'far' from deal", "Reuters", "REPORTED"),
    (28, "EUROPE", "Zelensky rebukes jibe", "Wire", "REPORTED"),
    (29, "EUROPE", "Turkey summons envoy", "Wire", "REPORTED"),
    (30, "MID EAST", "Eisenkot eyes cabinet", "Wire", "REPORTED"),
    (31, "S ASIA", "Islamabad defence talks", "Wire", "REPORTED"),
    (32, "S ASIA", "Pakistan checks Libya", "Dawn", "REPORTED"),
    (33, "OCEANIA", "ACCC warns on AI deals", "ABC", "REPORTED"),
    (34, "OCEANIA", "Hunter rail strike off", "ABC", "REPORTED"),
    (35, "MID EAST", "Ugochukwu F2 debut pole", "FIA F2", "REPORTED"),
    (36, "AFRICA", "RSF raids kill 14", "Anadolu", "REPORTED"),
    (37, "E ASIA", "Hong Kong fire anniversary", "AP", "REPORTED"),
    (38, "EUROPE", "FTSE 100 closes up 0.8%", "Reuters", "REPORTED"),
    (39, "LAT AM", "Ex-BRB chief stays jailed", "STF", "REPORTED"),
    (40, "N AMERICA", "SpaceX shares for kids", "CNBC", "REPORTED"),
]

NUMBERS = [
    ("65/130", "NZ coalition seats in the final count \u2014 66 needed for a majority"),
    ("+5.6%", "S&P 500's best week since April 2025; +1.60% on Friday to 7,297.49"),
    ("2.9%", "Tokyo core inflation in November \u2014 a 16-month high"),
    ("44\u201318", "North Melbourne's AFLW three-peat over Melbourne in the rain"),
    ("10,000+", "SAP jobs at risk as the software giant rebuilds around AI"),
    ("$12.9bn", "Forecast US Black Friday online sales, up 9.2% on last year"),
]

TIMELINE = [
    ("00:30", "De Cos ECB chief"),
    ("01:00", "NZ count 65/130"),
    ("03:00", "Mine toll rises to 27"),
    ("04:40", "Estonia air alert"),
    ("06:00", "Nikkei +2.11%"),
    ("11:00", "AFLW 44\u201318"),
    ("18:00", "S&P +1.60%"),
    ("23:00", "Spain rallies end"),
]

CHIPS = [
    ("EUROPE 12", NAVY), ("N AMERICA 5", RED), ("MIDDLE EAST 5", TEAL),
    ("EAST ASIA 5", PURPLE), ("OCEANIA 4", GREEN), ("GLOBAL 3", (90, 90, 90)),
    ("AFRICA 2", BROWN), ("S ASIA 2", ORANGE), ("SE ASIA 1", (70, 110, 130)),
    ("LATIN AMERICA 1", (140, 40, 90)),
]

# Map pins: story number -> (lon, lat). Illustrated stories 1-13 only.
PINS = {
    1: (-74.0, 40.7), 2: (4.35, 50.85), 3: (174.8, -41.3), 4: (27.8, 57.5),
    5: (-74.0, 40.7), 6: (139.7, 35.7), 7: (56.5, 26.5), 8: (-3.7, 40.4),
    9: (106.8, -6.6), 10: (8.6, 49.3), 11: (130.9, 37.5), 12: (145.0, -37.8),
    13: (5.4, 43.3),
}
PIN_JITTER = {5: (14, -12), 2: (-12, -10), 10: (12, 8), 13: (-12, 10), 4: (10, -10)}


# ---------------- drawn scenes (flat vector art, no external images) ----------------
def _skyline(d, x, y, w, h, colour=(30, 45, 70)):
    """Row of dark buildings along the bottom of a scene box."""
    base = y + h
    widths = [18, 26, 14, 30, 20, 24, 16]
    cx = x + 2
    i = 0
    while cx < x + w - 4:
        bw = widths[i % len(widths)]
        bh = 18 + ((i * 37) % 34)
        d.rectangle([cx, base - bh, cx + bw, base], fill=colour)
        for wy in range(base - bh + 5, base - 4, 9):
            for wx in range(cx + 4, cx + bw - 3, 8):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 220, 120))
        cx += bw + 3
        i += 1


def art_sp(d, x, y, w, h):
    """Wall St: night skyline with a rising S&P line and a green stat chip."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 28, 52))
    for sx, sy in [(x + 20, y + 8), (x + 60, y + 18), (x + 150, y + 6), (x + 190, y + 16)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    _skyline(d, x, y + 22, w, h - 22)
    pts = [(x + 6, y + h - 26), (x + 45, y + h - 38), (x + 80, y + h - 30),
           (x + 120, y + h - 52), (x + 160, y + h - 62), (x + 200, y + h - 78),
           (x + w - 6, y + 18)]
    d.line(pts, fill=(60, 200, 90), width=4, joint="curve")
    d.polygon([(x + w - 16, y + 12), (x + w - 4, y + 24), (x + w - 18, y + 26)], fill=(60, 200, 90))
    d.rectangle([x + 8, y + 6, x + 118, y + 26], fill=(28, 120, 60))
    d.text((x + 12, y + 16), "S&P +1.60%  7,297.49", font=font(SANS_B, 13),
           fill=(255, 255, 255), anchor="lm")


def art_parliament(d, x, y, w, h):
    """NZ: semicircle of 130 seat dots — 65 navy, 7 gold, 58 grey — over '65/130'."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 224))
    cx, cy = x + w // 2, y + h - 16
    colours = [NAVY] * 65 + [GOLD] * 7 + [(120, 120, 125)] * 58
    arcs = [(86, 46), (70, 40), (54, 28), (38, 16)]
    idx = 0
    for radius, count in arcs:
        for i in range(count):
            if idx >= 130:
                break
            ang = math.pi * (1 - (i + 0.5) / count)
            px = cx + int(radius * math.cos(ang))
            py = cy - int(radius * math.sin(ang) * 0.82)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=colours[idx])
            idx += 1
    d.rectangle([x + w // 2 - 46, y + h - 30, x + w // 2 + 46, y + h - 6], fill=NAVY)
    d.text((x + w // 2, y + h - 18), "65 / 130", font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="mm")


def art_ecb(d, x, y, w, h):
    """ECB: classical bank building under a ring of EU stars, ribbon '7 FEB 2027'."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    bx, bw = x + 28, w - 56
    d.polygon([(bx, y + 34), (bx + bw // 2, y + 12), (bx + bw, y + 34)], fill=NAVY)
    d.rectangle([bx, y + 34, bx + bw, y + h - 8], fill=(220, 224, 232))
    for i in range(6):
        cx = bx + 12 + i * (bw - 24) // 5
        d.rectangle([cx - 4, y + 40, cx + 4, y + h - 14], fill=NAVY)
    d.rectangle([bx - 4, y + h - 14, bx + bw + 4, y + h - 8], fill=NAVY)
    for i in range(12):
        ang = 2 * math.pi * i / 12
        sx = x + w - 30 + int(15 * math.cos(ang))
        sy = y + 16 + int(15 * math.sin(ang))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    d.rectangle([x + 8, y + h - 24, x + 108, y + h - 6], fill=GOLD)
    d.text((x + 58, y + h - 15), "7 FEB 2027", font=font(SANS_B, 12),
           fill=(255, 255, 255), anchor="mm")


def art_drone(d, x, y, w, h):
    """Baltic drones: grey sky, quadcopter silhouette, red dashed flight path."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 228))
    for cx, cy, s in [(x + 18, y + 10, 16), (x + 120, y + 6, 20), (x + 190, y + 16, 14)]:
        d.ellipse([cx, cy, cx + s, cy + s // 2], fill=(255, 255, 255))
    dx, dy = x + w // 2, y + h // 2 - 6
    d.ellipse([dx - 22, dy - 8, dx + 22, dy + 8], fill=(40, 40, 52))
    d.ellipse([dx - 6, dy - 14, dx + 6, dy + 2], fill=(90, 90, 105))
    for sx in (dx - 30, dx + 30):
        d.line([sx - 12, dy - 12, sx + 12, dy - 12], fill=(40, 40, 52), width=3)
    d.line([dx - 14, dy + 8, dx - 18, dy + 18], fill=(40, 40, 52), width=2)
    d.line([dx + 14, dy + 8, dx + 18, dy + 18], fill=(40, 40, 52), width=2)
    for i in range(8):
        px = x + 6 + i * (w - 12) // 7
        py = y + h - 12 - int(10 * math.sin(i * 1.1))
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.arc([x + w - 52, y + h - 40, x + w - 4, y + h + 8], 180, 330, fill=RED, width=2)
    d.arc([x + w - 40, y + h - 28, x + w - 16, y + h - 4], 180, 330, fill=RED, width=2)


def art_market(d, x, y, w, h):
    """Black Friday: striped awning, shopfront, shopping bags, % tag."""
    d.rectangle([x, y, x + w, y + h], fill=(246, 238, 220))
    for i in range(7):
        col = RED if i % 2 == 0 else (255, 255, 255)
        d.polygon([(x + i * (w // 7), y + 8), (x + (i + 1) * (w // 7), y + 8),
                   (x + (i + 1) * (w // 7) - 4, y + 26), (x + i * (w // 7) + 4, y + 26)], fill=col)
    d.rectangle([x + 6, y + 30, x + w - 6, y + h - 6], fill=(90, 60, 40))
    d.rectangle([x + 14, y + 38, x + w - 14, y + h - 14], fill=(60, 40, 28))
    d.rectangle([x + 20, y + 44, x + w // 2 - 8, y + h - 22], fill=(255, 230, 140))
    d.rectangle([x + w // 2 + 8, y + 44, x + w - 20, y + h - 22], fill=(140, 200, 220))
    for bx, col in [(x + 30, RED), (x + 66, TEAL), (x + 102, GOLD)]:
        d.polygon([(bx, y + h - 26), (bx + 26, y + h - 26), (bx + 22, y + h - 6),
                   (bx + 4, y + h - 6)], fill=col)
    d.ellipse([x + w - 34, y + 4, x + w - 4, y + 34], fill=RED)
    d.text((x + w - 19, y + 19), "%", font=font(SANS_B, 18), fill=(255, 255, 255), anchor="mm")


def art_tokyo(d, x, y, w, h):
    """Tokyo: skyline, red tower, green rising arrow, big 2.9%."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 246))
    _skyline(d, x, y + 34, w, h - 34, colour=(70, 85, 110))
    tx = x + w - 34
    d.polygon([(tx, y + 6), (tx + 6, y + 22), (tx + 4, y + 22), (tx + 4, y + h - 34),
               (tx - 4, y + h - 34), (tx - 4, y + 22), (tx - 6, y + 22)], fill=RED)
    d.line([x + 8, y + h - 14, x + w - 8, y + 12], fill=GREEN, width=4)
    d.polygon([(x + w - 20, y + 6), (x + w - 4, y + 14), (x + w - 22, y + 18)], fill=GREEN)
    d.text((x + 8, y + 10), "2.9%", font=font(SANS_B, 22), fill=RED)


def art_tanker(d, x, y, w, h):
    """Hormuz: sea, tanker, smoke, flame, red UNVERIFIED ribbon."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 205, 225))
    for cx, cy, s in [(x + 30, y + 10, 12), (x + 46, y + 16, 9), (x + 120, y + 8, 14)]:
        d.ellipse([cx, cy, cx + s, cy + s], fill=(110, 110, 118))
    d.polygon([(x + 40, y + 26), (x + 48, y + 10), (x + 56, y + 26)], fill=(230, 110, 20))
    d.polygon([(x + 58, y + 30), (x + 64, y + 18), (x + 70, y + 30)], fill=(240, 160, 40))
    d.rectangle([x + 8, y + h - 34, x + w - 8, y + h - 18], fill=(30, 30, 42))
    d.rectangle([x + w - 44, y + h - 52, x + w - 14, y + h - 34], fill=(60, 60, 78))
    d.rectangle([x + 16, y + h - 46, x + w - 52, y + h - 34], fill=(120, 40, 30))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(24, 68, 118))
    for i in range(5):
        d.arc([x + i * 30 - 6, y + h - 12, x + i * 30 + 18, y + h + 4], 200, 340,
              fill=(255, 255, 255), width=2)
    d.rectangle([x + 8, y + h - 26, x + 92, y + h - 12], fill=RED)
    d.text((x + 50, y + h - 19), "UNVERIFIED", font=font(SANS_B, 9),
           fill=(255, 255, 255), anchor="mm")


def art_rally(d, x, y, w, h):
    """Spain: podium, three flags, crowd of dots."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
    for fx, col in [(x + 26, RED), (x + 66, GOLD), (x + 106, PURPLE)]:
        d.line([fx, y + 8, fx, y + 44], fill=(60, 60, 60), width=2)
        d.polygon([(fx, y + 8), (fx + 26, y + 15), (fx, y + 22)], fill=col)
    d.rectangle([x + w // 2 - 16, y + 44, x + w // 2 + 16, y + h - 26], fill=NAVY)
    d.ellipse([x + w // 2 - 8, y + 30, x + w // 2 + 8, y + 46], fill=(230, 190, 150))
    for i in range(24):
        cx = x + 8 + (i % 12) * 12
        cy = y + h - 20 + (i // 12) * 9
        d.ellipse([cx, cy, cx + 6, cy + 6], fill=(60, 60, 70) if i % 3 else RED)


def art_mine(d, x, y, w, h):
    """Bogor mine: dark tunnel, lamp beam, big 27."""
    d.rectangle([x, y, x + w, y + h], fill=(48, 40, 32))
    d.ellipse([x + 12, y + 4, x + w - 12, y + h - 4], fill=(22, 18, 14))
    for i in range(4):
        d.line([x + 22, y + 16 + i * 12, x + w - 22, y + 16 + i * 12],
               fill=(130, 105, 70), width=2)
    d.polygon([(x + w // 2, y + 12), (x + w // 2 - 18, y + 44), (x + w // 2 + 18, y + 44)],
              fill=(255, 220, 120))
    d.text((x + w // 2, y + h - 22), "27", font=font(SANS_B, 22),
           fill=GOLD, anchor="mm")


def art_sap(d, x, y, w, h):
    """SAP: blue glass tower, red down arrow, AI chip, -10,000 tag."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 244))
    d.rectangle([x + 16, y + 8, x + 66, y + h - 6], fill=(40, 90, 160))
    for wy in range(y + 14, y + h - 12, 10):
        for wx in range(x + 22, x + 60, 10):
            d.rectangle([wx, wy, wx + 6, wy + 5], fill=(180, 210, 240))
    d.rectangle([x + 78, y + 30, x + 128, y + h - 6], fill=(70, 110, 170))
    d.line([x + 96, y + 12, x + 96, y + h - 22], fill=RED, width=4)
    d.polygon([(x + 84, y + h - 30), (x + 108, y + h - 30), (x + 96, y + h - 14)], fill=RED)
    d.rectangle([x + w - 46, y + 8, x + w - 8, y + 32], fill=(30, 30, 42))
    d.text((x + w - 27, y + 20), "AI", font=font(SANS_B, 13), fill=(255, 255, 255), anchor="mm")


def art_boat(d, x, y, w, h):
    """Ulleung: sea, fishing boat, two small flags, '6 RETURNED' tag."""
    d.rectangle([x, y, x + w, y + h], fill=(190, 216, 232))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 68, 118))
    for i in range(4):
        d.arc([x + i * 34 - 4, y + h - 20, x + i * 34 + 20, y + h - 2], 200, 340,
              fill=(255, 255, 255), width=2)
    d.polygon([(x + 22, y + h - 34), (x + w - 22, y + h - 34), (x + w - 34, y + h - 22),
               (x + 34, y + h - 22)], fill=(90, 50, 30))
    d.rectangle([x + 58, y + h - 56, x + 92, y + h - 34], fill=(240, 240, 235))
    d.line([x + 92, y + h - 62, x + 92, y + h - 34], fill=(60, 60, 60), width=2)
    d.polygon([(x + 92, y + h - 62), (x + 116, y + h - 56), (x + 92, y + h - 50)], fill=RED)
    d.polygon([(x + 58, y + h - 62), (x + 82, y + h - 56), (x + 58, y + h - 50)], fill=TEAL)
    d.text((x + 10, y + 8), "6 RETURNED", font=font(SANS_B, 12), fill=NAVY)


def art_footy(d, x, y, w, h):
    """AFLW: green oval, goal posts, rain, scoreboard 44-18."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 130, 70))
    d.ellipse([x + 4, y + 10, x + w - 4, y + h - 10], outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + 10, x + w // 2, y + h - 10], fill=(255, 255, 255), width=2)
    for gx in (x + 18, x + w - 26):
        d.line([gx, y + 12, gx, y + 34], fill=(255, 255, 255), width=3)
    for i in range(10):
        rx = x + 6 + (i * 29) % (w - 12)
        ry = y + 6 + (i * 17) % (h - 12)
        d.line([rx, ry, rx - 3, ry + 8], fill=(180, 210, 240), width=2)
    d.rectangle([x + w // 2 - 34, y + 4, x + w // 2 + 34, y + 24], fill=(255, 255, 255))
    d.text((x + w // 2, y + 14), "44\u201318", font=font(SANS_B, 14), fill=NAVY, anchor="mm")


def art_stadium(d, x, y, w, h):
    """Marseille: stands of dots, flare, '5 IN HOSPITAL' tag."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 80))
    for row in range(4):
        for i in range(11):
            cx = x + 8 + i * 13
            cy = y + 8 + row * 11
            col = (200, 200, 210) if (i + row) % 4 else RED
            d.ellipse([cx, cy, cx + 6, cy + 6], fill=col)
    d.polygon([(x + w // 2 - 6, y + h - 34), (x + w // 2, y + h - 48),
               (x + w // 2 + 6, y + h - 34)], fill=(240, 120, 20))
    d.ellipse([x + w // 2 - 10, y + h - 30, x + w // 2 + 10, y + h - 14], fill=(240, 160, 40))
    d.rectangle([x + 6, y + h - 26, x + 116, y + h - 12], fill=RED)
    d.text((x + 61, y + h - 19), "5 IN HOSPITAL", font=font(SANS_B, 10),
           fill=(255, 255, 255), anchor="mm")


ART = {"sp": art_sp, "parliament": art_parliament, "ecb": art_ecb,
       "drone": art_drone, "market": art_market, "tokyo": art_tokyo,
       "tanker": art_tanker, "rally": art_rally, "mine": art_mine,
       "sap": art_sap, "boat": art_boat, "footy": art_footy,
       "stadium": art_stadium}


def draw_scene(d, kind, x, y, w, h):
    """Draw a scene on a fixed 240x100 canvas, then scale it into the box."""
    scene = Image.new("RGB", (240, 100), PAPER)
    sd = ImageDraw.Draw(scene)
    ART[kind](sd, 0, 0, 240, 100)
    scene = scene.resize((w, h), Image.LANCZOS)
    d._image.paste(scene, (x, y))


# ---------------- schematic world map ----------------
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-78, 73), (-58, 60), (-52, 47),
     (-68, 42), (-78, 32), (-90, 30), (-97, 25), (-106, 22), (-116, 31), (-126, 42),
     (-132, 56), (-152, 60)],
    [(-82, 10), (-62, 9), (-50, 0), (-40, -8), (-35, -18), (-44, -28), (-58, -38),
     (-68, -50), (-74, -34), (-80, -14)],
    [(-10, 36), (-4, 43), (0, 49), (4, 57), (10, 59), (20, 64), (30, 70), (42, 68),
     (32, 60), (22, 55), (16, 46), (10, 40), (0, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (36, 28), (42, 15),
     (50, 10), (46, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25),
     (10, -15), (5, 5), (-5, 5)],
    [(40, 68), (60, 70), (80, 73), (100, 75), (120, 72), (140, 72), (160, 65),
     (170, 60), (160, 50), (140, 40), (130, 35), (120, 25), (110, 10), (100, 8),
     (90, 15), (80, 8), (70, 20), (60, 25), (50, 28), (40, 35)],
    [(113, -22), (125, -15), (135, -12), (145, -15), (150, -25), (155, -35),
     (145, -40), (135, -35), (125, -32)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 242), outline=(150, 160, 175))

    def px(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (75 - lat) / 135.0 * h)

    for cont in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in cont],
                  fill=(188, 198, 182), outline=(140, 150, 140))
    for num, (lon, lat) in sorted(PINS.items()):
        cx, cy = px(lon, lat)
        dx, dy = PIN_JITTER.get(num, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([cx, cy, cx + dx, cy + dy], fill=RED, width=1)
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
            cx, cy = cx + dx, cy + dy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((cx, cy), str(num), font=font(SANS_B, 9), fill=(255, 255, 255), anchor="mm")


# ---------------- layout ----------------
REGION_SHORT = {"EUROPE": "EU", "MID EAST": "ME", "E ASIA": "EA", "N AMERICA": "NA",
                "GLOBAL": "GL", "AFRICA": "AF", "S ASIA": "SA", "OCEANIA": "OC",
                "SE ASIA": "SEA", "LAT AM": "LA"}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=RED)
    d.rectangle([0, H - 8, W, H], fill=NAVY)

    # Top bar: paper name left, counts right
    d.text((24, 12), "THE WORLD IN ONE DAY", font=font(SERIF_B, 21), fill=INK)
    d.text((W - 24, 14), "40 STORIES  \u00b7  10 REGIONS  \u00b7  13 FIELDS",
           font=font(SANS_B, 13), fill=GREY, anchor="ra")

    # Masthead + one-line summary of the three leads
    d.text((W // 2, 36), "Friday 27 November 2026", font=font(SERIF_B, 52),
           fill=INK, anchor="mt")
    d.text((W // 2, 94),
           "Wall St caps its best week since April 2025  \u00b7  EU names De Cos to lead the ECB  \u00b7  NZ coalition falls one seat short",
           font=font(SERIF, 16), fill=DARKRED, anchor="mt")

    # Region chips
    d.text((24, 118), "REGIONS", font=font(SANS_B, 11), fill=GREY)
    cx = 96
    for label, col in CHIPS:
        fnt = font(SANS_B, 10)
        tw = d.textlength(label, font=fnt)
        d.rectangle([cx, 114, cx + tw + 12, 132], fill=col)
        d.text((cx + 6, 123), label, font=fnt, fill=(255, 255, 255), anchor="lm")
        cx += tw + 18

    # UTC timeline strip (6 verified times)
    d.rectangle([24, 140, W - 24, 162], fill=NAVY)
    slot = (W - 48) / 6
    for i, (when, what) in enumerate(TIMELINE[:6]):
        sx = 24 + i * slot
        d.text((sx + 6, 151), when, font=font(SANS_B, 11), fill=GOLD, anchor="lm")
        d.text((sx + 52, 151), truncate(d, what, font(SANS, 10), slot - 58),
               font=font(SANS, 10), fill=(255, 255, 255), anchor="lm")

    # ---- leads (3 cards across the left zone) ----
    lead_w, lead_h, lead_gap = 242, 242, 11
    lead_y = 168
    for i, s in enumerate(LEADS):
        x0 = 24 + i * (lead_w + lead_gap)
        d.rectangle([x0, lead_y, x0 + lead_w, lead_y + lead_h],
                    outline=(160, 150, 130), width=2, fill=(255, 255, 255))
        d.rectangle([x0, lead_y, x0 + lead_w, lead_y + 24], fill=s["colour"])
        d.text((x0 + 8, lead_y + 12),
               truncate(d, f"{s['n']} \u00b7 {s['city']} \u00b7 {s['field']}",
                        font(SANS_B, 10), lead_w - 68),
               font=font(SANS_B, 10), fill=(255, 255, 255), anchor="lm")
        d.text((x0 + lead_w - 8, lead_y + 12), s["tag"], font=font(SANS_B, 10),
               fill=(255, 220, 120), anchor="rm")
        draw_scene(d, s["art"], x0 + 2, lead_y + 26, lead_w - 4, 104)
        y, nlines = draw_wrapped(d, (x0 + 10, lead_y + 136), s["headline"],
                                 font(SANS_B, 20), INK, lead_w - 20,
                                 leading=22, max_lines=3)
        avail_deck = max(1, (lead_y + lead_h - 20 - (y + 2)) // 15)
        draw_wrapped(d, (x0 + 10, y + 2), s["deck"], font(SANS, 12),
                     (60, 60, 60), lead_w - 20, leading=15, max_lines=avail_deck)
        d.text((x0 + 10, lead_y + lead_h - 16),
               truncate(d, s["stat"], font(SANS_B, 10), lead_w - 20),
               font=font(SANS_B, 10), fill=TAG_COLOUR[s["tag"]])

    # ---- medium panels (5 cols x 2 rows) ----
    med_w, med_h, med_gap = 144, 168, 7
    med_y0 = 416
    for i, s in enumerate(MEDIUM):
        col, row = i % 5, i // 5
        x0 = 24 + col * (med_w + med_gap)
        y0 = med_y0 + row * (med_h + 6)
        d.rectangle([x0, y0, x0 + med_w, y0 + med_h],
                    outline=(160, 150, 130), width=1, fill=(255, 255, 255))
        d.text((x0 + 6, y0 + 10), f"{s['n']} {s['city']}",
               font=font(SANS_B, 9), fill=NAVY, anchor="lm")
        d.text((x0 + med_w - 6, y0 + 10), s["tag"], font=font(SANS_B, 8),
               fill=TAG_COLOUR[s["tag"]], anchor="rm")
        draw_scene(d, s["art"], x0 + 2, y0 + 18, med_w - 4, 54)
        y, nlines = draw_wrapped(d, (x0 + 6, y0 + 76), s["headline"],
                                 font(SANS_B, 13), INK, med_w - 12,
                                 leading=15, max_lines=3)
        draw_wrapped(d, (x0 + 6, y + 1), s["deck"], font(SANS, 10),
                     (70, 70, 70), med_w - 12, leading=12, max_lines=2)
        d.text((x0 + 6, y0 + med_h - 12),
               truncate(d, s["source"], font(SANS_B, 9), med_w - 12),
               font=font(SANS_B, 9), fill=GREY)

    # ---- numbers sidebar ----
    sb_x, sb_y, sb_w, sb_h = 784, 168, 216, 590
    d.rectangle([sb_x, sb_y, sb_x + sb_w, sb_y + sb_h], fill=NAVY)
    d.text((sb_x + sb_w // 2, sb_y + 16), "THE DAY IN NUMBERS",
           font=font(SANS_B, 13), fill=GOLD, anchor="mm")
    d.line([sb_x + 12, sb_y + 30, sb_x + sb_w - 12, sb_y + 30], fill=GOLD, width=1)
    ny = sb_y + 36
    for big, label in NUMBERS:
        d.text((sb_x + 12, ny), big, font=font(SERIF_B, 30), fill=(255, 255, 255))
        draw_wrapped(d, (sb_x + 12, ny + 38), label, font(SANS, 11),
                     (210, 220, 235), sb_w - 24, leading=13, max_lines=3)
        ny += 86
    d.line([sb_x + 12, ny + 2, sb_x + sb_w - 12, ny + 2], fill=GOLD, width=1)
    d.text((sb_x + 12, ny + 10), "Every figure is from\nFriday 27 November 2026.",
           font=font(SANS, 10), fill=(210, 220, 235))

    # ---- bottom: map + list ----
    d.text((24, 770), "WHERE IT HAPPENED \u2014 PINS 1\u201313",
           font=font(SANS_B, 12), fill=NAVY)
    draw_map(d, 24, 786, 306, 162)
    d.text((342, 770), "ALSO ON FRIDAY 27 NOVEMBER \u2014 27 MORE STORIES",
           font=font(SANS_B, 12), fill=NAVY)
    col_w = 219
    for i, (num, region, head, src, tag) in enumerate(MORE):
        col, row = i % 3, i // 3
        x0 = 342 + col * col_w
        y0 = 790 + row * 18
        d.text((x0, y0), f"{num}.", font=font(SANS_B, 12), fill=RED)
        tx = x0 + 26
        code = REGION_SHORT[region]
        d.text((tx, y0 + 1), f"[{code}]", font=font(SANS_B, 10), fill=NAVY)
        tx += d.textlength(f"[{code}]", font=font(SANS_B, 10)) + 5
        suffix = ""
        rw = 0
        if tag != "REPORTED":
            rf = font(SANS_B, 8)
            suffix = tag
            rw = d.textlength(suffix, font=rf) + 4
        avail = x0 + col_w - 6 - rw - tx
        d.text((tx, y0), truncate(d, head, font(SANS, 11), avail),
               font=font(SANS, 11), fill=INK)
        if suffix:
            d.text((x0 + col_w - 6, y0 + 1), suffix, font=rf,
                   fill=TAG_COLOUR[tag], anchor="ra")

    # ---- date-check strip ----
    d.rectangle([24, 962, W - 24, 992], fill=(255, 240, 240), outline=RED, width=1)
    d.text((36, 966),
           "DATE CHECK \u2014 Every story on this page happened or was first reported on Friday 27 November 2026 (any time zone).",
           font=font(SANS_B, 11), fill=RED)
    d.text((36, 980),
           "Left out because they happened on an earlier day: Kuwait strike \u00b7 UK migration 77,000 \u00b7 Chess Game 3 \u00b7 Bangkok blast \u00b7 Ebola 12,021 \u00b7 Cairo fire (25 Nov)",
           font=font(SANS, 10), fill=DARKRED)

    # ---- footer ----
    d.text((24, 996),
           "SOURCES: AP \u00b7 Reuters \u00b7 Consilium \u00b7 Electoral Commission NZ \u00b7 AFL \u00b7 F1 \u00b7 FIA F2 \u00b7 Bloomberg \u00b7 Adobe \u00b7 Basarnas \u00b7 ERR \u00b7 AFP \u00b7 UNCTAD \u00b7 UNI Global \u00b7 Fars/Anadolu",
           font=font(SANS, 9), fill=GREY)
    d.text((24, 1007),
           "OFFICIAL = confirmed by an authority  \u00b7  REPORTED = reported by a named source  \u00b7  CLAIM = one party's claim, not confirmed  \u00b7  Scenes are drawn illustrations, not photographs.",
           font=font(SANS, 9), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
