#!/usr/bin/env python3
"""Draw the news-image-20261125 front page: Wednesday 25 November 2026.

Renders ONE 1024x1024 PNG editorial front page with Pillow, entirely from
the story data below. Deterministic: no randomness, no clock, no network.
Every story was compiled on 25 November 2026 from wire reporting
(pm.gov.au, AP, Reuters, NOS, The Verge, NYT, Bloomberg and daily
digests) and each one happened, or was first reported, on 25 November
2026 in some time zone. Stories that only LOOK like 25 November news
(they happened on 24 Nov or earlier) are kept out and named in the
DATE CHECK box instead.

Run:  python3 gen.py        -> writes entry.png next to this file.
"""
import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (25, 25, 25)
RED = (166, 30, 34)
NAVY = (29, 58, 95)
TEAL = (14, 107, 98)
GOLD = (154, 123, 10)
GREY = (107, 107, 96)
LINE = (201, 194, 174)
CREAM = (255, 252, 240)
GREEN = (46, 110, 52)
AMBER = (146, 96, 0)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (number, kicker, headline, deck, certainty, scene, lon, lat)
LEADS = [
    (1, "CANBERRA \u00b7 TREATY", "PACIFIC PIVOT",
     "Solomon Islands name Australia their security partner of choice "
     "\u2014 and rule out any foreign military base on their soil.",
     "CONFIRMED", "treaty", 149.1, -35.3),
    (2, "PYONGYANG \u00b7 DIPLOMACY", "SWISS SHOWN THE DOOR",
     "North Korea orders its Swiss diplomatic office shut and its "
     "envoy out of the country within 48 hours.",
     "OFFICIAL", "expel", 125.8, 39.0),
    (3, "SHANGHAI \u00b7 POLITICS", "SHANGHAI FALLS IN LINE",
     "A day after its party chief's graft probe, the city's leaders "
     "pledge loyalty to Beijing.",
     "REPORTED", "shanghai", 121.5, 31.2),
]

# (number, kicker, headline, deck, certainty, icon, lon, lat)
CARDS = [
    (4, "MARKETS", "AI SHARES SLIDE",
     "Asian tech shares fall as AI wobbles.", "REPORTED",
     "chart", 139.7, 35.7),
    (5, "CYBER", "FINCEN CYBER INCIDENT",
     "FinCEN discloses a cybersecurity breach.", "REPORTED",
     "shield", -77.0, 38.9),
    (6, "AMERICAS", "ECUADOR OPS PAUSED",
     "US pauses joint operations with Ecuador.", "REPORTED",
     "flag", -78.5, -0.2),
    (7, "ECONOMY", "INFLATION STAYS HOT",
     "Core inflation jumps in Australia.", "REPORTED",
     "arrow", 133.0, -25.0),
    (8, "EUROPE", "EU CAPS CHINESE EVs",
     "Brussels to cap Chinese hybrid EVs.", "REPORTED",
     "car", 4.4, 50.8),
    (9, "ASIA", "MIGRANTS SENT BACK",
     "Malaysia to send 6,500 workers back.", "REPORTED",
     "people", 101.7, 3.1),
]

# One-liners for the "Also on Wednesday" list (26 items).
ALSO = [
    "Houthis threaten Saudi ports as Gulf tension rises",
    "Iraq cracks down on oil smuggling networks",
    "EU budget battle rages as Ukraine aid debated",
    "Poland, Latvia pushback rulings land in court",
    "Hungary rule-of-law worries grow in Brussels",
    "Violence against women rises in Germany",
    "Bulgaria wrestles with its fiscal squeeze",
    "Berlin Left expels lawmaker Vanessa Emde",
    "Bundestag rows over the 2027 budget",
    "Ifo index points to German recovery",
    "VW's Zwickau plant crisis deepens",
    "Green politician attacked in Germany",
    "Steinmeier urges business to look to Africa",
    "BJP and Akali Dal reunite for Punjab 2027",
    "England level T20 series with Australia",
    "Suryavanshi, 15, smashes 204* off 53 balls",
    "India orders 76 naval helicopters for \u20b915,000 Cr",
    "Delhi hosts first India\u2013EU maritime roundtable",
    "Varanasi glows for Dev Deepawali festival",
    "Iowa braces as Army plans lead-azide blast",
    "UN flags deepening hardship in Gaza",
    "Russia, Ukraine trade barbs at the UN",
    "US and Qatar talk strategy and cooperation",
    "Nvidia board faces scrutiny over CEO return",
    "School threat emails probed in Germany",
    "China study: robot dogs to guard moon bases",
]

