#!/usr/bin/env python3
"""Render "The World in One Page" - Friday 27 November 2026.

Fresh renderer for the news-image-20261127 v3 rebuild. Draws a single
1024x1024 news summary with PIL: 3 lead stories with drawn scenes, 12
illustrated medium panels, a 27-item numbered list, a world map with 15
pins, a UTC timeline, a numbers sidebar and a fields block.

Every story is dated Friday 27 November 2026 (or labelled CARRY-OVER
with its original date). Labels: OFFICIAL = authority-confirmed,
REPORTED = named outlet, CLAIM = one party's claim, unverified.

Run:  python3 render.py            -> writes entry.png beside this file
       python3 main.py             -> same, via the entrypoint (honours
                                      MAKEFUN_OUTPUT_DIR when set)
The image is deterministic: same input always yields byte-identical PNG.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = _font("DejaVuSans-Bold.ttf", 30)
F_SUB = _font("DejaVuSans-Bold.ttf", 13)
F_SEC = _font("DejaVuSans-Bold.ttf", 12)
F_LEAD_H = _font("DejaVuSans-Bold.ttf", 16)
F_LEAD_B = _font("DejaVuSans.ttf", 11)
F_LEAD_W = _font("DejaVuSans.ttf", 10)
F_LEAD_WB = _font("DejaVuSans-Bold.ttf", 10)
F_MED_H = _font("DejaVuSans-Bold.ttf", 11)
F_MED_B = _font("DejaVuSans.ttf", 10)
F_LIST = _font("DejaVuSans.ttf", 10)
F_LIST_N = _font("DejaVuSans-Bold.ttf", 10)
F_NUM_B = _font("DejaVuSans-Bold.ttf", 21)
F_NUM_L = _font("DejaVuSans.ttf", 10)
F_TL_T = _font("DejaVuSans-Bold.ttf", 10)
F_TL_B = _font("DejaVuSans.ttf", 10)
F_SRC = _font("DejaVuSans.ttf", 9)
F_FOOT = _font("DejaVuSans.ttf", 9)
F_CHIP = _font("DejaVuSans-Bold.ttf", 9)
F_PIN = _font("DejaVuSans-Bold.ttf", 8)
F_TAG = _font("DejaVuSans-Bold.ttf", 11)

PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
NAVY = (27, 58, 92)
NAVY_LT = (38, 78, 120)
RED = (178, 38, 30)
RED_BG = (246, 224, 220)
GREEN = (28, 110, 60)
GREEN_BG = (222, 240, 228)
GOLD = (176, 124, 20)
GOLD_BG = (248, 236, 205)
SEA = (168, 205, 225)
SEA_DK = (90, 140, 175)
LAND = (226, 214, 178)
LAND_EDGE = (170, 155, 120)
LINE = (200, 192, 175)

LABEL_FILL = {"OFFICIAL": NAVY, "REPORTED": GREEN, "CLAIM": GOLD}

# ---------------------------------------------------------------- data
LEADS = [
    {
        "n": 1, "kind": "ship", "tag": "6TH SHIP DISABLED",
        "label": "OFFICIAL", "region": "MIDDLE EAST", "field": "CONFLICT",
        "headline": "US disables Iran blockade runner in Gulf of Oman",
        "deck": "CENTCOM: a US aircraft hit the M/V Pacific Archer; "
                "propulsion disabled, crew unharmed.",
        "why": "Sixth ship disabled under the US blockade of Iranian "
               "ports; 158 vessels have been redirected.",
        "date_note": "Announced Fri 27 Nov; the strike was Thu 26 Nov.",
    },
    {
        "n": 2, "kind": "wallst", "tag": "S&P +1.60%",
        "label": "REPORTED", "region": "N AMERICA", "field": "MARKETS",
        "headline": "Wall St caps best week since April 2025",
        "deck": "S&P +1.60% to 7,297.49; Nasdaq +2.31%, Dow +1.18%. "
                "Week: S&P +5.6%, best since April 2025.",
        "why": "A strong close to a holiday-shortened week as investors "
               "bet on a year-end rally.",
        "date_note": "Early close 13:00 ET, Fri 27 Nov.",
    },
    {
        "n": 3, "kind": "parliament", "tag": "65 / 130 SEATS",
        "label": "REPORTED", "region": "OCEANIA", "field": "POLITICS",
        "headline": "NZ coalition falls one seat short in final count",
        "deck": "National 40, ACT 13, NZ First 12 = 65 of 130, one short "
                "of 66. Labour 36, Greens 17, Te Pati Maori 5.",
        "why": "Newcomer Opportunity, led by Qiulae Wong, 38, now holds "
               "the balance of power.",
        "date_note": "Final count released 14:00 NZDT, Fri 27 Nov.",
    },
]

MEDIUMS = [
    {"n": 4, "kind": "ecb", "label": "OFFICIAL", "region": "EUROPE",
     "field": "CENTRAL BANKING",
     "headline": "EU names De Cos next ECB president",
     "deck": "Ex-Bank of Spain chief succeeds Lagarde on 7 Feb 2027."},
    {"n": 5, "kind": "bars", "label": "REPORTED", "region": "EAST ASIA",
     "field": "MARKETS",
     "headline": "Chinese shares soar on Beijing support signal",
     "deck": "Shanghai +3.7%, CSI 300 +4.2%, STAR 50 +15%; chips +19%."},
    {"n": 6, "kind": "drone", "label": "REPORTED", "region": "EUROPE",
     "field": "CONFLICT",
     "headline": "Drones breach Latvia; NATO jets scrambled",
     "deck": "Drone violates Latvian airspace; Estonia sounds alert."},
    {"n": 7, "kind": "shop", "label": "REPORTED", "region": "N AMERICA",
     "field": "RETAIL",
     "headline": "Black Friday opens: $12.9bn day ahead",
     "deck": "Adobe forecasts $12.9bn US online sales, up 9.2%."},
    {"n": 8, "kind": "tokyo", "label": "REPORTED", "region": "EAST ASIA",
     "field": "ECONOMY",
     "headline": "Tokyo inflation 2.9%; Nikkei jumps 2.11%",
     "deck": "Core CPI at 16-month high keeps a BOJ hike in play."},
    {"n": 9, "kind": "tanker", "label": "CLAIM", "region": "MIDDLE EAST",
     "field": "CONFLICT",
     "headline": "Iran says tanker hit its mines in Hormuz",
     "deck": "IRGC Navy says a tanker exploded; not verified."},
    {"n": 10, "kind": "rally", "label": "REPORTED", "region": "EUROPE",
     "field": "POLITICS",
     "headline": "Spain's campaign ends; Sanchez vows to defy polls",
     "deck": "Final day before Sunday's snap election; PP ~31%."},
    {"n": 11, "kind": "mine", "label": "OFFICIAL", "region": "SE ASIA",
     "field": "DISASTER",
     "headline": "Indonesia mine: toll rises to 27, all 13 dead identified",
     "deck": "One more victim counted after the Bogor flood."},
    {"n": 12, "kind": "sap", "label": "REPORTED", "region": "EUROPE",
     "field": "TECHNOLOGY",
     "headline": "SAP weighs 10,000+ job cuts in AI push",
     "deck": "Plan would cut ~9% of staff as it rebuilds on AI."},
    {"n": 13, "kind": "boat", "label": "REPORTED", "region": "EAST ASIA",
     "field": "DIPLOMACY",
     "headline": "Seoul sends six North Koreans home; one stays",
     "deck": "Six fishermen repatriated; the seventh stays South."},
    {"n": 14, "kind": "oval", "label": "REPORTED", "region": "OCEANIA",
     "field": "SPORT",
     "headline": "North Melbourne seal AFLW three-peat, 44-18",
     "deck": "Kangaroos beat Melbourne in the rain at Ikon Park."},
    {"n": 15, "kind": "stadium", "label": "REPORTED", "region": "EUROPE",
     "field": "SPORT",
     "headline": "Macron condemns Marseille fan violence",
     "deck": "Five Levski fans in hospital; UEFA opens probe."},
]

LIST_ITEMS = [
    (16, "OFFICIAL", "EUROPE", "EU budget summit ends without deal; 24 back \u20ac45bn Ukraine loan"),
    (17, "CLAIM", "MIDDLE EAST", "Iran denies Kuwait strike, cries \u2018false flag\u2019"),
    (18, "REPORTED", "EAST ASIA", "Taiwan: final day of campaigning; 26 Chinese jets tracked"),
    (19, "REPORTED", "EAST ASIA", "Kim vows a bigger nuclear arsenal"),
    (20, "REPORTED", "GLOBAL", "Gold rebounds off 15-month low; silver +6%; 10-year 4.92%"),
    (21, "REPORTED", "GLOBAL", "Amazon workers strike in 20+ countries on Black Friday"),
    (22, "REPORTED", "EUROPE", "Serbia students pick chemist Saicic for president"),
    (23, "REPORTED", "MIDDLE EAST", "Antonelli fastest in Qatar GP practice, 1:23.217"),
    (24, "REPORTED", "N AMERICA", "Thanksgiving storm: 500,000+ still out; Macy\u2019s parade off"),
    (25, "REPORTED", "GLOBAL", "UNCTAD: global seaborne trade to flatline in 2026"),
    (26, "OFFICIAL", "AFRICA", "Egypt detains driver after tanker crash"),
    (27, "REPORTED", "EUROPE", "France cyber chief warns of \u2018unprecedented\u2019 threat"),
    (28, "REPORTED", "EUROPE", "Meloni: EU \u2018far\u2019 from budget deal"),
    (29, "REPORTED", "EUROPE", "Zelensky rebukes \u2018my friend\u2019 jibe"),
    (30, "REPORTED", "EUROPE", "Turkey summons Georgia\u2019s envoy"),
    (31, "REPORTED", "MIDDLE EAST", "Eisenkot aims for cabinet in 8 days"),
    (32, "REPORTED", "S ASIA", "Islamabad hosts defence-pact talks"),
    (33, "REPORTED", "S ASIA", "Pakistan checks Libya boat reports"),
    (34, "REPORTED", "OCEANIA", "ACCC warns on AI-made sale deals"),
    (35, "REPORTED", "OCEANIA", "Hunter rail strike called off"),
    (36, "REPORTED", "MIDDLE EAST", "F2 pole for debutant Ugochukwu, 1:35.818"),
    (37, "REPORTED", "AFRICA", "RSF raids kill 14 in East Darfur and Kordofan"),
    (38, "REPORTED", "EAST ASIA", "Hong Kong marks tower-fire anniversary"),
    (39, "REPORTED", "EUROPE", "FTSE 100 closes up 0.8% at 10,698.81"),
    (40, "REPORTED", "LATIN AMERICA", "Brazil keeps ex-BRB chief jailed"),
    (41, "REPORTED", "N AMERICA", "SpaceX shares for every US child with a Trump Account"),
    (42, "REPORTED", "UK", "Forest beat Chelsea 3-2 in Friday-night opener"),
]

NUMBERS = [
    ("65/130", "NZ coalition seats; 66 needed for a majority"),
    ("+5.6%", "S&P 500\u2019s best week since April 2025 (+1.60% Fri)"),
    ("+3.7%", "Shanghai Composite jump; STAR 50 +15%, semis +19%"),
    ("44\u201318", "North Melbourne\u2019s AFLW three-peat"),
    ("10,000+", "SAP jobs at risk in its AI revamp"),
]

FIELDS = ["Politics", "Markets", "Economy", "Retail", "Central banking",
          "Conflict", "Defence", "Diplomacy", "Disaster", "Technology",
          "Cybersecurity", "Space", "Sport", "Motorsport", "Labour",
          "Trade", "Crime", "Migration", "Consumer"]

TIMELINE = [
    ("00:30", "EU names De Cos next ECB chief"),
    ("01:00", "NZ final count: coalition 65 of 130"),
    ("07:00", "Shanghai closes +3.7%; STAR 50 +15%"),
    ("18:00", "Wall St closes: S&P +1.60% to 7,297.49"),
    ("20:00", "Forest beat Chelsea 3-2"),
    ("23:00", "Spain\u2019s campaign closes with final rallies"),
]

# (number, longitude, latitude) for the 15 illustrated stories
PINS = [(1, 57.0, 25.0), (2, -74.0, 40.7), (3, 174.8, -41.3),
        (4, 4.35, 50.85), (5, 121.5, 31.2), (6, 27.8, 57.5),
        (7, -74.0, 40.7), (8, 139.7, 35.7), (9, 56.5, 26.5),
        (10, -3.7, 40.4), (11, 106.8, -6.6), (12, 8.6, 49.3),
        (13, 130.9, 37.5), (14, 145.0, -37.8), (15, 5.4, 43.3)]

SOURCES = ("AP \u00b7 Reuters \u00b7 Consilium \u00b7 CENTCOM \u00b7 Electoral "
           "Commission NZ \u00b7 AFL \u00b7 F1 \u00b7 FIA F2 \u00b7 Bloomberg "
           "\u00b7 Adobe \u00b7 Basarnas \u00b7 ERR \u00b7 AFP \u00b7 UNCTAD "
           "\u00b7 UNI Global \u00b7 Fars/Anadolu \u00b7 Premier League")

# ------------------------------------------------------- text helpers

def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines, each <= width pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def chip(d, x, y, label):
    """Small coloured label chip; returns width used."""
    fill = LABEL_FILL[label]
    w = int(d.textlength(label, font=F_CHIP)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=F_CHIP, fill=(255, 255, 255))
    return w


# --------------------------------------------------------- fit check

def check_fit():
    """Measure every text element against its box. Returns problems."""
    problems = []

    def need(name, text, fnt, width, max_lines):
        lines = wrap(text, fnt, width)
        if len(lines) > max_lines:
            problems.append(
                "%s: %d lines (max %d): %r" % (name, len(lines), max_lines,
                                               text[:60]))
        for ln in lines:
            if fnt.getlength(ln) > width + 0.5:
                problems.append("%s: line too wide: %r" % (name, ln[:60]))

    lead_w = (W - 2 * 8 - 2 * 8) // 3  # 330
    text_w = lead_w - 16
    for lead in LEADS:
        need("lead%d headline" % lead["n"], lead["headline"], F_LEAD_H,
             text_w, 2)
        need("lead%d deck" % lead["n"], lead["deck"], F_LEAD_B, text_w, 2)
        need("lead%d why" % lead["n"], lead["why"], F_LEAD_W, text_w, 2)
        need("lead%d date" % lead["n"], lead["date_note"], F_LEAD_W,
             text_w, 1)
        # chips: label chip + "REGION · FIELD" must fit one row
        rest = "%s \u00b7 %s" % (lead["region"], lead["field"])
        if F_CHIP.getlength(rest) > text_w - 70:
            problems.append("lead%d chips too wide: %r"
                            % (lead["n"], rest))

    med_text_w = 246 - 66 - 8  # cell 246, scene 60 + gap 6, padding 8
    for med in MEDIUMS:
        need("med%d headline" % med["n"], med["headline"], F_MED_H,
             med_text_w, 2)
        need("med%d deck" % med["n"], med["deck"], F_MED_B, med_text_w, 2)

    list_w = 416 - 26 - 6  # column 416, number gutter 26, padding 6
    for n, label, region, head in LIST_ITEMS:
        full = head + " \u00b7 " + region
        if F_LIST.getlength(full) > list_w:
            problems.append("list%d too wide (%d > %d): %r"
                            % (n, F_LIST.getlength(full), list_w, full[:60]))

    for big, label in NUMBERS:
        need("number %s" % big, label, F_NUM_L, 308 - 16, 2)

    fields_text = " \u00b7 ".join(FIELDS)
    need("fields block", fields_text, F_NUM_L, 308 - 16, 4)

    for t, text in TIMELINE:
        need("timeline %s" % t, text, F_TL_B, 268 - 52, 2)

    need("sources", SOURCES, F_SRC, 268 - 8, 5)
    need("footer", "Drawn from AP, Reuters and 14 other outlets \u00b7 "
                   "All times UTC unless noted \u00b7 Labels: OFFICIAL = "
                   "authority-confirmed \u00b7 REPORTED = named outlet "
                   "\u00b7 CLAIM = one party\u2019s claim, unverified",
         F_FOOT, W - 16, 2)
    return problems

# ------------------------------------------------------------- scenes
# Each scene draws into box (x0, y0, x1, y1) with simple flat shapes.
# All coordinates are relative to the box so the same scene works at
# lead size and at medium-cell size.

def _box(box):
    x0, y0, x1, y1 = box
    return x0, y0, x1, y1, x1 - x0, y1 - y0


def scene_ship(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(30, 60, 95))
    d.rectangle([x0, y0 + int(h * 0.62), x1, y1], fill=(16, 42, 68))
    for i in range(5):  # waves
        d.arc([x0 + i * w // 5 - 6, y0 + int(h * 0.66), x0 + (i + 1) * w // 5 + 6,
               y0 + int(h * 0.86)], 200, 340, fill=(120, 180, 210), width=2)
    hx, hy = x0 + int(w * 0.14), y0 + int(h * 0.48)
    d.polygon([(hx, hy), (hx + int(w * 0.62), hy), (hx + int(w * 0.56), hy + int(h * 0.20)),
               (hx + int(w * 0.06), hy + int(h * 0.20))], fill=(40, 40, 44))
    for i in range(3):  # containers
        cx = hx + int(w * (0.10 + i * 0.16))
        d.rectangle([cx, hy - int(h * 0.16), cx + int(w * 0.13), hy],
                    fill=[(200, 60, 40), (230, 170, 40), (60, 130, 90)][i])
    d.rectangle([hx + int(w * 0.52), hy - int(h * 0.30), hx + int(w * 0.60),
                 hy], fill=(220, 220, 220))
    sx, sy = x0 + int(w * 0.82), y0 + int(h * 0.30)  # strike flash
    for ang in range(0, 360, 45):
        import math
        r1, r2 = int(h * 0.10), int(h * 0.26)
        a = math.radians(ang)
        d.line([sx, sy, sx + int(r2 * math.cos(a)), sy + int(r2 * math.sin(a))],
               fill=(255, 200, 60), width=3)
    d.ellipse([sx - int(h * 0.11), sy - int(h * 0.11), sx + int(h * 0.11),
               sy + int(h * 0.11)], fill=(255, 230, 120))


def scene_wallst(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(24, 48, 80))
    base = y0 + int(h * 0.78)
    for i, bh in enumerate([0.30, 0.55, 0.42, 0.70, 0.58, 0.80, 0.48]):
        bx = x0 + int(w * (0.04 + i * 0.135))
        bw = int(w * 0.10)
        d.rectangle([bx, base - int(h * bh), bx + bw, base], fill=(52, 88, 130))
        for wy in range(3):
            d.rectangle([bx + 2, base - int(h * bh) + 4 + wy * 9, bx + bw - 2,
                         base - int(h * bh) + 8 + wy * 9], fill=(255, 210, 90))
    pts = [(x0 + int(w * 0.05), y0 + int(h * 0.55)),
           (x0 + int(w * 0.25), y0 + int(h * 0.48)),
           (x0 + int(w * 0.45), y0 + int(h * 0.52)),
           (x0 + int(w * 0.62), y0 + int(h * 0.34)),
           (x0 + int(w * 0.80), y0 + int(h * 0.30)),
           (x0 + int(w * 0.96), y0 + int(h * 0.12))]
    d.line(pts, fill=(90, 220, 130), width=3)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=(90, 220, 130))


def scene_parliament(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(38, 68, 110))
    cx, cy = x0 + w // 2, y0 + int(h * 0.92)
    import math
    for ring, r in enumerate([int(h * 0.62), int(h * 0.44), int(h * 0.26)]):
        n = 16 - ring * 4
        for i in range(n):
            a = math.pi * (1 - (i + 0.5) / n)
            px, py = cx + int(r * 1.25 * math.cos(a)), cy - int(r * math.sin(a))
            col = (235, 200, 60) if (ring * n + i) % 2 == 0 else (210, 210, 215)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
    d.rectangle([x0, cy - 2, x1, cy + 2], fill=(220, 220, 220))


def scene_ecb(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(70, 60, 110))
    bx, by = x0 + int(w * 0.30), y0 + int(h * 0.30)
    bw, bh = int(w * 0.40), int(h * 0.52)
    d.rectangle([bx, by, bx + bw, by + bh], fill=(215, 205, 180))
    d.polygon([(bx - 6, by), (bx + bw // 2, by - int(h * 0.16)), (bx + bw + 6, by)],
              fill=(180, 40, 40))
    for i in range(4):
        cx = bx + int(bw * (0.12 + i * 0.24))
        d.rectangle([cx, by + 6, cx + int(bw * 0.10), by + bh], fill=(150, 140, 115))
    import math
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = x0 + int(w * 0.88) + int(w * 0.07 * math.cos(a)), y0 + int(h * 0.24) + int(h * 0.16 * math.sin(a))
        d.polygon([(sx, sy - 4), (sx + 1, sy - 1), (sx + 4, sy), (sx + 1, sy + 1),
                   (sx, sy + 4), (sx - 1, sy + 1), (sx - 4, sy), (sx - 1, sy - 1)],
                  fill=(255, 215, 80))


def scene_bars(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(150, 30, 30))
    base = y0 + int(h * 0.85)
    for i, bh in enumerate([0.18, 0.30, 0.26, 0.44, 0.52, 0.72]):
        bx = x0 + int(w * (0.06 + i * 0.155))
        bw = int(w * 0.11)
        d.rectangle([bx, base - int(h * bh), bx + bw, base], fill=(255, 235, 230))
    d.line([(x0 + int(w * 0.06), y0 + int(h * 0.62)), (x1 - int(w * 0.04), y0 + int(h * 0.10))],
           fill=(255, 215, 80), width=3)


def scene_drone(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(18, 28, 46))
    cx, cy = x0 + w // 2, y0 + int(h * 0.42)
    for i, (ox, oy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        px, py = cx + ox * int(w * 0.20), cy + oy * int(h * 0.20)
        d.ellipse([px - 7, py - 3, px + 7, py + 3], fill=(180, 190, 200))
        d.line([cx, cy, px, py], fill=(140, 150, 160), width=2)
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(220, 225, 230))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 80, 60))
    for r in (14, 26, 38):
        d.arc([x0 + w - r - 8, y1 - r - 8, x0 + w + r - 8, y1 + r - 8],
              200, 330, fill=(90, 220, 130), width=2)


def scene_shop(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(240, 230, 210))
    for i in range(6):
        col = RED if i % 2 == 0 else (255, 255, 255)
        d.polygon([(x0 + i * w // 6, y0), (x0 + (i + 1) * w // 6, y0),
                   (x0 + (i + 1) * w // 6, y0 + int(h * 0.30)),
                   (x0 + i * w // 6, y0 + int(h * 0.30))], fill=col)
    d.rectangle([x0, y0 + int(h * 0.28), x1, y0 + int(h * 0.34)], fill=(60, 40, 30))
    d.rectangle([x0 + int(w * 0.16), y0 + int(h * 0.55), x0 + int(w * 0.40),
                 y0 + int(h * 0.88)], fill=(40, 90, 160))
    d.rectangle([x0 + int(w * 0.58), y0 + int(h * 0.62), x0 + int(w * 0.78),
                 y0 + int(h * 0.88)], fill=(200, 60, 40))
    d.arc([x0 + int(w * 0.22), y0 + int(h * 0.40), x0 + int(w * 0.34),
           y0 + int(h * 0.62)], 180, 360, fill=(40, 90, 160), width=3)


def scene_tokyo(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(40, 60, 110))
    base = y0 + int(h * 0.82)
    for i, bh in enumerate([0.35, 0.55, 0.45, 0.68, 0.50]):
        bx = x0 + int(w * (0.05 + i * 0.18))
        bw = int(w * 0.13)
        d.rectangle([bx, base - int(h * bh), bx + bw, base], fill=(25, 40, 75))
        for wy in range(2):
            d.rectangle([bx + 2, base - int(h * bh) + 4 + wy * 10, bx + bw - 2,
                         base - int(h * bh) + 7 + wy * 10], fill=(255, 215, 90))
    tx = x0 + int(w * 0.80)
    d.polygon([(tx - 6, base), (tx - 3, y0 + int(h * 0.18)), (tx + 3, y0 + int(h * 0.18)),
               (tx + 6, base)], fill=(200, 60, 50))
    d.line([(x0 + int(w * 0.08), y0 + int(h * 0.55)), (x0 + int(w * 0.45), y0 + int(h * 0.50)),
            (x0 + int(w * 0.45), y0 + int(h * 0.38)), (x0 + int(w * 0.90), y0 + int(h * 0.30))],
           fill=(90, 220, 130), width=3)
    d.polygon([(x0 + int(w * 0.90), y0 + int(h * 0.30)), (x0 + int(w * 0.80), y0 + int(h * 0.32)),
               (x0 + int(w * 0.88), y0 + int(h * 0.42))], fill=(90, 220, 130))


def scene_tanker(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(120, 70, 40))
    d.rectangle([x0, y0 + int(h * 0.66), x1, y1], fill=(30, 60, 95))
    hx, hy = x0 + int(w * 0.12), y0 + int(h * 0.50)
    d.polygon([(hx, hy), (hx + int(w * 0.66), hy), (hx + int(w * 0.60), hy + int(h * 0.18)),
               (hx + int(w * 0.06), hy + int(h * 0.18))], fill=(30, 30, 34))
    d.rectangle([hx + int(w * 0.56), hy - int(h * 0.22), hx + int(w * 0.64), hy],
                fill=(200, 200, 200))
    for i, (ox, oy, r) in enumerate([(0.30, 0.30, 10), (0.38, 0.22, 13), (0.48, 0.16, 16)]):
        d.ellipse([x0 + int(w * ox) - r, y0 + int(h * oy) - r,
                   x0 + int(w * ox) + r, y0 + int(h * oy) + r], fill=(90, 90, 95))
    d.polygon([(x0 + int(w * 0.30), y0 + int(h * 0.34)), (x0 + int(w * 0.36), y0 + int(h * 0.20)),
               (x0 + int(w * 0.42), y0 + int(h * 0.34))], fill=(255, 140, 40))


def scene_rally(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(90, 40, 90))
    d.rectangle([x0 + int(w * 0.30), y0 + int(h * 0.55), x0 + int(w * 0.70),
                 y0 + int(h * 0.68)], fill=(120, 90, 60))
    d.rectangle([x0 + int(w * 0.44), y0 + int(h * 0.30), x0 + int(w * 0.56),
                 y0 + int(h * 0.55)], fill=(230, 220, 200))
    d.ellipse([x0 + int(w * 0.46), y0 + int(h * 0.18), x0 + int(w * 0.54),
               y0 + int(h * 0.30)], fill=(240, 200, 160))
    import math
    for i in range(14):
        cx = x0 + int(w * (0.06 + (i % 7) * 0.14))
        cy = y0 + int(h * (0.74 + (i // 7) * 0.12))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(245, 220, 190))
        d.line([cx, cy - 12, cx, cy - 4], fill=(255, 255, 255), width=2)
    for i, col in enumerate([(200, 40, 40), (240, 200, 40), (40, 120, 200)]):
        fx = x0 + int(w * (0.12 + i * 0.30))
        d.line([fx, y0 + int(h * 0.55), fx, y0 + int(h * 0.30)], fill=(255, 255, 255), width=2)
        d.polygon([(fx, y0 + int(h * 0.30)), (fx + 14, y0 + int(h * 0.34)),
                   (fx, y0 + int(h * 0.38))], fill=col)


def scene_mine(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(70, 90, 110))
    d.polygon([(x0, y1), (x0 + int(w * 0.45), y0 + int(h * 0.15)),
               (x1, y1)], fill=(60, 75, 55))
    d.polygon([(x0 + int(w * 0.38), y1), (x0 + int(w * 0.50), y0 + int(h * 0.45)),
               (x0 + int(w * 0.62), y1)], fill=(45, 55, 40))
    d.ellipse([x0 + int(w * 0.44), y0 + int(h * 0.55), x0 + int(w * 0.56),
               y0 + int(h * 0.80)], fill=(20, 20, 20))
    d.ellipse([x0 + int(w * 0.47), y0 + int(h * 0.62), x0 + int(w * 0.53),
               y0 + int(h * 0.72)], fill=(255, 220, 90))


def scene_sap(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(30, 70, 120))
    bx, by = x0 + int(w * 0.18), y0 + int(h * 0.12)
    bw, bh = int(w * 0.34), int(h * 0.76)
    d.rectangle([bx, by, bx + bw, by + bh], fill=(200, 215, 235))
    for r in range(5):
        for c in range(3):
            d.rectangle([bx + 5 + c * 12, by + 6 + r * 13, bx + 12 + c * 12,
                         by + 12 + r * 13], fill=(90, 140, 190))
    cx, cy = x0 + int(w * 0.72), y0 + int(h * 0.55)
    d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(20, 20, 20))
    d.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], fill=(60, 220, 140))
    d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=(20, 20, 20))
    for i in range(3):
        d.line([cx - 16, cy - 16 + i * 16, cx + 16, cy - 16 + i * 16],
               fill=(60, 220, 140), width=1)


def scene_boat(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(140, 190, 220))
    for i in range(3):
        yy = y0 + int(h * (0.62 + i * 0.12))
        d.arc([x0 + 4, yy - 6, x1 - 4, yy + 6], 0, 180, fill=(255, 255, 255), width=2)
    hx, hy = x0 + int(w * 0.20), y0 + int(h * 0.44)
    d.polygon([(hx, hy), (hx + int(w * 0.55), hy), (hx + int(w * 0.48), hy + int(h * 0.14)),
               (hx + int(w * 0.07), hy + int(h * 0.14))], fill=(150, 90, 50))
    d.line([hx + int(w * 0.28), hy, hx + int(w * 0.28), hy - int(h * 0.28)],
           fill=(80, 60, 40), width=2)
    d.polygon([(hx + int(w * 0.28), hy - int(h * 0.28)), (hx + int(w * 0.48), hy - int(h * 0.06)),
               (hx + int(w * 0.28), hy - int(h * 0.06))], fill=(240, 240, 230))


def scene_oval(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(40, 110, 60))
    d.ellipse([x0 + int(w * 0.08), y0 + int(h * 0.14), x1 - int(w * 0.08),
               y1 - int(h * 0.14)], fill=(70, 160, 85))
    d.ellipse([x0 + int(w * 0.08), y0 + int(h * 0.14), x1 - int(w * 0.08),
               y1 - int(h * 0.14)], outline=(255, 255, 255), width=2)
    d.line([x0 + w // 2, y0 + int(h * 0.14), x0 + w // 2, y1 - int(h * 0.14)],
           fill=(255, 255, 255), width=2)
    for gx in (0.16, 0.84):
        px = x0 + int(w * gx)
        for off in (-8, 0, 8):
            d.line([px + off, y0 + int(h * 0.30), px + off, y0 + int(h * 0.62)],
                   fill=(255, 255, 255), width=2)
        d.line([px - 10, y0 + int(h * 0.30), px + 10, y0 + int(h * 0.30)],
               fill=(255, 255, 255), width=2)
    for i in range(12):
        rx = x0 + int(w * (0.08 + (i * 37 % 84) / 100.0))
        ry = y0 + int(h * (0.10 + (i * 53 % 70) / 100.0))
        d.line([rx, ry, rx - 2, ry + 6], fill=(180, 210, 255), width=1)


def scene_stadium(d, box):
    x0, y0, x1, y1, w, h = _box(box)
    d.rectangle(box, fill=(25, 35, 70))
    d.ellipse([x0 + int(w * 0.10), y0 + int(h * 0.30), x1 - int(w * 0.10),
               y1 - int(h * 0.10)], fill=(60, 120, 70))
    d.ellipse([x0 + int(w * 0.10), y0 + int(h * 0.30), x1 - int(w * 0.10),
               y1 - int(h * 0.10)], outline=(200, 200, 200), width=2)
    d.rectangle([x0, y0, x1, y0 + int(h * 0.30)], fill=(35, 50, 95))
    for i in range(8):
        d.rectangle([x0 + int(w * (0.06 + i * 0.115)), y0 + int(h * 0.08),
                     x0 + int(w * (0.06 + i * 0.115)) + 6, y0 + int(h * 0.24)],
                    fill=(255, 220, 120))
    fx, fy = x0 + int(w * 0.78), y0 + int(h * 0.55)
    for r, col in [(16, (255, 120, 40)), (10, (255, 170, 60)), (5, (255, 230, 150))]:
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)


SCENES = {"ship": scene_ship, "wallst": scene_wallst,
          "parliament": scene_parliament, "ecb": scene_ecb,
          "bars": scene_bars, "drone": scene_drone, "shop": scene_shop,
          "tokyo": scene_tokyo, "tanker": scene_tanker,
          "rally": scene_rally, "mine": scene_mine, "sap": scene_sap,
          "boat": scene_boat, "oval": scene_oval, "stadium": scene_stadium}

# ---------------------------------------------------------------- map
# Coarse continent outlines (lon, lat) for a stylised world map.

CONTINENTS = [
    [(-168, 65), (-150, 70), (-130, 71), (-115, 68), (-100, 68), (-90, 68),
     (-82, 66), (-76, 62), (-70, 58), (-65, 60), (-60, 55), (-65, 50),
     (-70, 45), (-75, 40), (-80, 32), (-81, 26), (-84, 30), (-90, 29),
     (-97, 26), (-105, 22), (-110, 24), (-115, 29), (-120, 34), (-125, 40),
     (-124, 48), (-130, 55), (-145, 60), (-160, 58), (-168, 65)],
    [(-80, 10), (-75, 5), (-70, 0), (-75, -5), (-80, -10), (-75, -15),
     (-70, -20), (-65, -25), (-60, -30), (-55, -35), (-60, -38), (-65, -40),
     (-70, -45), (-72, -50), (-70, -54), (-65, -52), (-60, -45), (-50, -35),
     (-40, -25), (-35, -15), (-35, -5), (-45, 0), (-55, 5), (-60, 8),
     (-70, 10), (-80, 10)],
    [(-10, 36), (-5, 40), (-2, 44), (-5, 48), (-2, 50), (0, 52), (5, 54),
     (8, 57), (10, 59), (15, 60), (20, 62), (25, 65), (30, 70), (35, 68),
     (40, 66), (45, 68), (50, 69), (55, 68), (60, 69), (65, 69), (68, 66),
     (60, 60), (55, 55), (50, 50), (45, 48), (40, 46), (35, 44), (30, 42),
     (28, 40), (25, 38), (22, 36), (18, 38), (15, 40), (12, 42), (8, 40),
     (5, 38), (0, 38), (-5, 36), (-10, 36)],
    [(-17, 15), (-15, 20), (-10, 28), (-5, 32), (0, 35), (10, 37), (15, 32),
     (20, 32), (25, 31), (30, 31), (35, 28), (38, 25), (40, 20), (42, 15),
     (45, 11), (48, 10), (50, 5), (48, 0), (42, -5), (40, -10), (38, -15),
     (35, -20), (32, -25), (28, -30), (25, -33), (20, -35), (15, -30),
     (12, -25), (12, -18), (13, -12), (12, -6), (10, 0), (8, 4), (0, 5),
     (-8, 5), (-13, 8), (-17, 12), (-17, 15)],
    [(30, 70), (40, 70), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 76), (110, 76), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 66), (170, 66), (178, 65), (170, 60), (162, 58), (158, 52),
     (150, 55), (142, 50), (140, 45), (135, 42), (130, 38), (127, 35),
     (122, 32), (120, 28), (115, 23), (110, 20), (105, 15), (100, 12),
     (98, 8), (95, 10), (92, 15), (90, 20), (88, 22), (85, 20), (82, 18),
     (80, 15), (77, 10), (75, 8), (72, 12), (70, 18), (68, 22), (66, 25),
     (62, 25), (58, 26), (55, 26), (52, 26), (50, 28), (48, 30), (45, 30),
     (42, 28), (40, 25), (38, 22), (36, 20), (35, 18), (33, 15), (30, 12),
     (28, 15), (30, 20), (32, 25), (35, 30), (38, 35), (40, 40), (42, 45),
     (45, 50), (48, 55), (50, 60), (45, 65), (40, 68), (35, 70), (30, 70)],
    [(113, -22), (115, -30), (118, -35), (122, -34), (125, -32), (130, -32),
     (132, -30), (135, -28), (138, -25), (140, -20), (142, -15), (143, -12),
     (145, -10), (147, -12), (148, -18), (150, -22), (152, -25), (153, -28),
     (150, -35), (148, -38), (145, -38), (142, -38), (140, -38), (138, -35),
     (135, -33), (132, -30), (130, -28), (128, -25), (125, -22), (122, -20),
     (118, -20), (115, -20), (113, -22)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (175, -40),
     (172, -42), (168, -45)],
    [(-5, 50), (-3, 52), (-2, 55), (-1, 58), (-3, 58), (-5, 56), (-6, 54),
     (-5, 50)],
]

# Small nudges (degrees) so neighbouring pins do not sit on each other.
PIN_NUDGE = {1: (-8, 4), 2: (-8, 5), 3: (-6, 0), 7: (8, -5), 9: (9, -4),
             4: (-8, 2), 6: (8, 3), 12: (10, -3), 15: (-4, -6),
             5: (-8, -4), 8: (5, -5), 13: (4, 7)}


def draw_map(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=SEA)
    for poly in CONTINENTS:
        pts = [(x0 + (lon + 180) / 360 * w, y0 + (90 - lat) / 180 * h)
               for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for n, lon, lat in PINS:
        dlon, dlat = PIN_NUDGE.get(n, (0, 0))
        px = x0 + (lon + dlon + 180) / 360 * w
        py = y0 + (90 - (lat + dlat)) / 180 * h
        r = 6
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        txt = str(n)
        tw = d.textlength(txt, font=F_PIN)
        d.text((px - tw / 2, py - 4), txt, font=F_PIN, fill=(255, 255, 255))


# -------------------------------------------------------------- layout

def section_head(d, x, y, text):
    d.text((x, y), text, font=F_SEC, fill=NAVY)
    d.line([x, y + 15, x + 90, y + 15], fill=RED, width=2)


def draw_header(d):
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.text((14, 8), "THE WORLD IN ONE PAGE", font=F_MAST, fill=(255, 255, 255))
    d.text((14, 48), "The day's most consequential news, drawn in one image",
           font=F_SUB, fill=(200, 215, 235))
    date = "FRIDAY 27 NOVEMBER 2026"
    dw = d.textlength(date, font=_font("DejaVuSans-Bold.ttf", 16))
    d.text((W - 14 - dw, 10), date, font=_font("DejaVuSans-Bold.ttf", 16),
           fill=(255, 215, 90))
    counts = "42 STORIES \u00b7 11 REGIONS \u00b7 19 FIELDS"
    cw = d.textlength(counts, font=F_SUB)
    d.text((W - 14 - cw, 48), counts, font=F_SUB, fill=(255, 255, 255))
    d.rectangle([0, 73, W, 76], fill=(255, 215, 90))


def draw_leads(d):
    y0, card_h = 84, 258
    col_w = (W - 2 * 8 - 2 * 8) // 3
    for i, lead in enumerate(LEADS):
        x = 8 + i * (col_w + 8)
        d.rounded_rectangle([x, y0, x + col_w, y0 + card_h], radius=6,
                            fill=CARD, outline=LINE, width=1)
        sx, sy = x + 6, y0 + 6
        SCENES[lead["kind"]](d, (sx, sy, x + col_w - 6, sy + 100))
        d.rectangle([sx, sy + 82, x + col_w - 6, sy + 100], fill=(20, 20, 20))
        d.text((sx + 6, sy + 86), lead["tag"], font=F_TAG, fill=(255, 215, 90))
        n_txt = str(lead["n"])
        d.ellipse([x + col_w - 26, sy + 6, x + col_w - 8, sy + 24], fill=RED)
        tw = d.textlength(n_txt, font=F_LEAD_WB)
        d.text((x + col_w - 17 - tw / 2, sy + 9), n_txt, font=F_LEAD_WB,
               fill=(255, 255, 255))
        cy = y0 + 112
        used = chip(d, x + 8, cy, lead["label"])
        d.text((x + 8 + used + 6, cy + 1),
               "%s \u00b7 %s" % (lead["region"], lead["field"]),
               font=F_CHIP, fill=MUTED)
        hy = y0 + 132
        lines = wrap(lead["headline"], F_LEAD_H, col_w - 16)
        draw_wrapped(d, x + 8, hy, lines, F_LEAD_H, INK, 19)
        dy = hy + 38
        lines = wrap(lead["deck"], F_LEAD_B, col_w - 16)
        draw_wrapped(d, x + 8, dy, lines, F_LEAD_B, (60, 58, 52), 14)
        wy = dy + 30
        d.text((x + 8, wy), "WHY IT MATTERS", font=F_LEAD_WB, fill=RED)
        lines = wrap(lead["why"], F_LEAD_W, col_w - 16)
        draw_wrapped(d, x + 8, wy + 13, lines, F_LEAD_W, INK, 13)
        d.text((x + 8, y0 + card_h - 16), lead["date_note"], font=F_LEAD_W,
               fill=MUTED)


def draw_grid(d):
    y0, row_h, gap = 362, 72, 6
    col_w = (W - 2 * 8 - 3 * 8) // 4
    d.text((8, 346), "MORE FROM FRIDAY \u2014 12 ILLUSTRATED STORIES",
           font=F_SEC, fill=NAVY)
    for i, med in enumerate(MEDIUMS):
        r, c = divmod(i, 4)
        x = 8 + c * (col_w + 8)
        y = y0 + r * (row_h + gap)
        d.rounded_rectangle([x, y, x + col_w, y + row_h], radius=5,
                            fill=CARD, outline=LINE, width=1)
        SCENES[med["kind"]](d, (x + 4, y + 4, x + 60, y + row_h - 4))
        d.rectangle([x + 4, y + 4, x + 22, y + 20], fill=(20, 20, 20))
        d.text((x + 8, y + 7), str(med["n"]), font=F_LEAD_WB,
               fill=(255, 255, 255))
        tx = x + 66
        lines = wrap(med["headline"], F_MED_H, col_w - 66 - 8)
        draw_wrapped(d, tx, y + 5, lines, F_MED_H, INK, 13)
        lines = wrap(med["deck"], F_MED_B, col_w - 66 - 8)
        draw_wrapped(d, tx, y + 33, lines, F_MED_B, (60, 58, 52), 12)
        d.text((tx, y + row_h - 14), med["region"], font=F_SRC, fill=MUTED)


def draw_bottom(d):
    y0 = 606
    d.line([8, 598, W - 8, 598], fill=LINE, width=1)
    # --- column A: numbered list 16-42
    section_head(d, 8, y0, "THE REST OF THE DAY \u00b7 27 MORE")
    ry = y0 + 20
    for n, label, region, head in LIST_ITEMS:
        d.rectangle([10, ry + 3, 16, ry + 9], fill=LABEL_FILL[label])
        d.text((20, ry), "%d." % n, font=F_LIST_N, fill=NAVY)
        d.text((44, ry), head, font=F_LIST, fill=INK)
        hw = d.textlength(head, font=F_LIST)
        d.text((44 + hw + 4, ry), "\u00b7 " + region, font=F_LIST, fill=MUTED)
        ry += 14
    # --- column B: map + timeline + sources
    section_head(d, 432, y0, "WHERE IT HAPPENED \u00b7 15 PINS")
    draw_map(d, (432, y0 + 20, 700, y0 + 158))
    ty = y0 + 164
    section_head(d, 432, ty, "THE DAY IN UTC")
    ty += 20
    for t, text in TIMELINE:
        d.text((432, ty), t, font=F_TL_T, fill=RED)
        lines = wrap(text, F_TL_B, 268 - 52)
        draw_wrapped(d, 432 + 46, ty, lines, F_TL_B, INK, 12)
        ty += 20
    sy = ty + 6
    section_head(d, 432, sy, "SOURCES")
    lines = wrap(SOURCES, F_SRC, 268 - 8)
    draw_wrapped(d, 432, sy + 20, lines, F_SRC, MUTED, 12)
    # --- column C: numbers + fields + date-check
    section_head(d, 708, y0, "THE DAY IN NUMBERS")
    ny = y0 + 20
    for big, label in NUMBERS:
        d.text((708, ny), big, font=F_NUM_B, fill=NAVY)
        lines = wrap(label, F_NUM_L, 308 - 16)
        draw_wrapped(d, 708, ny + 24, lines, F_NUM_L, INK, 12)
        ny += 48
        if big != NUMBERS[-1][0]:
            d.line([708, ny - 6, 1016, ny - 6], fill=LINE, width=1)
    fy = ny + 6
    section_head(d, 708, fy, "19 FIELDS COVERED")
    lines = wrap(" \u00b7 ".join(FIELDS), F_NUM_L, 308 - 16)
    draw_wrapped(d, 708, fy + 20, lines, F_NUM_L, INK, 13)
    by = fy + 20 + len(lines) * 13 + 8
    d.rounded_rectangle([708, by, 1016, 1004], radius=5, fill=GOLD_BG,
                        outline=GOLD, width=1)
    d.text((716, by + 6), "DATE-CHECK", font=F_LEAD_WB, fill=(120, 80, 0))
    dc = ("Every story above is dated Friday 27 November 2026. "
          "Carry-over items name their original date; one-sided claims "
          "are labelled CLAIM, never stated as fact.")
    lines = wrap(dc, F_NUM_L, 308 - 32)
    draw_wrapped(d, 716, by + 22, lines, F_NUM_L, INK, 13)
    # --- footer
    foot = ("Drawn from AP, Reuters and 14 other outlets \u00b7 All times "
            "UTC unless noted \u00b7 Labels: OFFICIAL = authority-confirmed "
            "\u00b7 REPORTED = named outlet \u00b7 CLAIM = one party\u2019s "
            "claim, unverified")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 1010), foot, font=F_FOOT, fill=MUTED)


def build():
    problems = check_fit()
    if problems:
        raise SystemExit("FIT CHECK FAILED:\n" + "\n".join(problems))
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_leads(d)
    draw_grid(d)
    draw_bottom(d)
    return img


def main(out_dir=None):
    img = build()
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(out_dir, "entry.png") if out_dir else \
        os.path.join(here, "entry.png")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    img.save(target, format="PNG")
    return target


if __name__ == "__main__":
    print(main())
