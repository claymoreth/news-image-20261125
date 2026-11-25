#!/usr/bin/env python3
"""Build the news-image-20261125 entry: one 1024x1024 newspaper page.

Source: Mana's own 30-story summary of Wednesday 25 November 2026.
Deterministic: no time, no randomness, no network. PIL only.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 234)
NAVY = (16, 28, 58)
RED = (207, 31, 38)
INK = (25, 25, 25)
GREY = (96, 96, 96)
GREEN = (46, 139, 87)
GOLD = (176, 132, 24)
OLIVE = (148, 138, 88)
LINEC = (200, 190, 175)

FDIR = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FDIR + "LiberationSerif-Bold.ttf"
SERIF_R = FDIR + "LiberationSerif-Regular.ttf"
SERIF_I = FDIR + "LiberationSerif-Italic.ttf"
SANS_B = FDIR + "LiberationSans-Bold.ttf"
SANS_R = FDIR + "LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, max_w, max_lines, min_size=8):
    """Shrink font until text wraps to at most max_lines; return (font, lines)."""
    s = size
    while s > min_size:
        fnt = font(path, s)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        s -= 0.5
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def fit_single(draw, text, path, size, max_w, min_size=7):
    """Shrink font until text fits on one line; return font."""
    s = size
    while s > min_size:
        fnt = font(path, s)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        s -= 0.5
    return font(path, min_size)


# ---------------------------------------------------------------- thumbnails
def thumb_hero_kospi():
    im = Image.new("RGB", (648, 260), (13, 22, 46))
    d = ImageDraw.Draw(im)
    for gy in (52, 104, 156, 208):
        d.line([(30, gy), (618, gy)], fill=(255, 255, 255), width=1)
    bars = [(70, 60, 150), (190, 95, 185), (310, 130, 205), (430, 165, 225)]
    for x0, y0, y1 in bars:
        d.rectangle([x0, y0, x0 + 70, y1], fill=(207, 31, 38))
    d.rectangle([540, 195, 600, 225], fill=(46, 139, 87))
    pts = [(40, 55), (150, 80), (240, 105), (330, 130), (430, 165),
           (520, 195), (610, 225)]
    d.line(pts, fill=(255, 80, 80), width=6, joint="curve")
    return im


def thumb_hero_riyadh():
    im = Image.new("RGB", (648, 260), (232, 122, 48))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 200, 648, 260], fill=(38, 30, 26))
    # tower dead center
    d.rectangle([289, 40, 359, 200], fill=(16, 28, 58))
    d.polygon([(289, 40), (324, 18), (359, 40)], fill=(16, 28, 58))
    for r in range(5):
        for c in range(4):
            d.rectangle([299 + c * 15, 55 + r * 28, 309 + c * 15, 65 + r * 28],
                        fill=(255, 214, 120))
    # smoke plume at the top
    d.ellipse([296, 0, 336, 26], fill=(150, 150, 150))
    d.ellipse([308, 8, 352, 34], fill=(170, 170, 170))
    d.ellipse([282, 10, 318, 32], fill=(130, 130, 130))
    # flame at the crown
    d.polygon([(314, 22), (324, 2), (334, 22)], fill=(255, 190, 0))
    return im


def thumb_hero_kremlin():
    im = Image.new("RGB", (648, 260), (168, 205, 232))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 215, 648, 260], fill=(240, 240, 235))
    # red-brick wall with three towers
    d.rectangle([60, 150, 588, 215], fill=(178, 58, 48))
    for tx in (110, 294, 478):
        d.rectangle([tx, 90, tx + 60, 215], fill=(150, 40, 34))
        d.rectangle([tx + 22, 66, tx + 38, 92], fill=(150, 40, 34))
    domes = [(140, (46, 139, 87)), (324, (36, 84, 160)), (508, (212, 175, 55))]
    for cx, col in domes:
        d.ellipse([cx - 28, 30, cx + 28, 74], fill=col)
        d.rectangle([cx - 2, 14, cx + 2, 32], fill=(212, 175, 55))
    d.line([(0, 215), (648, 215)], fill=(255, 255, 255), width=4)
    return im


def thumb_card_nikkei():
    im = Image.new("RGB", (576, 168), (13, 22, 46))
    d = ImageDraw.Draw(im)
    # big red downward arrow, centered-left
    d.rectangle([120, 22, 160, 108], fill=(207, 31, 38))
    d.polygon([(80, 104), (200, 104), (140, 152)], fill=(207, 31, 38))
    for i, bh in enumerate((30, 48, 66)):
        x0 = 260 + i * 80
        d.rectangle([x0, 140 - bh, x0 + 48, 140], fill=(207, 31, 38))
    return im


def thumb_card_flags():
    im = Image.new("RGB", (576, 168), (247, 242, 234))
    d = ImageDraw.Draw(im)
    for i in range(5):
        x = 70 + i * 105
        d.line([(x, 30), (x, 140)], fill=(120, 120, 120), width=4)
        d.polygon([(x, 30), (x + 78, 46), (x, 66)], fill=(232, 110, 20))
    return im


def thumb_card_nvidia():
    im = Image.new("RGB", (576, 168), (18, 77, 44))
    d = ImageDraw.Draw(im)
    cx, cy = 288, 84
    for i in range(6):  # pins, all four sides
        d.rectangle([cx - 90 + i * 36, cy - 66, cx - 78 + i * 36, cy - 48],
                    fill=(120, 200, 140))
        d.rectangle([cx - 90 + i * 36, cy + 48, cx - 78 + i * 36, cy + 66],
                    fill=(120, 200, 140))
        d.rectangle([cx - 66, cy - 60 + i * 24, cx - 48, cy - 48 + i * 24],
                    fill=(120, 200, 140))
        d.rectangle([cx + 48, cy - 60 + i * 24, cx + 66, cy - 48 + i * 24],
                    fill=(120, 200, 140))
    d.rectangle([cx - 48, cy - 48, cx + 48, cy + 48], fill=(46, 139, 87))
    d.rectangle([cx - 24, cy - 24, cx + 24, cy + 24], fill=(140, 220, 160))
    return im


def thumb_card_ship():
    im = Image.new("RGB", (576, 168), (70, 130, 190))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 84, 576, 168], fill=(30, 80, 150))
    d.line([(0, 84), (576, 84)], fill=(255, 255, 255), width=2)
    # hull with containers
    d.polygon([(110, 96), (466, 96), (440, 140), (140, 140)], fill=(90, 90, 90))
    d.rectangle([110, 96, 466, 104], fill=(60, 60, 60))
    for i, col in enumerate(((207, 31, 38), (36, 84, 160), (212, 175, 55),
                             (46, 139, 87))):
        d.rectangle([150 + i * 80, 62, 214 + i * 80, 96], fill=col)
    d.rectangle([430, 60, 466, 96], fill=(240, 240, 240))
    # drone above with dotted path
    for i in range(6):
        d.ellipse([300 + i * 14, 26, 306 + i * 14, 32], fill=(255, 255, 255))
    d.ellipse([370, 18, 396, 34], fill=(25, 25, 25))
    d.line([(362, 26), (404, 26)], fill=(25, 25, 25), width=3)
    return im


def thumb_card_rupiah():
    im = Image.new("RGB", (576, 168), (247, 242, 234))
    d = ImageDraw.Draw(im)
    d.rectangle([88, 34, 488, 134], fill=(178, 222, 178))
    d.rectangle([88, 34, 488, 134], outline=(46, 139, 87), width=4)
    d.ellipse([238, 54, 338, 114], outline=(46, 139, 87), width=4)
    d.ellipse([268, 74, 308, 94], fill=(46, 139, 87))
    # red downward arrow across the note
    d.rectangle([150, 48, 168, 96], fill=(207, 31, 38))
    d.polygon([(132, 92), (186, 92), (159, 128)], fill=(207, 31, 38))
    return im


def thumb_card_vaccine():
    im = Image.new("RGB", (576, 168), (255, 255, 255))
    d = ImageDraw.Draw(im)
    # vial with blue liquid
    d.rectangle([180, 60, 240, 130], fill=(220, 235, 245))
    d.rectangle([180, 60, 240, 130], outline=(90, 130, 170), width=3)
    d.rectangle([184, 96, 236, 126], fill=(40, 110, 200))
    d.rectangle([192, 48, 228, 60], fill=(120, 120, 120))
    # diagonal syringe: clear barrel, grey plunger, thin needle
    d.line([(300, 130), (430, 30)], fill=(150, 150, 150), width=3)
    d.line([(300, 130), (430, 30)], fill=(200, 220, 240), width=14)
    d.line([(300, 130), (430, 30)], fill=(150, 150, 150), width=3)
    d.line([(296, 134), (322, 108)], fill=(120, 120, 120), width=8)
    d.line([(430, 30), (452, 12)], fill=(180, 180, 180), width=3)
    d.line([(418, 42), (442, 18)], fill=(120, 120, 120), width=6)
    return im


def thumb_card_well():
    im = Image.new("RGB", (576, 168), (232, 205, 160))
    d = ImageDraw.Draw(im)
    # stone well
    d.ellipse([208, 78, 368, 138], fill=(150, 140, 120))
    d.ellipse([228, 88, 348, 122], fill=(40, 110, 180))
    d.ellipse([228, 88, 348, 122], outline=(120, 110, 90), width=4)
    # wooden frame
    d.rectangle([212, 30, 224, 92], fill=(120, 82, 40))
    d.rectangle([352, 30, 364, 92], fill=(120, 82, 40))
    d.rectangle([200, 24, 376, 36], fill=(140, 96, 48))
    # bucket hanging
    d.line([(288, 36), (288, 62)], fill=(90, 60, 30), width=3)
    d.rectangle([268, 62, 308, 84], fill=(160, 110, 60))
    return im


AFRICA_POLY = [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
               (32, -28), (25, -34), (18, -35), (15, -27), (12, -18),
               (9, -1), (9, 4), (-8, 4), (-13, 8)]


def thumb_card_africa():
    im = Image.new("RGB", (576, 168), (247, 242, 234))
    d = ImageDraw.Draw(im)
    pts = []
    for lon, lat in AFRICA_POLY:
        x = 40 + (lon + 17) / 68.0 * 496
        y = 14 + (35 - lat) / 70.0 * 140
        pts.append((x, y))
    d.polygon(pts, fill=NAVY)
    # red awareness ribbon: loop at upper center, two short tails
    # crossing below the loop
    d.ellipse([258, 36, 318, 96], outline=RED, width=10)
    d.line([(276, 92), (252, 130)], fill=RED, width=10)
    d.line([(300, 92), (324, 130)], fill=RED, width=10)
    return im


def thumb_card_tanker():
    im = Image.new("RGB", (576, 168), (20, 60, 110))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 110, 576, 168], fill=(12, 40, 80))
    # hull, black with red bottom, white superstructure
    d.polygon([(80, 78), (496, 78), (470, 122), (110, 122)], fill=(20, 20, 20))
    d.polygon([(96, 108), (480, 108), (470, 122), (110, 122)],
              fill=(178, 40, 40))
    d.rectangle([420, 44, 480, 78], fill=(240, 240, 240))
    d.rectangle([436, 30, 464, 44], fill=(240, 240, 240))
    # yellow warning triangle above
    d.polygon([(288, 8), (252, 52), (324, 52)], fill=(255, 200, 0))
    d.rectangle([284, 24, 292, 38], fill=(20, 20, 20))
    d.rectangle([284, 42, 292, 48], fill=(20, 20, 20))
    return im


def thumb_card_waves():
    im = Image.new("RGB", (576, 168), (40, 110, 190))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 138, 576, 168], fill=(232, 205, 160))
    for i, (x0, y0, x1, y1) in enumerate(
            [(40, 60, 240, 140), (200, 40, 400, 140), (360, 60, 540, 140)]):
        d.arc([x0, y0, x1, y1], 180, 360, fill=(255, 255, 255), width=14)
        d.arc([x0 + 8, y0 + 14, x1 - 8, y1], 180, 360, fill=(220, 240, 255),
              width=6)
    return im


# ---------------------------------------------------------------- map
CONTINENTS = {
    "na": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80),
           (-85, 70), (-75, 62), (-65, 60), (-55, 47), (-70, 42),
           (-75, 35), (-80, 25), (-85, 20), (-90, 15), (-95, 18),
           (-105, 20), (-110, 23), (-120, 32), (-125, 40), (-130, 55),
           (-150, 60)],
    "sa": [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5), (-35, -10),
           (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50),
           (-73, -40), (-72, -20), (-78, -5)],
    "eu": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 70),
           (40, 68), (45, 60), (40, 50), (35, 45), (30, 42), (28, 40),
           (23, 36), (19, 40), (15, 38), (12, 44), (8, 44), (3, 43),
           (-2, 37)],
    "af": AFRICA_POLY,
    "as": [(30, 70), (40, 68), (55, 70), (70, 72), (90, 75), (110, 74),
           (130, 72), (150, 70), (170, 66), (178, 65), (162, 60),
           (158, 52), (142, 50), (140, 40), (135, 35), (127, 33),
           (122, 38), (120, 30), (110, 20), (105, 10), (100, 8),
           (95, 15), (90, 22), (85, 20), (80, 8), (77, 8), (72, 20),
           (66, 25), (60, 25), (55, 28), (50, 30), (48, 30), (43, 35),
           (36, 36), (30, 42)],
    "se": [(95, 5), (105, 0), (110, -5), (115, -8), (120, -10), (130, -5),
           (135, 0), (140, -5), (140, 2), (130, 5), (120, 8), (105, 10)],
    "au": [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
           (137, -35), (140, -38), (145, -38), (150, -37), (153, -27),
           (150, -22), (146, -19), (142, -11), (136, -12), (132, -11),
           (126, -14), (122, -17), (118, -20)],
    "nz": [(167, -45), (170, -42), (174, -39), (178, -38), (175, -41),
           (172, -43), (168, -47)],
}


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (
                x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


# ---------------------------------------------------------------- content
STATS = [("-5.3%", "Kospi's plunge in Seoul"),
         ("Rp18.269", "rupiah per US dollar"),
         ("US$150.5", "thermal coal, per ton"),
         ("350,000", "Taiz children miss vaccines"),
         ("129", "orange flags at the UN"),
         ("22,100", "women killed in Africa")]

TABS = ["SE ASIA 5", "EAST ASIA 5", "MID EAST 5", "EUROPE 5",
        "N AMERICA 5", "S AMERICA 2", "AFRICA & OCE 3"]
TAB_COLORS = [RED, (36, 84, 160), GOLD, (34, 120, 74), (110, 62, 150),
              (20, 130, 138), NAVY]

HEROES = [
    dict(bar="SEOUL: MARKETS PLUNGE", badge="25 NOV", badge_color=GREEN,
         tag="-5.3%", caption="Red boards across Asia",
         loc="6 SEOUL \u00b7 EAST ASIA \u00b7 MARKETS",
         head="Kospi dives 4.49% to 5.3% as Asian stocks slide",
         deck="Tech shares lead Asia lower on fresh US tariff threats; "
              "Nikkei falls and Taiwan drops more than 5%.",
         thumb=thumb_hero_kospi),
    dict(bar="RIYADH: TOWER STRUCK", badge="25 NOV", badge_color=GREEN,
         tag="HOUTHI", caption="Riyadh's tallest tower, after the strike",
         loc="11 RIYADH \u00b7 MIDDLE EAST \u00b7 WAR",
         head="Houthis strike Riyadh's tallest building",
         deck="Yemen's Houthis say they hit the capital's tallest tower "
              "and warn Red Sea ports are next.",
         thumb=thumb_hero_riyadh),
    dict(bar="MOSCOW: RETALIATION VOWED", badge="25 NOV", badge_color=GOLD,
         tag="PUTIN", caption="The Kremlin, Moscow",
         loc="16 MOSCOW \u00b7 EUROPE \u00b7 WAR",
         head="Putin: Russian retaliation cannot be avoided",
         deck="President says retaliation is inevitable, accusing Ukraine "
              "of continuing to hit his oil refineries.",
         thumb=thumb_hero_kremlin),
]

CARDS = [
    dict(bar="TOKYO: MARKETS FALL",
         loc="TOKYO & TAIPEI, EAST ASIA \u00b7 MARKETS",
         head="Nikkei slides; Taiwan drops over 5%",
         deck="Japan and Taiwan follow Wall Street lower as tech shares "
              "sink across the region.",
         thumb=thumb_card_nikkei),
    dict(bar="NEW YORK: 129 FLAGS",
         loc="NEW YORK, AMERICAS \u00b7 UN",
         head="UN flies 129 orange flags for femicide victims",
         deck="The UN marks the day against violence towards women with "
              "one flag for each daily victim worldwide.",
         thumb=thumb_card_flags),
    dict(bar="SANTA CLARA: NVIDIA",
         loc="CALIFORNIA, AMERICAS \u00b7 TECH",
         head="Jensen Huang returns as Nvidia CEO",
         deck="Huang is back as chief executive after the board accepts "
              "US security clarifications.",
         thumb=thumb_card_nvidia),
    dict(bar="FINLAND: SHIP STRUCK",
         loc="GULF OF FINLAND, EUROPE \u00b7 WAR",
         head="Ukraine says it hit a Russian ship off Finland",
         deck="Kyiv claims a strike on a Russian vessel in Finnish waters "
              "and drone hits on the Crimea bridge.",
         thumb=thumb_card_ship),
    dict(bar="JAKARTA: RUPIAH SLIPS",
         loc="JAKARTA, SE ASIA \u00b7 MARKETS",
         head="Rupiah weakens to Rp18.269 per dollar",
         deck="The rupiah opens lower at Rp18.269\u201318.271 as demand for "
              "safe-haven assets rises.",
         thumb=thumb_card_rupiah),
    dict(bar="GAZA: UNRWA STAFF KILLED",
         loc="JABALYA, MIDDLE EAST \u00b7 AID",
         head="UNRWA worker killed near Gaza water well",
         deck="One UNRWA staffer is killed and three hurt in a strike "
              "near a water well in northern Gaza.",
         thumb=thumb_card_well),
    dict(bar="AFRICA: 22,100 KILLED",
         loc="AFRICA, WORLD \u00b7 UN REPORT",
         head="Africa records highest domestic-violence toll",
         deck="A UN report counts 22,100 women killed by partners or "
              "family in Africa, the highest of any region.",
         thumb=thumb_card_africa),
    dict(bar="WASHINGTON: TANKER PROBE",
         loc="WASHINGTON, AMERICAS \u00b7 SECURITY",
         head="US probes cyberattack on about 50 tankers",
         deck="Washington investigates a suspected cyberattack on some 50 "
              "oil and chemical tankers.",
         thumb=thumb_card_tanker),
    dict(bar="TAIZ: VACCINES MISSED",
         loc="TAIZ, MIDDLE EAST \u00b7 HEALTH",
         head="350,000 Taiz children miss measles shots",
         deck="The UN says about 350,000 children in Taiz missed measles "
              "and rubella jabs amid blockade and fighting.",
         thumb=thumb_card_vaccine),
    dict(bar="GORDON'S BAY: WAVES",
         loc="WESTERN CAPE, AFRICA \u00b7 WEATHER",
         head="3\u20134 metre waves flood South Africa coast",
         deck="Waves of 3 to 4 metres wash over the shore at Gordon's Bay "
              "and along the coast.",
         thumb=thumb_card_waves),
]

PINS = [(6, 127.0, 37.5, 0, -10), (11, 46.7, 24.7, 10, -12),
        (16, 37.6, 55.8, 0, -12), (7, 139.7, 35.7, 0, 10),
        (21, -74.0, 40.7, 0, -12), (23, -122.0, 37.4, -8, 10),
        (17, 24.0, 60.0, 12, -8), (4, 106.8, -6.2, 0, 12),
        (14, 34.5, 31.5, -14, 0), (28, 20.0, 5.0, 0, 0),
        (22, -77.0, 39.0, -14, 12), (13, 44.0, 13.6, 0, 14),
        (29, 18.9, -34.2, 0, -6)]

MORE = [
    (1, "Teachers' Day marked across Indonesia"),
    (2, "BEM SI rallies at the palace from 13:00 WIB with seven demands"),
    (3, "Today is the deadline for regions to set 2027 minimum wages"),
    (5, "Vietnam holds E5 petrol price before tomorrow's review"),
    (8, "India urges human control over AI warfare at the UN"),
    (9, "Thermal coal tops US$150.5 a ton on China port demand"),
    (10, "Pakistan plans mandatory registration for social media"),
    (12, "Iraq sacks border ports chief and North Oil leaders over smuggling"),
    (15, "Qatar PM in Washington to mediate the US\u2013Iran deadlock"),
    (18, "UN convoy brings food and medicine to Kherson's front line"),
    (19, "Leaked data logs about 1,000 suicides among Russian troops"),
    (20, "Germany pressed over cuts to anti-racism funding"),
    (24, "CIA hit by hack of its unclassified systems"),
    (25, "Two killed as helicopter hits a hill in Temecula, California"),
    (26, "Americas records 7,400 femicide victims last year"),
    (27, "Brazil confirmed as 2027 Women's World Cup host"),
    (30, "Hyatt opens Andaz Gold Coast resort in Broadbeach"),
]


def build():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)

    # top navy bar
    d.rectangle([0, 0, W, 27], fill=NAVY)
    d.text((14, 6), "THE WORLD IN ONE DAY", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    f = font(SANS_B, 9)
    t = "30 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS ONE DAY \u00b7 " \
        "PRESS TIME 04:00 UTC"
    d.text((W - 14 - d.textlength(t, font=f), 8), t, font=f,
           fill=(255, 255, 255))

    # masthead
    f = font(SERIF_B, 54)
    t = "Wednesday 25 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 30), t, font=f, fill=NAVY)

    # ticker
    ticker = "KOSPI: -5.3% \u00b7 RIYADH: Houthis strike tallest tower " \
             "\u00b7 PUTIN: retaliation unavoidable \u00b7 NEW YORK: 129 " \
             "orange flags \u00b7 JAKARTA: rupiah Rp18.269"
    f = fit_single(d, ticker, SERIF_I, 15, W - 28)
    d.text(((W - d.textlength(ticker, font=f)) / 2, 88), ticker, font=f,
           fill=RED)

    # stats row
    d.line([(14, 106), (W - 14, 106)], fill=LINEC, width=1)
    d.line([(14, 140), (W - 14, 140)], fill=LINEC, width=1)
    cw = 166
    for i, (num, lab) in enumerate(STATS):
        cx = 14 + i * cw + cw / 2
        f = font(SERIF_B, 23)
        d.text((cx - d.textlength(num, font=f) / 2, 108), num, font=f,
               fill=RED)
        f = font(SANS_R, 9)
        d.text((cx - d.textlength(lab, font=f) / 2, 131), lab, font=f,
               fill=GREY)
        if i:
            d.line([(14 + i * cw, 110), (14 + i * cw, 136)], fill=LINEC,
                   width=1)

    # region tabs
    tw = 996 / 7
    for i, (lab, col) in enumerate(zip(TABS, TAB_COLORS)):
        x0 = 14 + i * tw
        d.rectangle([x0, 142, x0 + tw - 2, 158], fill=col)
        f = font(SANS_B, 10)
        d.text((x0 + (tw - 2) / 2 - d.textlength(lab, font=f) / 2, 145),
               lab, font=f, fill=(255, 255, 255))

    # heroes
    HW = 324
    for hi, hero in enumerate(HEROES):
        x = 14 + hi * 336
        d.rectangle([x, 160, x + HW, 176], fill=RED)
        d.text((x + 8, 163), hero["bar"], font=font(SANS_B, 11),
               fill=(255, 255, 255))
        thumb = hero["thumb"]().resize((HW, 130), Image.LANCZOS)
        im.paste(thumb, (x, 176))
        for j, (txt, col) in enumerate(
                [(hero["badge"], hero["badge_color"]), (hero["tag"], NAVY)]):
            pf = font(SANS_B, 9)
            pw = d.textlength(txt, font=pf) + 12
            px = x + HW - 6 - pw
            py = 180 + j * 20
            d.rounded_rectangle([px, py, px + pw, py + 16], radius=7,
                                fill=col)
            d.text((px + 6, py + 2), txt, font=pf, fill=(255, 255, 255))
        d.text((x, 308), hero["caption"], font=font(SERIF_I, 11), fill=GREY)
        d.text((x, 322), hero["loc"], font=font(SANS_B, 10), fill=RED)
        hf, hlines = fit_lines(d, hero["head"], SERIF_B, 19, HW, 3)
        y = 336
        for ln in hlines:
            d.text((x, y), ln, font=hf, fill=INK)
            y += hf.size * 1.08
        dy = max(y + 2, 372)
        df, dlines = fit_lines(d, hero["deck"], SANS_R, 11, HW, 3)
        for ln in dlines:
            d.text((x, dy), ln, font=df, fill=INK)
            dy += 13

    # cards
    CW2 = 192
    for ci, card in enumerate(CARDS):
        row, col = divmod(ci, 5)
        y0 = 408 + row * 170
        x = 14 + col * 201
        thumb = card["thumb"]().resize((CW2, 56), Image.LANCZOS)
        im.paste(thumb, (x, y0))
        d.rectangle([x, y0 + 56, x + CW2, y0 + 71], fill=RED)
        bf = fit_single(d, card["bar"], SANS_B, 8.5, CW2 - 8)
        d.text((x + 4, y0 + 59), card["bar"], font=bf,
               fill=(255, 255, 255))
        lf = fit_single(d, card["loc"], SANS_B, 7.5, CW2)
        d.text((x, y0 + 74), card["loc"], font=lf, fill=RED)
        hf, hlines = fit_lines(d, card["head"], SERIF_B, 13, CW2, 3)
        y = y0 + 86
        for ln in hlines:
            d.text((x, y), ln, font=hf, fill=INK)
            y += 15
        max_deck = 3 if len(hlines) <= 2 else 2
        df, dlines = fit_lines(d, card["deck"], SANS_R, 9.5, CW2, max_deck)
        for ln in dlines:
            d.text((x, y), ln, font=df, fill=INK)
            y += 12
        assert y <= y0 + 164 + 1, f"card {ci} overflow y={y} y0={y0}"

    # bottom headings
    d.text((14, 748), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
    d.text((150, 750), "pins match story numbers",
           font=font(SERIF_I, 9), fill=GREY)
    d.text((340, 748), "17 MORE STORIES \u00b7 WEDNESDAY 25 NOVEMBER",
           font=font(SANS_B, 12), fill=INK)
    d.line([(14, 764), (W - 14, 764)], fill=INK, width=1)

    # dotted world map
    mx0, my0, mx1, my1 = 14, 768, 330, 920
    for gx in range(mx0, mx1 + 1, 6):
        for gy in range(my0, my1 + 1, 6):
            lon = (gx - mx0) / (mx1 - mx0) * 360 - 180
            lat = 84 - (gy - my0) / (my1 - my0) * 142
            if any(point_in_poly(lon, lat, poly)
                   for poly in CONTINENTS.values()):
                d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6],
                          fill=OLIVE)
    # pins
    for num, lon, lat, dx, dy in PINS:
        px = mx0 + (lon + 180) / 360 * (mx1 - mx0) + dx
        py = my0 + (84 - lat) / 142 * (my1 - my0) + dy
        px = max(mx0 + 9, min(mx1 - 9, px))
        py = max(my0 + 9, min(my1 - 9, py))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(SANS_B, 8)
        s = str(num)
        d.text((px - d.textlength(s, font=f) / 2, py - 5.5), s, font=f,
               fill=(255, 255, 255))

    # 17 more stories list
    for k, (num, txt) in enumerate(MORE):
        col, row = divmod(k, 9)
        x = 340 + col * 340
        y = 768 + row * 13.8
        edge = 670 if col == 0 else 1010
        size = 9
        while size > 7:
            nf = font(SANS_B, size)
            tf = font(SANS_R, size)
            wnum = d.textlength(f"{num}.", font=nf)
            if x + wnum + 4 + d.textlength(txt, font=tf) <= edge:
                break
            size -= 0.5
        nf = font(SANS_B, size)
        tf = font(SANS_R, size)
        d.text((x, y), f"{num}.", font=nf, fill=RED)
        d.text((x + d.textlength(f"{num}.", font=nf) + 4, y), txt, font=tf,
               fill=INK)

    # date check box
    d.rectangle([14, 926, 1010, 968], outline=RED, width=2)
    d.text((24, 936), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    dtxt = ("Every main story on this page happened, or was first "
            "reported, on Wednesday 25 November 2026 (UTC). Figures are "
            "as reported by the wires at press time; developing stories "
            "may since have moved on.")
    tf = font(SANS_R, 10.5)
    y = 930
    for ln in wrap(d, dtxt, tf, W - 14 - 150):
        d.text((150, y), ln, font=tf, fill=INK)
        y += 13

    # sources line
    d.text((14, 972), "Sources: Reuters, AP, AFP.", font=font(SANS_R, 9),
           fill=GREY)
    f = font(SANS_R, 9)
    t = "Scenes are drawn illustrations \u00b7 wires read to 04:00 UTC"
    d.text((W - 14 - d.textlength(t, font=f), 972), t, font=f, fill=GREY)

    # footer bar
    d.rectangle([0, 992, W, H], fill=NAVY)
    d.text((14, 1002), "THE WORLD IN ONE DAY", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    f = font(SANS_B, 9)
    t = "WEDNESDAY 25 NOVEMBER 2026 \u00b7 ONE PAGE"
    d.text((W - 14 - d.textlength(t, font=f), 1004), t, font=f,
           fill=(255, 255, 255))

    return im


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img = build()
    img.save(out, optimize=True, compress_level=9)
    data = open(out, "rb").read()
    print(out, img.size, len(data), "bytes",
          hashlib.sha256(data).hexdigest())