DATE_CHECK = (
    "DATE CHECK \u2014 Left out on purpose: the Gaza Hamas-chief killing, the Cartagena "
    "hostage seizure, NATO's space vow, the Hormuz tanker claims, the Dutch climate "
    "ruling and the Nepal quake all happened on 24 Nov. So did the Sarkozy trial order; "
    "the Megaspeed blacklist was filed 23 Nov and the Chen probe announced 24 Nov. "
    "Only 25 November developments made this page."
)

FOOTER = (
    "Sources: pm.gov.au \u00b7 AP \u00b7 Reuters \u00b7 NOS \u00b7 The Verge \u00b7 NYT \u00b7 Bloomberg \u00b7 wire digests. "
    "Drawn from reporting of Wednesday 25 November 2026."
)

# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def chip(draw, x, y, label, fill):
    f = font(SANS_B, 11)
    w = draw.textlength(label, font=f) + 12
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def chip_color(certainty):
    if certainty == "CONFIRMED":
        return GREEN
    if certainty == "OFFICIAL":
        return NAVY
    return AMBER


def draw_scene(draw, kind, x, y, w, h):
    """Original drawn scene for a lead story (simple flat shapes)."""
    if kind == "treaty":
        # Sky, sun, parliament silhouette, table, two figures, two flags.
        draw.rectangle([x, y, x + w, y + h], fill=(213, 228, 240))
        draw.ellipse([x + w - 52, y + 12, x + w - 16, y + 48], fill=(240, 196, 90))
        draw.rectangle([x + 18, y + h - 78, x + w - 18, y + h - 58], fill=NAVY)
        draw.polygon([(x + 40, y + h - 78), (x + w // 2, y + h - 118),
                      (x + w - 40, y + h - 78)], fill=(23, 46, 76))
        for cx in range(x + 46, x + w - 40, 26):
            draw.rectangle([cx, y + h - 56, cx + 8, y + h - 30], fill=(240, 238, 228))
        draw.rectangle([x + 60, y + h - 30, x + w - 60, y + h - 18], fill=(122, 84, 52))
        # Flags on poles.
        for fx, col in ((x + 34, (0, 47, 108)), (x + w - 58, (0, 102, 153))):
            draw.rectangle([fx, y + 58, fx + 3, y + h - 58], fill=INK)
            draw.rectangle([fx + 3, y + 58, fx + 27, y + 78], fill=col)
            draw.ellipse([fx + 9, y + 64, fx + 13, y + 68], fill=(255, 255, 255))
            draw.ellipse([fx + 17, y + 70, fx + 21, y + 74], fill=(255, 255, 255))
        # Two figures shaking hands over the table: arms meet at the centre.
        for hx, suit in ((x + 118, NAVY), (x + 172, RED)):
            draw.ellipse([hx, y + h - 108, hx + 26, y + h - 82], fill=(232, 196, 160))
            draw.polygon([(hx - 4, y + h - 84), (hx + 30, y + h - 84),
                          (hx + 24, y + h - 30), (hx + 2, y + h - 30)], fill=suit)
        draw.line([x + 136, y + h - 62, x + 160, y + h - 56], fill=(232, 196, 160),
                  width=6)
        draw.line([x + 184, y + h - 62, x + 160, y + h - 56], fill=(232, 196, 160),
                  width=6)
        draw.rectangle([x + 96, y + h - 18, x + w - 96, y + h - 12], fill=(90, 60, 36))
    elif kind == "expel":
        # Red door with a white Swiss cross, diplomat with suitcase leaving.
        draw.rectangle([x, y, x + w, y + h], fill=(228, 222, 205))
        draw.rectangle([x + 30, y + 22, x + 150, y + h - 30], fill=(122, 20, 24))
        draw.rectangle([x + 78, y + 48, x + 102, y + 122], fill=(255, 255, 255))
        draw.rectangle([x + 62, y + 72, x + 118, y + 96], fill=(255, 255, 255))
        draw.rectangle([x + 26, y + 18, x + 154, y + 26], fill=INK)
        # Diplomat walking away with a suitcase.
        draw.ellipse([x + 196, y + 58, x + 220, y + 82], fill=(232, 196, 160))
        draw.polygon([(x + 192, y + 84), (x + 224, y + 84),
                      (x + 228, y + h - 30), (x + 188, y + h - 30)], fill=NAVY)
        draw.line([x + 196, y + 96, x + 182, y + 118], fill=INK, width=4)
        draw.line([x + 220, y + 96, x + 234, y + 118], fill=INK, width=4)
        draw.rectangle([x + 238, y + 108, x + 272, y + 136], fill=(122, 84, 52))
        draw.line([x + 234, y + 116, x + 238, y + 118], fill=INK, width=3)
        # "48 HOURS" tag in the clear sky at the top right.
        draw.rectangle([x + w - 128, y + 10, x + w - 12, y + 34], fill=RED)
        f = font(SANS_B, 15)
        draw.text((x + w - 120, y + 13), "48 HOURS", font=f, fill=(255, 255, 255))
    elif kind == "shanghai":
        # Skyline with the Oriental Pearl tower, red banner across.
        draw.rectangle([x, y, x + w, y + h], fill=(250, 214, 170))
        draw.ellipse([x + w - 66, y + 14, x + w - 18, y + 62], fill=(214, 48, 49))
        # Pearl tower: needle with two spheres.
        cx = x + 78
        draw.rectangle([cx - 3, y + 26, cx + 3, y + h - 30], fill=NAVY)
        draw.ellipse([cx - 22, y + 34, cx + 22, y + 78], fill=NAVY)
        draw.ellipse([cx - 15, y + 96, cx + 15, y + 126], fill=NAVY)
        # Stepped towers and blocks.
        for bx, bw, bh in ((x + 120, 34, 96), (x + 160, 26, 70),
                           (x + 192, 40, 118), (x + 238, 30, 84),
                           (x + 274, 26, 60)):
            draw.rectangle([bx, y + h - 30 - bh, bx + bw, y + h - 30],
                           fill=(58, 72, 96))
            for wy in range(y + h - 30 - bh + 10, y + h - 40, 16):
                for wx in range(bx + 5, bx + bw - 6, 12):
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(250, 214, 170))
        draw.rectangle([x, y + h - 30, x + w, y + h - 18], fill=(40, 40, 40))
        draw.rectangle([x + 20, y + h - 62, x + w - 20, y + h - 38], fill=RED)
        f = font(SANS_B, 14)
        draw.text((x + 34, y + h - 59), "LOYALTY PLEDGED", font=f,
                  fill=(255, 255, 255))


