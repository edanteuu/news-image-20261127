#!/usr/bin/env python3
"""Draw the 27 November 2026 world-news broadsheet, 1024x1024.

Fresh implementation written for the v3 revision. All story facts come from
the verified research notes (news-27nov-v2.md); every drawing routine, helper
and layout block below was authored in this session.
"""
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# Palette -- warm paper, near-black ink, one red and one blue accent.
PAPER_BG = (251, 248, 239)
CARD_BG = (255, 255, 255)
INK_TXT = (24, 24, 30)
SOFT_TXT = (92, 92, 102)
RULE_COL = (24, 24, 30)
RED_ACC = (176, 32, 28)
BLUE_ACC = (26, 58, 110)
GOLD_ACC = (196, 148, 44)
TEAL_ACC = (18, 110, 105)
LIGHT_LINE = (205, 200, 186)
SCENE_SKY = (214, 230, 242)
SCENE_SKY_DUSK = (250, 214, 178)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _load(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


def serif_b(size):
    return _load("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _load("DejaVuSerif.ttf", size)


def sans_b(size):
    return _load("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _load("DejaVuSans.ttf", size)


def mono_b(size):
    return _load("DejaVuSansMono-Bold.ttf", size)


# ---------------------------------------------------------------- text tools

def split_lines(draw, text, font, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    if not words:
        return []
    lines = []
    cur = words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def para(draw, x, y, text, font, fill, max_w, leading):
    """Draw wrapped paragraph; return y just below the last line."""
    for ln in split_lines(draw, text, font, max_w):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def clipped(draw, text, font, max_w):
    """Shorten with an ellipsis until it fits max_w."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."


def tag_chip(draw, x, y, label, fill):
    """Small filled status chip; returns the x just past it."""
    f = sans_b(11)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=8, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x + w


def section_head(draw, x, y, label):
    f = sans_b(13)
    draw.text((x, y), label, font=f, fill=RED_ACC)
    w = int(draw.textlength(label, font=f))
    draw.line([x + w + 10, y + 7, x + 210, y + 7], fill=LIGHT_LINE, width=1)
    return y + 20


# ------------------------------------------------------------ scene painters
# Each paints a small flat illustration inside the given box. All use only
# rectangles, ellipses, polygons and lines -- no pasted art.

def paint_rising_chart(d, box, line_col=TEAL_ACC):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=SCENE_SKY)
    fracs = [0.28, 0.44, 0.36, 0.58, 0.52, 0.74, 0.66, 0.88]
    pts = [(x0 + 8 + i * 22, int(y1 - f * h)) for i, f in enumerate(fracs)]
    d.line(pts, fill=line_col, width=4)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED_ACC)
    d.text((x0 + 8, y0 + 4), "+5.6%", font=sans_b(15), fill=INK_TXT)


def paint_city_towers(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=SCENE_SKY_DUSK)
    heights = [0.50, 0.76, 0.58, 0.90, 0.66, 0.82, 0.52]
    bw = (x1 - x0 - 16) // len(heights)
    for i, hf in enumerate(heights):
        bh = int(hf * h)
        bx = x0 + 8 + i * bw
        d.rectangle([bx, y1 - bh, bx + bw - 4, y1], fill=BLUE_ACC)
        for wy in range(y1 - bh + 6, y1 - 5, 11):
            d.rectangle([bx + 3, wy, bx + 7, wy + 4], fill=GOLD_ACC)
    d.ellipse([x1 - 30, y0 + 4, x1 - 12, y0 + 22], fill=GOLD_ACC)


def paint_parliament(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    cx, cy = (x0 + x1) // 2, y1 - 4
    d.rectangle(box, fill=(232, 238, 245))
    for rf, col in ((0.78, RED_ACC), (0.58, BLUE_ACC), (0.38, GOLD_ACC)):
        ring = int(rf * h)
        d.arc([cx - ring, cy - ring, cx + ring, cy + ring], 180, 360, fill=col, width=6)
    d.text((x0 + 8, y0 + 4), "65 / 130", font=sans_b(15), fill=INK_TXT)
    d.text((x0 + 8, y0 + 22), "1 SHORT", font=sans_b(10), fill=RED_ACC)


def paint_drone_sky(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=SCENE_SKY)
    for fx, fy, rf in ((0.24, 0.45, 0.30), (0.70, 0.62, 0.36), (0.48, 0.80, 0.22)):
        cx, cy, r = x0 + int(fx * (x1 - x0)), y0 + int(fy * h), int(rf * h)
        d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(140, 160, 180), width=1)
    d.rectangle([x0 + 66, y0 + int(0.30 * h), x0 + 106, y0 + int(0.55 * h)], fill=INK_TXT)
    d.ellipse([x0 + 62, y0 + int(0.28 * h), x0 + 70, y0 + int(0.58 * h)], fill=INK_TXT)
    d.ellipse([x0 + 102, y0 + int(0.28 * h), x0 + 110, y0 + int(0.58 * h)], fill=INK_TXT)
    d.line([x0 + 86, y0 + int(0.55 * h), x0 + 86, y0 + int(0.85 * h)], fill=RED_ACC, width=2)


def paint_shopfront(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(245, 226, 200))
    for i in range(6):
        col = RED_ACC if i % 2 == 0 else (255, 255, 255)
        d.polygon([(x0 + 8 + i * 28, y0 + 4), (x0 + 32 + i * 28, y0 + 4),
                   (x0 + 28 + i * 28, y0 + int(0.42 * h)), (x0 + 12 + i * 28, y0 + int(0.42 * h))],
                  fill=col)
    d.rectangle([x0 + 30, y0 + int(0.55 * h), x0 + 62, y1 - 4], fill=BLUE_ACC)
    d.rectangle([x0 + 96, y0 + int(0.55 * h), x0 + 128, y1 - 4], fill=TEAL_ACC)
    d.rectangle([x0 + 138, y0 + int(0.68 * h), x0 + 166, y1 - 4], fill=GOLD_ACC)


def paint_tanker_sea(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(198, 222, 235))
    d.rectangle([x0 + 14, y1 - int(0.38 * h), x0 + 150, y1 - int(0.18 * h)], fill=(90, 60, 50))
    d.rectangle([x0 + 100, y1 - int(0.62 * h), x0 + 118, y1 - int(0.38 * h)], fill=(120, 80, 60))
    for sx in (x0 + 128, x0 + 140, x0 + 152):
        d.ellipse([sx, y0 + 2, sx + 14, y0 + int(0.30 * h)], fill=(150, 150, 150))
    d.line([x0 + 10, y1 - 6, x1 - 10, y1 - 6], fill=BLUE_ACC, width=2)


def paint_rally(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(238, 228, 245))
    for i, cx in enumerate(range(x0 + 22, x1 - 10, 26)):
        d.ellipse([cx - 7, y1 - int(0.72 * h), cx + 7, y1 - int(0.42 * h)], fill=INK_TXT)
        d.rectangle([cx - 9, y1 - int(0.42 * h), cx + 9, y1 - 6], fill=RED_ACC if i % 2 else BLUE_ACC)
    d.rectangle([x0 + 50, y0 + 4, x0 + 56, y0 + int(0.85 * h)], fill=(120, 90, 60))
    d.polygon([(x0 + 56, y0 + 4), (x0 + 92, y0 + int(0.14 * h)), (x0 + 56, y0 + int(0.26 * h))],
              fill=RED_ACC)


def paint_mine_hill(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(226, 214, 190))
    d.polygon([(x0, y1), (x0 + 60, y0 + int(0.30 * h)), (x1, y1)], fill=(120, 96, 66))
    d.polygon([(x0 + 60, y0 + int(0.30 * h)), (x0 + 110, y0 + int(0.68 * h)),
               (x0 + 60, y0 + int(0.82 * h))], fill=(90, 72, 48))
    d.rectangle([x0 + 18, y1 - int(0.42 * h), x0 + 44, y1 - 6], fill=GOLD_ACC)


def paint_office_chip(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(228, 234, 240))
    d.rectangle([x0 + 16, y0 + 6, x0 + 52, y1 - 6], fill=BLUE_ACC)
    d.rectangle([x0 + 60, y0 + int(0.30 * h), x0 + 88, y1 - 6], fill=(150, 170, 195))
    d.rectangle([x0 + 108, y0 + int(0.38 * h), x0 + 148, y0 + int(0.88 * h)], fill=INK_TXT)
    for dx in (-14, 0, 14):
        d.line([x0 + 128 + dx, y0 + int(0.38 * h), x0 + 128 + dx, y0 + int(0.24 * h)],
               fill=GOLD_ACC, width=3)
    d.text((x0 + 112, y0 + int(0.52 * h)), "AI", font=sans_b(14), fill=(255, 255, 255))


def paint_boat(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(198, 222, 235))
    d.polygon([(x0 + 30, y1 - int(0.42 * h)), (x0 + 140, y1 - int(0.42 * h)),
               (x0 + 122, y1 - int(0.14 * h)), (x0 + 48, y1 - int(0.14 * h))],
              fill=(140, 70, 40))
    d.rectangle([x0 + 76, y0 + int(0.16 * h), x0 + 82, y1 - int(0.42 * h)], fill=(120, 90, 60))
    d.polygon([(x0 + 82, y0 + int(0.18 * h)), (x0 + 118, y1 - int(0.48 * h)),
               (x0 + 82, y1 - int(0.48 * h))], fill=(255, 255, 255))
    d.line([x0 + 8, y1 - 6, x1 - 8, y1 - 6], fill=BLUE_ACC, width=2)


def paint_oval(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(196, 224, 178))
    d.ellipse([x0 + 8, y0 + 18, x1 - 8, y1 - 10], outline=(255, 255, 255), width=3)
    d.line([x0 + 30, y0 + 8, x0 + 30, y1 - 8], fill=(255, 255, 255), width=3)
    d.line([x1 - 30, y0 + 8, x1 - 30, y1 - 8], fill=(255, 255, 255), width=3)
    d.text((x0 + 8, y0 + 4), "44-18", font=sans_b(15), fill=INK_TXT)


def paint_stadium(d, box):
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(210, 216, 228))
    d.polygon([(x0 + 10, y1 - 8), (x0 + 40, y0 + int(0.24 * h)), (x1 - 40, y0 + int(0.24 * h)),
               (x1 - 10, y1 - 8)], fill=BLUE_ACC)
    for fx in (x0 + 46, x0 + 86, x0 + 126):
        d.line([fx, y0 + int(0.36 * h), fx, y0 + int(0.66 * h)], fill=GOLD_ACC, width=3)
        d.ellipse([fx - 3, y0 + int(0.30 * h), fx + 3, y0 + int(0.42 * h)], fill=RED_ACC)
    d.ellipse([(x0 + x1) // 2 - 14, y0 + int(0.55 * h), (x0 + x1) // 2 + 14, y0 + int(0.92 * h)],
              fill=(255, 255, 255))


# ------------------------------------------------------------------- the day
# Facts verified in news-27nov-v2.md. Each item: (headline, deck, why-it-
# matters, source, status, region, scene painter).

LEADS = [
    ("Wall St caps best week since April",
     "S&P +1.60% to 7,297.49; Nasdaq +2.31%. Week: S&P +5.6%, best since April 2025.",
     "Why it matters: the rebound caps a week that repaired October's sell-off.",
     "AP", "REPORTED", "N AMERICA", paint_rising_chart),
    ("EU names De Cos next ECB president",
     "De Cos, ex-Bank of Spain and now BIS chief, succeeds Lagarde on 7 Feb 2027.",
     "Why it matters: the pick sets euro-zone rates policy for the next eight years.",
     "Consilium", "OFFICIAL", "EUROPE", paint_city_towers),
    ("NZ coalition falls one seat short",
     "National 40 + ACT 13 + NZ First 12 = 65 of 130, one short of 66.",
     "Why it matters: a first-term newcomer now decides who governs New Zealand.",
     "Electoral Commission", "REPORTED", "OCEANIA", paint_parliament),
]

MEDIUMS = [
    ("Drones breach Latvia; NATO jets scramble",
     "Unidentified drone violates Latvian airspace; NATO jets scramble. Estonia sounds an air-threat alert across six counties.",
     "Reuters", "REPORTED", "EUROPE", paint_drone_sky),
    ("Black Friday opens: $12.9bn day ahead",
     "Adobe forecasts $12.9bn in US online sales, up 9.2% on last year, as stores open for the biggest shopping day.",
     "Adobe", "REPORTED", "N AMERICA", paint_shopfront),
    ("Tokyo inflation 2.9%; Nikkei jumps 2.11%",
     "Tokyo core CPI rises 2.9%, its fastest in 16 months, keeping a December BOJ hike in play. Nikkei closes at 58,711.",
     "Reuters", "REPORTED", "E ASIA", paint_city_towers),
    ("Iran says tanker hit its mines in Hormuz",
     "IRGC Navy says a tanker exploded after hitting naval mines north of Ghavam Island. Not independently verified; no vessel named.",
     "Fars", "CLAIM", "M EAST", paint_tanker_sea),
    ("Spain's campaign ends; Sanchez defies polls",
     "Final day before Sunday's snap election. Sanchez tells SER radio he 'can't conceive of us losing'. PP leads at ~31%.",
     "Reuters", "REPORTED", "EUROPE", paint_rally),
    ("Indonesia mine: toll rises to 27",
     "Basarnas counts one more victim in the Bogor mine flood; 13 dead, 14 missing. Police identify all 13 dead.",
     "Basarnas", "OFFICIAL", "SE ASIA", paint_mine_hill),
    ("SAP weighs 10,000+ job cuts in AI push",
     "Bloomberg: SAP is preparing a plan to cut at least 10,000 jobs, about 9% of staff, as it rebuilds around AI. No decision made.",
     "Bloomberg", "REPORTED", "EUROPE", paint_office_chip),
    ("Seoul sends six North Koreans home",
     "South Korea repatriates six of seven fishermen found adrift near Ulleung Island; the seventh chooses to stay in the South.",
     "Reuters", "REPORTED", "E ASIA", paint_boat),
    ("North Melbourne seal AFLW three-peat, 44-18",
     "Kangaroos beat Melbourne in the rain at Ikon Park, the first premiership three-peat in AFLW history. Crowd 12,659.",
     "AFL", "REPORTED", "OCEANIA", paint_oval),
    ("Macron condemns Marseille fan violence",
     "Presidents Macron and Iotova condemn pre-match violence; five Levski fans in hospital. UEFA appoints ethics inspectors.",
     "AFP", "REPORTED", "EUROPE", paint_stadium),
]

LIST_ITEMS = [
    ("EU summit ends without deal; Ukraine loan backed", "OFFICIAL"),
    ("Iran denies Kuwait strike, cries 'false flag'", "CLAIM"),
    ("Taiwan: final campaign day; 26 jets tracked", "REPORTED"),
    ("Kim vows a bigger nuclear arsenal", "REPORTED"),
    ("Gold rebounds; silver +6%; 10-year 4.92%", "REPORTED"),
    ("Amazon workers strike in 20+ countries", "REPORTED"),
    ("Serbia students pick Saicic for president", "REPORTED"),
    ("Antonelli fastest in Qatar GP practice, 1:23.217", "REPORTED"),
    ("Thanksgiving storm: 500,000+ without power", "REPORTED"),
    ("UNCTAD: seaborne trade to flatline in 2026", "REPORTED"),
    ("Strobe Talbott dies at 80", "REPORTED"),
    ("Egypt detains driver after tanker crash", "OFFICIAL"),
    ("France warns of 'unprecedented' cyber threat", "REPORTED"),
    ("Meloni: EU 'far' from budget deal", "REPORTED"),
    ("Zelensky rebukes 'my friend' jibe", "REPORTED"),
    ("Turkey summons Georgia's envoy", "REPORTED"),
    ("Eisenkot aims for cabinet in 8 days", "REPORTED"),
    ("Islamabad hosts defence-pact talks", "REPORTED"),
    ("Pakistan checks Libya boat reports", "REPORTED"),
    ("ACCC warns on AI-made sale deals", "REPORTED"),
    ("Hunter rail strike called off", "REPORTED"),
    ("F2 pole for debutant Ugochukwu, 1:35.818", "REPORTED"),
    ("RSF raids kill 14 in Darfur and Kordofan", "REPORTED"),
    ("Hong Kong marks tower-fire anniversary", "REPORTED"),
    ("FTSE 100 closes up 0.8% at 10,698.81", "REPORTED"),
    ("Brazil keeps ex-BRB chief jailed", "REPORTED"),
    ("SpaceX shares for US children with Trump Acct", "REPORTED"),
]

NUMBERS = [
    ("65/130", "NZ coalition seats; 66 needed"),
    ("+5.6%", "S&P best week since Apr 2025"),
    ("2.9%", "Tokyo CPI, 16-month high"),
    ("44-18", "AFLW three-peat"),
    ("10,000+", "SAP jobs at risk in AI revamp"),
    ("$12.9bn", "Forecast US Black Friday sales"),
]

TIMELINE = [
    ("00:30", "EU names De Cos; budget talks end"),
    ("00:30", "Drone breaches Latvia; NATO jets up"),
    ("01:00", "NZ final count: coalition 65 of 130"),
    ("03:00", "Indonesia mine toll rises to 27"),
    ("04:40", "Estonia air-threat alert, six counties"),
    ("06:00", "Nikkei +2.11%; Tokyo CPI 2.9%"),
    ("11:00", "AFLW three-peat sealed, 44-18"),
    ("18:00", "Wall St closes: S&P +1.60%"),
    ("23:00", "Spain's campaign closes"),
]

SOURCES_LINE = "AP  ·  Reuters  ·  Consilium  ·  Electoral Commission NZ  ·  AFL  ·  F1  ·  FIA F2  ·  Bloomberg  ·  Adobe  ·  Basarnas  ·  ERR  ·  AFP  ·  UNCTAD  ·  UNI Global  ·  Fars / Anadolu"
EXCLUDED_LINE = "DATE CHECK — not counted as 27 Nov news: Kuwait strike itself (26 Nov) · UK migration 77,000 (26 Nov) · Chess Game 3 (26 Nov) · Bangkok refinery blast (26 Nov) · Ebola data (26 Nov) · Macy's parade postponement (26 Nov) · Marseille violence itself (26 Nov) · Hong Kong tower fire itself (26 Nov 2025)"
REGION_LINE = "EUROPE 12  ·  N AMERICA 5  ·  MIDDLE EAST 5  ·  EAST ASIA 5  ·  OCEANIA 4  ·  GLOBAL 3  ·  AFRICA 2  ·  SOUTH ASIA 2  ·  SE ASIA 1  ·  LATIN AMERICA 1"


# ------------------------------------------------------------------- layout

def draw_masthead(d, y):
    d.rectangle([0, 0, CANVAS_W, 104], fill=INK_TXT)
    d.text((24, 10), "THE WORLD IN ONE DAY", font=serif_b(28), fill=(255, 255, 255))
    d.text((24, 46), "Friday, 27 November 2026", font=serif(22), fill=GOLD_ACC)
    d.text((24, 80), "40 VERIFIED STORIES  ·  10 REGIONS  ·  13 FIELDS  ·  13 ILLUSTRATED PANELS",
           font=sans_b(13), fill=(255, 255, 255))
    d.text((CANVAS_W - 24, 12), "ALL FROM", font=sans_b(12), fill=(200, 200, 205), anchor="ra")
    d.text((CANVAS_W - 24, 30), "FRIDAY", font=sans_b(20), fill=(255, 255, 255), anchor="ra")
    d.text((CANVAS_W - 24, 54), "27 NOV 2026", font=sans_b(20), fill=(255, 255, 255), anchor="ra")
    d.text((CANVAS_W - 24, 80), "EVERY ITEM DATED", font=sans_b(10), fill=(200, 200, 205), anchor="ra")
    return 104


def draw_leads(d, y):
    y = section_head(d, 24, y + 4, "THE THREE BIGGEST STORIES")
    top = y
    cw = 312
    gap = 20
    for i, (head, deck, why, src, status, region, painter) in enumerate(LEADS):
        x = 24 + i * (cw + gap)
        d.rounded_rectangle([x, top, x + cw, top + 210], radius=6, outline=LIGHT_LINE, fill=CARD_BG)
        painter(d, (x + 8, top + 8, x + cw - 8, top + 66))
        yy = top + 72
        tag_chip(d, x + 10, yy, status, RED_ACC if status == "CLAIM" else BLUE_ACC)
        d.text((x + 10, yy + 19), region + "  ·  " + src, font=sans_b(11), fill=SOFT_TXT)
        yy = para(d, x + 10, yy + 36, head, sans_b(16), INK_TXT, cw - 20, 20)
        yy = para(d, x + 10, yy + 3, deck, sans(11), SOFT_TXT, cw - 20, 14)
        para(d, x + 10, top + 182, why, sans_b(11), RED_ACC, cw - 20, 13)
    return top + 210


def draw_numbers(d, y):
    y += 10
    d.rectangle([0, y, CANVAS_W, y + 50], fill=(238, 232, 214))
    d.text((24, y + 5), "THE DAY IN NUMBERS", font=sans_b(12), fill=RED_ACC)
    seg = (CANVAS_W - 48) // len(NUMBERS)
    for i, (num, cap) in enumerate(NUMBERS):
        x = 24 + i * seg
        d.text((x, y + 20), num, font=sans_b(17), fill=INK_TXT)
        d.text((x, y + 38), clipped(d, cap, sans(10), seg - 8), font=sans(10), fill=SOFT_TXT)
    return y + 50


def draw_mediums(d, y):
    y = section_head(d, 24, y + 6, "AROUND THE WORLD")
    top = y
    cols, rows = 5, 2
    cw = (CANVAS_W - 48 - (cols - 1) * 12) // cols
    ch = 112
    for idx, (head, deck, src, status, region, painter) in enumerate(MEDIUMS):
        r, c = divmod(idx, cols)
        x = 24 + c * (cw + 12)
        yy = top + r * (ch + 10)
        d.rounded_rectangle([x, yy, x + cw, yy + ch], radius=5, outline=LIGHT_LINE, fill=CARD_BG)
        painter(d, (x + 6, yy + 6, x + cw - 6, yy + 44))
        tag_chip(d, x + 8, yy + 48, status, RED_ACC if status == "CLAIM" else TEAL_ACC)
        para(d, x + 8, yy + 68, head, sans_b(11), INK_TXT, cw - 16, 13)
        d.text((x + 8, yy + ch - 13), region + "  ·  " + src, font=sans(9), fill=SOFT_TXT)
    return top + rows * (ch + 10) - 10


def draw_list(d, y):
    y = section_head(d, 24, y + 4, "ALSO ON FRIDAY — 27 MORE STORIES")
    top = y
    cols = 3
    cw = (CANVAS_W - 48 - (cols - 1) * 16) // cols
    f = sans(10)
    for idx, (head, status) in enumerate(LIST_ITEMS):
        c, r = divmod(idx, 9)
        x = 24 + c * (cw + 16)
        yy = top + r * 17
        d.text((x, yy), "%2d." % (idx + 14), font=mono_b(10), fill=RED_ACC)
        label = clipped(d, head, f, cw - 72)
        d.text((x + 28, yy), label, font=f, fill=INK_TXT)
        d.text((x + cw - 44, yy), status, font=sans_b(8), fill=SOFT_TXT)
    return top + 9 * 17 + 4


def draw_bottom(d, y):
    d.rectangle([0, y, CANVAS_W, CANVAS_H], fill=INK_TXT)
    d.text((24, y + 6), "WHERE IT HAPPENED  ·  13 PINS, ILLUSTRATED STORIES ONLY",
           font=sans_b(11), fill=GOLD_ACC)
    d.text((24, y + 22), "1 New York   2 Brussels   3 Wellington   4 Ludza   5 New York   6 Tokyo",
           font=sans(11), fill=(255, 255, 255))
    d.text((24, y + 37), "7 Hormuz   8 Madrid   9 Bogor   10 Walldorf   11 Ulleung Is.   12 Melbourne   13 Marseille",
           font=sans(11), fill=(255, 255, 255))
    d.text((24, y + 55), "TIMELINE (UTC)", font=sans_b(11), fill=GOLD_ACC)
    tcol_w = (CANVAS_W - 48) // 3
    for idx, (t, what) in enumerate(TIMELINE):
        c, r = divmod(idx, 3)
        tx = 24 + c * tcol_w
        tyy = y + 71 + r * 14
        d.text((tx, tyy), t + "  " + clipped(d, what, sans(10), tcol_w - 48),
               font=sans(10), fill=(255, 255, 255))
    d.line([0, y + 122, CANVAS_W, y + 122], fill=(80, 80, 90), width=1)
    para(d, 24, y + 126, EXCLUDED_LINE, sans(9), (200, 200, 205), CANVAS_W - 48, 11)
    d.text((24, y + 150), SOURCES_LINE, font=sans(8), fill=(160, 160, 170))
    return CANVAS_H


def build():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER_BG)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d, 0)
    d.text((24, y + 4), REGION_LINE, font=sans(10), fill=SOFT_TXT)
    y += 20
    y = draw_leads(d, y)
    y = draw_numbers(d, y)
    y = draw_mediums(d, y)
    y = draw_list(d, y)
    draw_bottom(d, y)
    img.save(OUT_PATH, optimize=True)
    return OUT_PATH


if __name__ == "__main__":
    print(build())
