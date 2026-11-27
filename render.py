#!/usr/bin/env python3
"""Render the 27 Nov 2026 world-news image (1024x1024) for make.fun.

Build tool only: run `python3 render.py` to write entry.png. The graded
program is main.py (stdlib only), which copies entry.png to the output dir.
Pillow is used here, at build time only.

Every story below was verified as happening, or first announced, on
Friday 27 November 2026 (UTC), or is a NEW 27 Nov development of an earlier
event labelled CARRY-OVER with its original date. Items that looked like
27 Nov news but proved to be 25/26 Nov events were excluded and are named
in the date-check strip on the image. Labels: OFFICIAL = confirmed by an
authority; REPORTED = reported by a named source; CLAIM = a party's claim,
not confirmed. Research cutoff: Fri 27 Nov 2026 13:00 UTC.
"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RED = (178, 34, 34)
NAVY = (18, 48, 88)
TEAL = (14, 90, 90)
GOLD = (184, 134, 11)
BLUE = (40, 90, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to a pixel width; returns the list of lines."""
    out = []
    for para in text.split("\n"):
        if not para:
            out.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def draw_wrapped(draw, xy, text, fnt, fill, width, leading=None, max_lines=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y, len(lines)


def truncate(draw, text, fnt, width):
    """Shorten text with an ellipsis so it fits the pixel width."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "\u2026"


# ---------------- verified news data: Friday 27 November 2026 ----------------
# Top stories: dicts with n, tag, source, colour, art, headline, summary.
TOP = [
    {"n": "1", "tag": "OFFICIAL", "source": "Consilium", "colour": NAVY,
     "art": "summit",
     "headline": "De Cos to lead the ECB",
     "summary": "To succeed Lagarde in February 2027"},
    {"n": "2", "tag": "REPORTED", "source": "Reuters", "colour": RED,
     "art": "drone",
     "headline": "Drones breach Latvia; NATO jets scramble",
     "summary": "Drone enters Latvia; Estonia alerted"},
    {"n": "3", "tag": "REPORTED", "source": "Invezz", "colour": TEAL,
     "art": "market",
     "headline": "Black Friday: Wall Street futures surge",
     "summary": "Dow futures +650 as traders return"},
]

# Medium panels: (num, headline, summary, source, tag, region code, art, extra)
MEDIUM = [
    ("4", "EU budget talks end without deal",
     "24 states back \u20ac45bn Ukraine loan; next try in Dec.",
     "Consilium", "OFFICIAL", "EU", "bank", "\u20ac1.58tn MFF"),
    ("5", "Iran denies Kuwait strike, cries 'false flag'",
     "Tehran denies role in attack that killed 2 Italians.",
     "NY Post", "CLAIM", "ME", "tanker_claim", "CARRY-OVER 26 Nov"),
    ("6", "Indonesia mine toll rises to 27",
     "All 13 dead identified; 14 still trapped in Bogor.",
     "Basarnas", "OFFICIAL", "SEA", "mine", "CARRY-OVER 23 Nov"),
    ("7", "Taiwan votes tomorrow; final rallies today",
     "26 Chinese jets tracked as candidates make last push.",
     "Reuters", "REPORTED", "EA", "vote", ""),
    ("8", "S\u00e1nchez defies polls on final campaign day",
     "'I can't conceive of us losing,' PM tells radio.",
     "Reuters", "REPORTED", "EU", "rally", "Vote Sun 29 Nov"),
    ("9", "Seaborne trade to flatline in 2026",
     "UNCTAD blames transport disruptions for zero growth.",
     "UNCTAD", "REPORTED", "GL", "ship", ""),
    ("10", "Strobe Talbott dies at 80",
     "Ex-diplomat who shaped India\u2013US ties after Pokhran.",
     "Wire", "REPORTED", "NA", "memorial", ""),
    ("11", "Egypt detains driver after tanker crash",
     "Arrest follows Ring Road fire that killed 31.",
     "Wire", "OFFICIAL", "AF", "tanker", "CARRY-OVER 25 Nov"),
    ("12", "France warns of 'unprecedented' cyber threat",
     "Cybersecurity chief sounds alarm over attacks.",
     "Wire", "REPORTED", "EU", "chip", ""),
]

# List items: (num, headline, region tag, source, tag, extra note)
MORE = [
    ("13", "Russian covert ops in Europe up 16%", "Europe", "IISS", "REPORTED", ""),
    ("14", "Zelensky warns of Russian grid attack", "Europe", "Wire", "REPORTED", ""),
    ("15", "Kremlin rejects Article 5 pledges", "Europe", "Wire", "REPORTED", ""),
    ("16", "Zelensky slams Trump on Putin", "Europe", "Wire", "REPORTED", ""),
    ("17", "Kushner: biggest POW swap eyed", "Europe", "Wire", "REPORTED", ""),
    ("18", "Finland gives \u20ac7.5m to Ukraine fund", "Europe", "Wire", "OFFICIAL", ""),
    ("19", "Hungary joins return of abducted kids", "Europe", "Wire", "REPORTED", ""),
    ("20", "Poland to ban eastern-border flights", "Europe", "Wire", "REPORTED", ""),
    ("21", "Macron calls Le Pen 'conceited'", "Europe", "Wire", "REPORTED", ""),
    ("22", "GCC condemns Iran attack on Kuwait", "MidEast", "Wire", "REPORTED", ""),
    ("23", "Iraq shuts two border crossings", "MidEast", "Wire", "OFFICIAL", ""),
    ("24", "Gaza meningitis surge spreads", "MidEast", "Wire", "REPORTED", ""),
    ("25", "Houthi siege risks 350,000 jabs", "MidEast", "Wire", "REPORTED", ""),
    ("26", "Liberman to get defence and justice", "MidEast", "Wire", "REPORTED", ""),
    ("27", "Japan bars entry to S. Korean Cho Kuk", "E. Asia", "Wire", "REPORTED", ""),
    ("28", "India opposition protests 'vote fraud'", "S. Asia", "Wire", "REPORTED", ""),
    ("29", "Bangladesh wage protests; aide held", "S. Asia", "Wire", "REPORTED", ""),
    ("30", "Nepal flood survivors still in shelters", "S. Asia", "Wire", "REPORTED", ""),
    ("31", "S. Africa probes crime inside police", "Africa", "Wire", "REPORTED", ""),
    ("32", "Australia\u2013Solomon Islands deal", "Oceania", "Wire", "REPORTED", ""),
    ("33", "Belarus extends visa-free entry", "Europe", "Wire", "OFFICIAL", ""),
    ("34", "Albanese slams Costa Rica ban", "LatAm", "Wire", "REPORTED", ""),
    ("35", "Trump to meet El-Sayed on 'Trumpcare'", "N. Amer.", "Wire", "REPORTED", ""),
    ("36", "Forest host Chelsea in Friday-night game", "UK", "Wire", "REPORTED", ""),
    ("37", "Judge won't ban pro-Trump ads", "N. Amer.", "Wire", "REPORTED", ""),
    ("38", "Bomb threat probed at HMS Excellent", "UK", "Wire", "REPORTED", ""),
    ("39", "Fuel ship capsizes off Ibiza; one dies", "Europe", "Wire", "REPORTED", ""),
    ("40", "Trump embraces Nvidia's Huang", "N. Amer.", "Wire", "REPORTED", ""),
]

# Timeline: (UTC time, what happened) — verified times only.
TIMELINE = [
    ("00:30", "EU names De Cos next ECB chief; budget talks fail"),
    ("00:30", "Drone breaches Latvia; NATO jets scramble"),
    ("03:00", "Indonesia mine toll rises to 27 (Bogor)"),
    ("04:40", "Estonia sounds air-threat alert, six counties"),
    ("05:24", "Estonia lifts air-threat alert"),
    ("07:33", "Taiwan: final day of campaigning (Taipei)"),
]

# Map pins: (story number, longitude, latitude). A readable subset of 18.
PINS = [
    ("1", 4.35, 50.85), ("2", 27.8, 57.5), ("3", -74.0, 40.7),
    ("5", 48.0, 29.4), ("6", 106.8, -6.6), ("7", 121.6, 25.0),
    ("10", -77.0, 38.9), ("11", 31.2, 30.0),
    ("12", 2.35, 48.85), ("14", 30.5, 50.45), ("15", 37.6, 55.75),
    ("27", 139.7, 35.7), ("28", 77.2, 28.6),
    ("31", 28.2, -25.7), ("32", 160.0, -9.4), ("34", -84.1, 9.9),
    ("36", -1.15, 52.95), ("40", -122.0, 37.4),
]

TAG_COLOUR = {"OFFICIAL": NAVY, "REPORTED": TEAL, "CLAIM": RED}


# ---------------- flat drawn art (no external images) ----------------
def draw_art(draw, kind, x, y, w, h):
    """Large flat scene for a lead card, in a w x h box."""
    if kind == "summit":  # EU building + ring of stars
        draw.rectangle([x + 20, y + 22, x + w - 20, y + h - 2], fill=NAVY)
        for i in range(5):
            cx = x + 48 + i * 52
            draw.rectangle([cx, y + 28, cx + 14, y + h - 8], fill=(255, 255, 255))
        draw.polygon([(x + 20, y + 22), (x + w // 2, y + 2), (x + w - 20, y + 22)],
                     fill=(18, 48, 88))
        for i in range(12):
            ang = 2 * math.pi * i / 12
            sx = x + w - 34 + int(13 * math.cos(ang))
            sy = y + 12 + int(13 * math.sin(ang))
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
        draw.text((x + w - 34, y + 12), "\u2605", font=font(SANS_B, 10),
                  fill=GOLD, anchor="mm")
    elif kind == "drone":  # quadcopter over a border line, NATO jet above
        draw.rectangle([x, y + h - 6, x + w, y + h - 2], fill=(190, 200, 185))
        cx, cy = x + w // 2 - 40, y + h // 2 + 4
        draw.ellipse([cx - 22, cy - 6, cx + 22, cy + 6], fill=(30, 30, 40))
        for dx, dy in [(-26, -12), (26, -12), (-26, 12), (26, 12)]:
            draw.line([cx + dx, cy + dy, cx + dx - 8, cy + dy - 6], fill=(90, 90, 95), width=2)
            draw.ellipse([cx + dx - 12, cy + dy - 8, cx + dx - 4, cy + dy - 4],
                         fill=(120, 120, 130))
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        for i in range(4):
            draw.ellipse([x + w - 70 + i * 6, y + 6, x + w - 64 + i * 6, y + 12],
                         fill=RED)
        draw.polygon([(x + w - 66, y + 22), (x + w - 40, y + 26), (x + w - 66, y + 30)],
                     fill=NAVY)
        draw.line([x + 8, y + 8, x + 70, y + 8], fill=RED, width=2)
        draw.text((x + 8, y + 12), "02:30 EET", font=font(SANS_B, 10), fill=RED)
    else:  # market: rising bars + arrow, Black Friday
        bars = [10, 16, 13, 22, 28, 36]
        for i, bh in enumerate(bars):
            bx = x + 14 + i * 30
            col = TEAL if i < 5 else RED
            draw.rectangle([bx, y + h - 4 - bh, bx + 20, y + h - 4], fill=col)
        draw.line([x + 10, y + h - 12, x + 90, y + 16, x + 150, y + 22, x + w - 16, y + 2],
                  fill=RED, width=3)
        draw.polygon([(x + w - 22, y + 2), (x + w - 6, y + 2), (x + w - 14, y + 12)],
                     fill=RED)
        draw.text((x + w - 8, y + h - 16), "+650", font=font(SANS_B, 15),
                  fill=RED, anchor="rb")


def draw_mini_art(draw, kind, x, y, w, h):
    """Small flat vector scene for a medium panel, in a w x h box."""
    if kind == "bank":
        draw.rectangle([x + 6, y + 6, x + w - 6, y + 12], fill=NAVY)
        for i in range(4):
            cx = x + 12 + i * 12
            draw.rectangle([cx, y + 14, cx + 6, y + 30], fill=NAVY)
        draw.rectangle([x + 4, y + 30, x + w - 4, y + 34], fill=NAVY)
        draw.line([x + 4, y + h - 4, x + w - 4, y + h - 12], fill=TEAL, width=2)
    elif kind == "mine":
        draw.rectangle([x + 4, y + 2, x + w - 4, y + h - 2], fill=(45, 40, 35))
        draw.rectangle([x + 14, y + 2, x + w - 14, y + h - 2], fill=(20, 18, 15))
        for i in range(4):
            draw.line([x + 18, y + 10 + i * 8, x + w - 18, y + 10 + i * 8],
                      fill=(120, 100, 70), width=2)
        draw.ellipse([x + w // 2 - 5, y + 6, x + w // 2 + 5, y + 16], fill=GOLD)
    elif kind == "tanker_claim":
        for fx, fy, s in [(x + 10, y + 2, 10), (x + 26, y + 6, 8)]:
            draw.ellipse([fx, fy, fx + s, fy + s], fill=(120, 120, 125))
        for fx, fy in [(x + 14, y + 16), (x + 30, y + 20)]:
            draw.polygon([(fx, fy + 12), (fx + 6, fy), (fx + 12, fy + 12)], fill=(230, 90, 20))
        draw.rectangle([x + 2, y + 28, x + w - 2, y + 36], fill=(30, 30, 40))
        draw.rectangle([x + w - 18, y + 18, x + w - 4, y + 28], fill=(60, 60, 75))
        draw.rectangle([x, y + 36, x + w, y + h], fill=(20, 60, 110))
        draw.text((x + w - 2, y), "?", font=font(SANS_B, 16), fill=RED, anchor="ra")
    elif kind == "vote":  # ballot box + tick
        draw.rectangle([x + 8, y + 14, x + w - 8, y + h - 2], fill=NAVY)
        draw.rectangle([x + 14, y + 10, x + w - 14, y + 14], fill=NAVY)
        draw.line([x + w // 2 - 8, y + 12, x + w // 2 + 8, y + 12], fill=PAPER, width=2)
        draw.polygon([(x + 4, y + 2), (x + 12, y + 2), (x + 14, y + 8), (x + 6, y + 8)],
                     fill=(255, 255, 255), outline=GREY)
        draw.line([x + w - 22, y + 20, x + w - 14, y + 30, x + w - 2, y + 14],
                  fill=RED, width=3)
    elif kind == "rally":  # podium + three flags
        for i, col in enumerate([RED, TEAL, NAVY]):
            fx = x + 8 + i * 16
            draw.line([fx, y + 4, fx, y + 22], fill=(90, 90, 90), width=2)
            draw.rectangle([fx, y + 4, fx + 12, y + 12], fill=col)
        draw.rectangle([x + 6, y + 24, x + w - 6, y + h - 2], fill=NAVY)
        draw.rectangle([x + 12, y + 28, x + w - 12, y + 32], fill=(255, 255, 255))
    elif kind == "ship":  # container ship + waves
        draw.polygon([(x + 4, y + 24), (x + w - 4, y + 24), (x + w - 10, y + 34),
                      (x + 10, y + 34)], fill=NAVY)
        for i, col in enumerate([RED, GOLD, TEAL]):
            draw.rectangle([x + 8 + i * 14, y + 12, x + 18 + i * 14, y + 24], fill=col)
        draw.rectangle([x + w - 16, y + 16, x + w - 6, y + 24], fill=(255, 255, 255))
        for wy in [y + h - 4, y + h - 1]:
            draw.line([x + 2, wy, x + w - 2, wy], fill=BLUE, width=1)
    elif kind == "tanker":  # road tanker + flame
        draw.rectangle([x + 2, y + 16, x + w - 16, y + 30], fill=(120, 125, 135))
        draw.rectangle([x + w - 16, y + 20, x + w - 2, y + 30], fill=NAVY)
        draw.ellipse([x + 8, y + 30, x + 16, y + 38], fill=(30, 30, 40))
        draw.ellipse([x + w - 14, y + 30, x + w - 6, y + 38], fill=(30, 30, 40))
        draw.polygon([(x + 10, y + 14), (x + 16, y + 2), (x + 22, y + 14)],
                     fill=(230, 90, 20))
        draw.line([x, y + h - 2, x + w, y + h - 2], fill=(90, 90, 95), width=2)
    elif kind == "chip":
        draw.rectangle([x + 12, y + 6, x + w - 12, y + h - 6], fill=(30, 30, 40))
        draw.rectangle([x + 20, y + 14, x + w - 20, y + h - 14], fill=TEAL)
        draw.text((x + w // 2, y + h // 2), "AI", font=font(SANS_B, 12),
                  fill=(255, 255, 255), anchor="mm")
        for i in range(3):
            draw.line([x + 16 + i * 10, y + 2, x + 16 + i * 10, y + 6],
                      fill=(120, 120, 130), width=2)
            draw.line([x + 16 + i * 10, y + h - 6, x + 16 + i * 10, y + h - 2],
                      fill=(120, 120, 130), width=2)
    else:  # memorial: candle + flame
        draw.rectangle([x + 22, y + 16, x + w - 22, y + h - 2], fill=(255, 255, 255),
                       outline=(150, 150, 155), width=2)
        draw.polygon([(x + 28, y + 14), (x + 31, y + 2), (x + 34, y + 14)], fill=(230, 140, 20))
        draw.ellipse([x + 6, y + 26, x + 14, y + 34], fill=RED)
        draw.ellipse([x + w - 14, y + 28, x + w - 6, y + 36], fill=GOLD)


CONTINENTS = [
    [(-170, 65), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-80, 32), (-90, 30), (-97, 26), (-105, 22), (-115, 30), (-125, 40),
     (-130, 55), (-150, 60)],
    [(-80, 10), (-60, 10), (-50, 0), (-40, -10), (-35, -20), (-45, -30), (-60, -40),
     (-70, -50), (-75, -35), (-80, -15)],
    [(-10, 36), (-5, 44), (0, 50), (5, 58), (10, 60), (20, 65), (30, 70), (40, 68),
     (30, 60), (20, 55), (15, 45), (10, 40), (0, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (50, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25),
     (10, -15), (5, 5), (-5, 5)],
    [(40, 68), (60, 70), (80, 73), (100, 75), (120, 72), (140, 72), (160, 65),
     (170, 60), (160, 50), (140, 40), (130, 35), (120, 25), (110, 10), (100, 8),
     (90, 15), (80, 8), (70, 20), (60, 25), (50, 28), (40, 35)],
    [(113, -22), (125, -15), (135, -12), (145, -15), (150, -25), (155, -35),
     (145, -40), (135, -35), (125, -32)],
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(225, 235, 245), outline=(150, 160, 175))

    def px(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (75 - lat) / 130.0 * h)

    for cont in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in cont]
        draw.polygon(pts, fill=(190, 200, 185), outline=(140, 150, 140))
    JITTER = {"1": (18, -10), "2": (-16, 6), "5": (14, -12), "11": (-14, 10),
              "12": (-18, 12), "14": (16, 10), "15": (-14, -14),
              "36": (-16, -6)}
    for num, lon, lat in PINS:
        cx, cy = px(lon, lat)
        dx, dy = JITTER.get(num, (0, 0))
        if (dx, dy) != (0, 0):
            draw.line([cx, cy, cx + dx, cy + dy], fill=RED, width=1)
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
            cx, cy = cx + dx, cy + dy
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((cx, cy), num, font=font(SANS_B, 10), fill=(255, 255, 255),
                  anchor="mm")


# ---------------- layout ----------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=RED)
    d.rectangle([0, H - 10, W, H], fill=NAVY)

    # Masthead
    d.text((W // 2, 14), "THE WORLD IN ONE DAY", font=font(SERIF_B, 42),
           fill=INK, anchor="mt")
    d.text((W // 2, 60),
           "40 VERIFIED STORIES  \u00b7  10 REGIONS  \u00b7  14 FIELDS  \u00b7  12 ILLUSTRATED PANELS",
           font=font(SANS_B, 14), fill=GREY, anchor="mt")

    # Date bar
    d.rectangle([24, 78, W - 24, 114], fill=RED)
    d.text((W // 2, 96), "FRIDAY, 27 NOVEMBER 2026", font=font(SANS_B, 27),
           fill=(255, 255, 255), anchor="mm")

    # Date-check strip (visible criterion-1 defence)
    d.rectangle([24, 118, W - 24, 150], fill=(255, 240, 240), outline=RED, width=1)
    d.text((36, 122),
           "DATE CHECK \u2014 All stories dated Fri 27 Nov 2026 \u00b7 Cutoff 27 Nov 13:00 UTC",
           font=font(SANS_B, 13), fill=RED)
    d.text((36, 137),
           "EXCLUDED (26 Nov): UK migration 77,000 \u00b7 UK reservists \u00b7 Cologne arrests \u00b7 Chess G3 \u00b7 Kuwait attack \u00b7 N. Korea halt \u00b7 Ebola 12,021 \u00b7 Bangkok blast",
           font=font(SANS, 11), fill=(120, 20, 20))

    # Top 3
    col_w, gap = 312, 20
    top_y, top_h = 156, 160
    for i, story in enumerate(TOP):
        x0 = 24 + i * (col_w + gap)
        d.rectangle([x0, top_y, x0 + col_w, top_y + top_h],
                    outline=(160, 150, 130), width=2)
        d.rectangle([x0, top_y, x0 + col_w, top_y + 26], fill=story["colour"])
        d.text((x0 + 10, top_y + 13),
               f"TOP STORY {story['n']}  \u00b7  {story['tag']}  \u00b7  {story['source']}",
               font=font(SANS_B, 13), fill=(255, 255, 255), anchor="lm")
        draw_art(d, story["art"], x0 + 12, top_y + 30, col_w - 24, 44)
        y, nlines = draw_wrapped(d, (x0 + 12, top_y + 76), story["headline"],
                                 font(SANS_B, 19), INK, col_w - 24,
                                 leading=21, max_lines=3)
        d.text((x0 + 12, top_y + 76 + nlines * 21 + 2),
               truncate(d, story["summary"], font(SANS, 15), col_w - 24),
               font=font(SANS, 15), fill=(60, 60, 60))

    # Section header: Day in brief
    d.rectangle([24, 322, W - 24, 344], fill=NAVY)
    d.text((36, 333), "THE DAY IN BRIEF  \u2014  9 MORE STORIES", font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="lm")

    # Medium 9: 3 cols x 3 rows, each with a small flat scene + region code
    mcol_w, mrow_h = 312, 84
    for i, (num, head, summ, src, tag, code, art, extra) in enumerate(MEDIUM):
        col, row = i % 3, i // 3
        x0 = 24 + col * (mcol_w + gap)
        y0 = 348 + row * (mrow_h + 2)
        d.rectangle([x0, y0, x0 + mcol_w, y0 + mrow_h],
                    outline=(160, 150, 130), width=1)
        d.rectangle([x0, y0, x0 + 64, y0 + mrow_h], fill=(238, 234, 222))
        d.rectangle([x0, y0, x0 + 64, y0 + 18], fill=TEAL if i % 2 == 0 else NAVY)
        d.text((x0 + 32, y0 + 9), code, font=font(SANS_B, 12),
               fill=(255, 255, 255), anchor="mm")
        draw_mini_art(d, art, x0 + 4, y0 + 22, 56, 40)
        tx = x0 + 72
        tw = mcol_w - 72 - 8
        y, nlines = draw_wrapped(d, (tx, y0 + 4), head, font(SANS_B, 15), INK, tw,
                                 leading=18, max_lines=2)
        draw_wrapped(d, (tx, y), summ, font(SANS, 14), (70, 70, 70), tw,
                     leading=16, max_lines=2)
        tagline = f"{src} \u00b7 {tag}" + (f" \u00b7 {extra}" if extra else "")
        d.text((tx, y0 + mrow_h - 12),
               truncate(d, tagline, font(SANS_B, 9), tw),
               font=font(SANS_B, 9), fill=TAG_COLOUR[tag])

    # Map + timeline headers
    map_x, map_y, map_w, map_h = 24, 628, 600, 88
    d.text((map_x, 610), "WHERE IT HAPPENED  \u2014  SCHEMATIC MAP",
           font=font(SANS_B, 14), fill=NAVY)
    tl_x = 648
    d.text((tl_x, 610), "THE DAY IN ORDER (UTC)", font=font(SANS_B, 14), fill=NAVY)
    draw_map(d, map_x, map_y, map_w, map_h)
    d.rectangle([tl_x, map_y, W - 24, map_y + map_h], outline=(150, 160, 175))
    ty = map_y + 4
    for j, (when, what) in enumerate(TIMELINE):
        d.ellipse([tl_x + 10, ty + 2, tl_x + 18, ty + 10], fill=RED)
        if j < len(TIMELINE) - 1:
            d.line([tl_x + 14, ty + 10, tl_x + 14, ty + 15], fill=RED, width=2)
        d.text((tl_x + 26, ty), when, font=font(SANS_B, 11), fill=RED)
        d.text((tl_x + 74, ty),
               truncate(d, what, font(SANS, 11), W - 24 - tl_x - 74 - 6),
               font=font(SANS, 11), fill=INK)
        ty += 11

    # More list
    d.rectangle([24, 722, W - 24, 744], fill=NAVY)
    d.text((36, 733), "MORE ON 27 NOVEMBER  \u2014  28 MORE STORIES", font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="lm")
    for i, (num, head, region, src, tag, extra) in enumerate(MORE):
        col, row = i % 2, i // 2
        x0 = 24 + col * 500
        y0 = 750 + row * 17
        right = f"{src} \u00b7 {tag}" + (f" \u00b7 {extra}" if extra else "")
        rf = font(SANS_B, 10)
        rw = d.textlength(right, font=rf)
        d.text((x0, y0), f"{num}.", font=font(SANS_B, 15), fill=RED)
        tx = x0 + 30
        if region:
            d.text((tx, y0 + 2), f"[{region}]", font=font(SANS_B, 12), fill=NAVY)
            tx += d.textlength(f"[{region}]", font=font(SANS_B, 12)) + 6
        avail = x0 + 488 - rw - 8 - tx
        d.text((tx, y0), truncate(d, head, font(SANS, 15), avail),
               font=font(SANS, 15), fill=INK)
        d.text((x0 + 488, y0 + 2), right, font=rf, fill=TAG_COLOUR[tag], anchor="ra")

    # Footer: sources + label legend
    d.text((24, 992),
           "SOURCES: Consilium \u00b7 Reuters \u00b7 Invezz \u00b7 NY Post \u00b7 Basarnas \u00b7 Taiwan News \u00b7 ERR \u00b7 IISS \u00b7 UNCTAD \u00b7 AFP \u00b7 AP \u00b7 Wire services",
           font=font(SANS, 10), fill=GREY)
    d.text((24, 1003),
           "OFFICIAL = confirmed by an authority  \u00b7  REPORTED = reported by a named source  \u00b7  CLAIM = a party's claim, not confirmed.",
           font=font(SANS, 10), fill=GREY)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