def draw_icon(draw, kind, x, y, s):
    """Small flat icon inside a s x s box."""
    c = NAVY
    if kind == "chart":
        draw.rectangle([x, y + s - 8, x + s, y + s - 4], fill=c)
        pts = [(x + 4, y + s - 16), (x + 16, y + s - 30), (x + 26, y + s - 22),
               (x + 38, y + s - 38), (x + 50, y + s - 12)]
        draw.line(pts, fill=RED, width=4, joint="curve")
    elif kind == "shield":
        draw.polygon([(x + s // 2, y + 4), (x + s - 4, y + 12),
                      (x + s - 4, y + s // 2), (x + s // 2, y + s - 4),
                      (x + 4, y + s // 2), (x + 4, y + 12)], fill=c)
        draw.line([(x + 16, y + s // 2), (x + 24, y + s // 2 + 8),
                   (x + 40, y + s // 2 - 8)], fill=(255, 255, 255), width=4)
    elif kind == "flag":
        draw.rectangle([x + 8, y + 4, x + 12, y + s - 4], fill=INK)
        draw.polygon([(x + 12, y + 6), (x + s - 4, y + 12),
                      (x + 12, y + 20)], fill=RED)
    elif kind == "arrow":
        draw.line([(x + 6, y + s - 10), (x + s - 8, y + 8)], fill=RED, width=5)
        draw.polygon([(x + s - 8, y + 8), (x + s - 22, y + 8),
                      (x + s - 8, y + 22)], fill=RED)
        draw.rectangle([x + 6, y + s - 12, x + s - 6, y + s - 8], fill=c)
    elif kind == "car":
        draw.rounded_rectangle([x + 4, y + s // 2, x + s - 4, y + s - 12],
                               radius=5, fill=c)
        draw.polygon([(x + 12, y + s // 2), (x + 18, y + 10),
                      (x + 36, y + 10), (x + 44, y + s // 2)], fill=c)
        draw.ellipse([x + 10, y + s - 16, x + 20, y + s - 6], fill=INK)
        draw.ellipse([x + s - 20, y + s - 16, x + s - 10, y + s - 6], fill=INK)
    elif kind == "people":
        for px, py in ((x + 8, y + 8), (x + s - 20, y + 8), (x + s // 2 - 6, y + 22)):
            draw.ellipse([px, py, px + 12, py + 12], fill=(232, 196, 160))
            draw.pieslice([px - 2, py + 12, px + 14, py + 30], 180, 360, fill=c)

# ---------------------------------------------------------------- world map
# Coarse hand-drawn continent outlines (lon, lat). Dotted style forgives
# the roughness; these coordinates are my own simplification.
CONTINENTS = [
    # North America
    [(-168, 66), (-158, 58), (-140, 60), (-130, 54), (-125, 49), (-124, 42),
     (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
     (-87, 13), (-83, 9), (-79, 9), (-77, 7), (-80, 25), (-81, 31),
     (-76, 35), (-74, 40), (-70, 42), (-68, 44), (-65, 45), (-60, 47),
     (-55, 52), (-60, 55), (-65, 60), (-68, 58), (-78, 62), (-85, 66),
     (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
     (-165, 68)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
     (-25, 76), (-35, 80), (-55, 80), (-60, 76), (-58, 70)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50),
     (-70, -54), (-66, -55), (-65, -45), (-62, -41), (-58, -35),
     (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9),
     (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-76, 10)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
     (37, 22), (39, 18), (43, 12), (48, 11), (51, 10), (46, 5),
     (42, 0), (40, -5), (40, -10), (38, -15), (36, -20), (33, -26),
     (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
     (13, -5), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
     (-2, 50), (0, 51), (3, 53), (5, 53), (8, 55), (8, 57), (10, 59),
     (12, 56), (18, 56), (21, 55), (24, 58), (28, 59), (30, 60),
     (30, 62), (32, 65), (35, 66), (40, 68), (50, 69), (60, 69),
     (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (158, 69), (162, 66), (170, 66),
     (178, 65), (178, 62), (170, 60), (162, 60), (158, 56), (156, 52),
     (150, 59), (142, 55), (140, 50), (135, 45), (132, 43), (128, 38),
     (126, 35), (122, 32), (120, 28), (118, 25), (112, 22), (109, 18),
     (106, 10), (104, 8), (100, 8), (98, 12), (97, 16), (94, 17),
     (92, 21), (89, 22), (86, 20), (82, 17), (80, 13), (77, 8),
     (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26),
     (56, 27), (52, 28), (50, 29), (48, 30), (44, 29), (42, 27),
     (39, 24), (38, 20), (35, 18), (34, 15), (33, 12), (30, 14),
     (27, 17), (22, 20), (18, 22), (15, 27), (12, 30), (10, 33),
     (0, 36), (-6, 36)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 38),
     (141, 41), (143, 43), (145, 44), (142, 45), (140, 42), (138, 38),
     (135, 34)],
    # Indonesia (thin chain) + New Guinea
    [(95, 5), (98, 3), (100, -2), (104, -4), (106, -6), (110, -7),
     (114, -8), (118, -9), (120, -10), (124, -9), (128, -8), (132, -4),
     (136, -3), (140, -4), (141, -8), (138, -9), (132, -8), (126, -10),
     (120, -11), (114, -9), (110, -8), (106, -7), (102, -4), (98, 0),
     (95, 3)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -8),
     (142, -8), (136, -6), (131, -3)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (137, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
     (114, -22)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (178, -38),
     (176, -40), (174, -42), (171, -44), (168, -46)],
]


def inside(lon, lat, poly):
    """Ray-casting point-in-polygon test."""
    ok = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                ok = not ok
        j = i
    return ok


def on_land(lon, lat):
    return any(inside(lon, lat, p) for p in CONTINENTS)


# ---------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22  # margin

    # ---- masthead ------------------------------------------------------
    d.rectangle([mx, 14, W - mx, 16], fill=INK)
    f_title = font(SERIF, 62)
    d.text((W // 2, 20), "THE WORLD IN ONE PAGE", font=f_title,
           fill=INK, anchor="ma")
    f_date = font(SANS_B, 30)
    d.text((W // 2, 92), "WEDNESDAY  25  NOVEMBER  2026", font=f_date,
           fill=RED, anchor="ma")
    f_strap = font(SANS_B, 15)
    d.text((W // 2, 128), "ONE DAY  \u00b7  SIX CONTINENTS  \u00b7  THIRTY-FIVE STORIES",
           font=f_strap, fill=NAVY, anchor="ma")
    d.rectangle([mx, 150, W - mx, 152], fill=INK)

    # ---- day in numbers -------------------------------------------------
    nums = [("35", "STORIES TODAY"), ("6", "CONTINENTS"),
            ("$740M", "TREATY AID, 10 YEARS"), ("48 HRS", "SWISS ENVOY TO LEAVE"),
            ("3", "LEAD STORIES")]
    cell_w = (W - 2 * mx) // 5
    y0, y1 = 158, 196
    for i, (big, small) in enumerate(nums):
        x0 = mx + i * cell_w
        if i:
            d.line([x0, y0 + 4, x0, y1 - 4], fill=LINE, width=1)
        d.text((x0 + cell_w // 2, y0 + 2), big, font=font(SERIF, 22),
               fill=RED, anchor="ma")
        d.text((x0 + cell_w // 2, y0 + 26), small, font=font(SANS_B, 10),
               fill=GREY, anchor="ma")
    d.rectangle([mx, y1, W - mx, y1 + 2], fill=INK)

    # ---- three lead stories ---------------------------------------------
    lead_y, lead_h, lead_w, gap = 204, 262, 320, 8
    for i, (num, kicker, head, deck, cert, scene, lon, lat) in enumerate(LEADS):
        x0 = mx + i * (lead_w + gap)
        d.rectangle([x0, lead_y, x0 + lead_w, lead_y + lead_h],
                    outline=INK, width=2)
        draw_scene(d, scene, x0 + 2, lead_y + 2, lead_w - 4, 150)
        ty = lead_y + 158
        d.text((x0 + 10, ty), kicker, font=font(SANS_B, 11), fill=RED)
        chip(d, x0 + lead_w - 92, ty - 2, cert, chip_color(cert))
        d.text((x0 + 10, ty + 18), head, font=font(SERIF, 20), fill=INK)
        for j, line in enumerate(wrap(d, deck, font(SANS, 13), lead_w - 20)):
            d.text((x0 + 10, ty + 50 + j * 16), line, font=font(SANS, 13),
                   fill=(51, 51, 51))
        # story number badge
        d.ellipse([x0 + 8, lead_y + 8, x0 + 34, lead_y + 34], fill=RED)
        d.text((x0 + 21, lead_y + 12), str(num), font=font(SANS_B, 15),
               fill=(255, 255, 255), anchor="ma")

    # ---- six story cards --------------------------------------------------
    card_y, card_h, card_w = 474, 62, 320
    for i, (num, kicker, head, deck, cert, icon, lon, lat) in enumerate(CARDS):
        row, col = divmod(i, 3)
        x0 = mx + col * (card_w + gap)
        y0 = card_y + row * (card_h + gap)
        d.rectangle([x0, y0, x0 + card_w, y0 + card_h], outline=LINE, width=1,
                    fill=CREAM)
        draw_icon(d, icon, x0 + 8, y0 + 8, 46)
        d.text((x0 + 62, y0 + 6), "%s  \u00b7  %s" % (kicker, cert),
               font=font(SANS_B, 10), fill=RED)
        d.text((x0 + 62, y0 + 20), head, font=font(SERIF, 15), fill=INK)
        d.text((x0 + 62, y0 + 42), deck, font=font(SANS, 11), fill=(51, 51, 51))
        d.ellipse([x0 + card_w - 26, y0 + 6, x0 + card_w - 6, y0 + 26],
                  fill=NAVY)
        d.text((x0 + card_w - 16, y0 + 9), str(num), font=font(SANS_B, 11),
               fill=(255, 255, 255), anchor="ma")

    # ---- dotted world map with numbered pins ------------------------------
    map_x0, map_y0, map_x1, map_y1 = mx, 614, W - mx, 788
    d.text((mx, map_y0), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=RED)
    d.line([mx, map_y0 + 18, W - mx, map_y0 + 18], fill=INK, width=1)
    my0, my1 = map_y0 + 24, map_y1
    lon0, lon1, lat0, lat1 = -170.0, 190.0, 78.0, -56.0

    def to_xy(lon, lat):
        px = map_x0 + (lon - lon0) / (lon1 - lon0) * (map_x1 - map_x0)
        py = my0 + (lat0 - lat) / (lat0 - lat1) * (my1 - my0)
        return px, py

    step = 3.0
    lon = lon0
    while lon <= lon1:
        lat = lat0
        while lat >= lat1:
            if on_land(lon, lat):
                px, py = to_xy(lon, lat)
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(29, 58, 95))
            lat -= step
        lon += step
    # Display offsets (degrees) so the crowded East Asia pins do not touch.
    pin_shift = {2: (3.0, 2.5), 3: (-3.0, -2.5)}
    for num, _k, _h, _de, _c, _s, lon, lat in LEADS + CARDS:
        dlon, dlat = pin_shift.get(num, (0.0, 0.0))
        px, py = to_xy(lon + dlon, lat + dlat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px, py - 7), str(num), font=font(SANS_B, 11),
               fill=(255, 255, 255), anchor="ma")

    # ---- also on Wednesday -------------------------------------------------
    ay = 796
    d.text((mx, ay), "ALSO ON WEDNESDAY \u2014 26 MORE STORIES",
           font=font(SANS_B, 13), fill=RED)
    d.line([mx, ay + 18, W - mx, ay + 18], fill=INK, width=1)
    col_w = (W - 2 * mx - 32) // 3
    f_item = font(SANS, 12)
    for idx, item in enumerate(ALSO):
        col, row = divmod(idx, 9)
        x0 = mx + col * (col_w + 16)
        y0 = ay + 24 + row * 16
        text = item
        while d.textlength(text, font=f_item) > col_w - 14 and " " in text:
            text = text.rsplit(" ", 1)[0]
        d.text((x0, y0), "\u2022  " + text, font=f_item, fill=(51, 51, 51))

    # ---- date check ---------------------------------------------------------
    dy = 962
    d.rectangle([mx, dy, W - mx, dy + 40], fill=(232, 226, 205),
                outline=RED, width=1)
    f_dc = font(SANS, 11)
    lines = wrap(d, DATE_CHECK, f_dc, W - 2 * mx - 24)
    for j, line in enumerate(lines[:3]):
        d.text((mx + 12, dy + 4 + j * 12), line, font=f_dc, fill=INK)

    # ---- footer ---------------------------------------------------------------
    d.text((W // 2, 1008), FOOTER, font=font(SANS, 10), fill=GREY,
           anchor="ma")
    return img


def main():
    total = len(LEADS) + len(CARDS) + len(ALSO)
    assert total == 35, "story count is %d, want 35" % total
    img = build()
    assert img.size == (1024, 1024)
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    assert len(data) <= 1048576, "entry.png is %d bytes, over 1 MiB" % len(data)
    print("entry.png: %d bytes, sha256 %s, %d stories"
          % (len(data), hashlib.sha256(data).hexdigest(), total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
