#!/usr/bin/env python3
"""Render the news-image-20261126 newspaper: Thursday 26 November 2026, 33 stories.
1024x1024 PNG, Pillow. All pictures are drawings, not photos."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 86, 78)
MAGENTA = (196, 18, 110)
DARK = (24, 28, 44)
RULE = (26, 26, 26)

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, fill, max_w, lh, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def text_w(draw, text, font):
    return draw.textlength(text, font=font)

# ---------------------------------------------------------------- data
LEADS = [
    dict(num=1, badge="REPORTED", bc=(178, 34, 34),
         head="Two Italians killed in drone attack on Kuwait; Iran blamed, Iran denies",
         body="Two Italian technicians at a Rheinmetall air-defence station were killed; four hurt. Kuwait blamed Iran; Iran denied it. Meloni voiced deep sorrow.",
         scene="kuwait"),
    dict(num=2, badge="REPORTED / ONGOING", bc=(178, 34, 34),
         head="Israeli strikes kill nine in Gaza, including Hamas deputy education minister",
         body="Airstrikes killed at least nine, including deputy minister Khaled Abu Nada. Katz threatened to displace another one million Palestinians.",
         scene="gaza"),
    dict(num=3, badge="REPORTED", bc=(178, 34, 34),
         head="Houthis hit Ras Tanura refinery; Iran mines in the Strait of Hormuz; oil climbs",
         body="Saudi Arabia stopped a Houthi drone attack on Ras Tanura refinery. Iran said an LNG carrier hit a mine in Hormuz. Brent rose 0.63% to $91.21.",
         scene="hormuz"),
]

MIDS = [
    dict(num=4, head="ECB picks Spain's Hernandez de Cos to succeed Lagarde",
         body="Eurozone leaders chose the BIS chief; inflation runs near double the 2% target.", scene="ecb"),
    dict(num=5, head="Russia hits Kyiv with ballistic missiles; Ukraine hits back",
         body="At least three killed in Kyiv; defences downed 87 missiles and drones.", scene="kyiv"),
    dict(num=6, head="Iran faces US blockade as oil revenue falls",
         body="Crude exports could hit zero by mid-December under a US naval blockade.", scene="oil"),
    dict(num=7, head="EU leaders clash over \u20ac2 trillion long-term budget",
         body="The 2028\u20132034 budget could reach \u20ac2 trillion; three states want out of a \u20ac45bn loan.", scene="eu"),
    dict(num=8, head="DR Congo Ebola cases pass 12,000",
         body="The second-largest outbreak on record; fighting forced responders to evacuate.", scene="ebola"),
    dict(num=9, head="Cheaper HIV prevention jab reaches Africa",
         body="Lenacapavir, a twice-yearly jab nearly 100% effective, reaches millions at lower cost.", scene="jab"),
    dict(num=10, head="Nvidia halts AI server shipments to Southeast Asia",
         body="Huang returned as CEO amid US scrutiny; S&P put Nvidia's rating on downgrade watch.", scene="chip"),
    dict(num=11, head="FCC approves SpaceX plan for one million satellites",
         body="One million satellites for orbital data centres (\u201cStarmind\u201d). Amazon opposed it.", scene="sat"),
    dict(num=12, head="Diesel tanker capsizes off Ibiza, one crew member dies",
         body="The Med Emre carried up to 7,000 tonnes of diesel; 16\u201317 crew saved.", scene="tanker"),
    dict(num=13, head="UK net migration falls to 77,000, lowest since 1997",
         body="Lowest since 1997 outside Covid years. Indians remain the largest group.", scene="mig"),
    dict(num=14, head="Storms disrupt US Thanksgiving travel; 100th Macy's parade postponed",
         body="Over 80 million travelling; about 300,000 lost power; parade moves to Saturday.", scene="storm"),
    dict(num=15, head="Leaked data: Russia lost nearly 500,000 troops",
         body="A BBC analysis of leaked data puts the dead at at least 490,334.", scene="troops"),
    dict(num=16, head="King tides and storms flood California coast",
         body="Part of the Pacifica Municipal Pier was destroyed; LA and La Jolla saw record tides.", scene="waves"),
]

ALSO = [
    "Bangkok oil refinery blast injures nine, three critically.",
    "Indonesia gold mine flood kills 13, 13 missing (reported Thu).",
    "Sudan drone attacks kill 15+ in Blue Nile; WFP warns of food shortage.",
    "Iraq asserts control over Kurdistan oil; thousands protest in Duhok.",
    "Norse Atlantic suspends all flights, to file for bankruptcy.",
    "Bangladesh garment workers protest minimum wage; 140 factories shut.",
    "Memory-chip shortage triples some RAM prices ahead of Black Friday.",
    "New York bans AI chatbots from posing as human with children.",
    "Sinner out of Australian Open after knee surgery; out four months.",
    "Champions League: Liverpool 3\u20130 Club Brugge; Lille end Bayern's run 2\u20131.",
    "CAS restores Senegal's Africa Cup title; Morocco vows to fight on.",
    "Miss Universe: Puerto Rico's Jennifer Barreto wins in San Juan.",
    "Euclid telescope finds its first comet.",
    "Pig kidney patient marks one year off dialysis.",
    "China\u2013Cambodia Golden Dragon 2026 drills begin; 3,000 personnel.",
    "Nigeria seizes $220 million of methamphetamine; five arrested.",
    "UK sends convicted refugee to Eswatini under secret deal.",
]

NUMBERS = [
    ("2", "Italians killed\nin Kuwait"),
    ("9", "killed in Gaza\non Thursday"),
    ("12,000+", "confirmed Ebola\ncases, DR Congo"),
    ("490,334", "Russian soldiers\ndead in Ukraine"),
    ("77,000", "UK net migration,\nlowest since 1997"),
    ("1,000,000", "satellites in\nSpaceX plan"),
    ("\u20ac2tn", "EU long-term\nbudget in talks"),
    ("7,000t", "diesel aboard\nthe Ibiza tanker"),
    ("80M+", "Americans travelling\nfor Thanksgiving"),
    ("$91.21", "Brent crude\n+0.63%"),
]

MARKETS = [
    ("EURO STOXX", "+2.04%", True), ("SENSEX", "+2.3%", True),
    ("SHANGHAI", "\u22122.01%", False), ("S&P 500*", "\u22120.25%", False),
    ("EURO", "$1.0973", None), ("BRENT", "$91.21", True),
]

REGIONS = [
    ("NORTH AMERICA", 8, (52, 110, 190)), ("EUROPE", 10, (34, 139, 92)),
    ("MIDDLE EAST", 5, (214, 110, 30)), ("AFRICA", 5, (124, 58, 150)),
    ("ASIA-PACIFIC", 5, (16, 130, 130)),
]

TIMELINE = [
    ("OVERNIGHT", "Russia hits Kyiv; Israeli strikes kill nine in Gaza"),
    ("EARLY", "Diesel tanker Med Emre capsizes off Ibiza"),
    ("MORNING", "EU leaders open summit on \u20ac2tn budget, Brussels"),
    ("~10:15 UTC", "SpaceX satellite approval; Babcock $11.4bn subs deal"),
    ("~18:15 UTC", "Nvidia pauses SE Asia shipments; Kuwait drone deaths"),
    ("EVENING", "Champions League: Liverpool 3\u20130; Lille 2\u20131 Bayern"),
]

DATECHECK = [
    "US tariffs on 14 partners (Wed 25 Nov)", "US Q3 GDP revised to 4.3% (Wed 25 Nov)",
    "Andy Taylor of Duran Duran dies, 65 (announced Wed 25 Nov)",
    "Solomon Islands\u2013Australia security treaty (Wed 25 Nov)",
    "Netanyahu trial: drop bribery charge suggested (Wed 25 Nov)",
    "Cairo fuel tanker fire kills 31 (Wed 25 Nov)",
    "UK energy bills +26% in January (Wed 25 Nov)",
    "Poundland collapses into administration (Wed 25 Nov)",
]

SOURCES = ("Reuters \u00b7 BBC News \u00b7 Al Jazeera \u00b7 AP \u00b7 AFP \u00b7 Euronews \u00b7 CNBC \u00b7 The Guardian \u00b7 "
           "Dow Jones \u00b7 NPR \u00b7 CBC News \u00b7 France 24 \u00b7 Sky News \u00b7 The Hindu \u00b7 SCMP \u00b7 Le Monde \u00b7 "
           "Folha de S.Paulo \u00b7 Japan Times \u00b7 ScienceDaily \u00b7 Phys.org \u00b7 oneturn.news \u00b7 Open Chronicle. "
           "Drawings, not photos.")

# ------------------------------------------------------- scene drawings
def sky_grad(d, box, top, bot):
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        c = tuple(int(top[j] + (bot[j] - top[j]) * t) for j in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)

def person(d, x, y, s, col, hat=False):
    d.ellipse([x - 3 * s, y - 8 * s, x + 3 * s, y - 2 * s], fill=col)
    d.rectangle([x - 3.5 * s, y - 2 * s, x + 3.5 * s, y + 6 * s], fill=col)
    d.rectangle([x - 3 * s, y + 6 * s, x - 1 * s, y + 12 * s], fill=col)
    d.rectangle([x + 1 * s, y + 6 * s, x + 3 * s, y + 12 * s], fill=col)
    if hat:
        d.rectangle([x - 4 * s, y - 8.5 * s, x + 4 * s, y - 6.5 * s], fill=(250, 200, 40))

def scene_kuwait(d, box):
    x0, y0, x1, y1 = box
    sky_grad(d, box, (58, 44, 86), (214, 122, 64))
    d.ellipse([x1 - 52, y0 + 8, x1 - 22, y0 + 38], fill=(250, 214, 140))
    for cx in (x0 + 34, x0 + 78):
        d.line([(cx, y1 - 34), (cx, y1 - 62)], fill=(30, 30, 34), width=3)
        d.pieslice([cx - 22, y1 - 88, cx + 22, y1 - 52], 180, 360, fill=(232, 232, 228), outline=(30, 30, 34))
        d.line([(cx, y1 - 70), (cx + 16, y1 - 84)], fill=(30, 30, 34), width=2)
    d.line([(x1 - 46, y1 - 30), (x1 - 46, y1 - 78)], fill=(30, 30, 34), width=3)
    d.line([(x1 - 58, y1 - 66), (x1 - 34, y1 - 66)], fill=(30, 30, 34), width=2)
    for cx, cy, r in ((x0 + 130, y0 + 22, 12), (x0 + 152, y0 + 14, 15), (x0 + 176, y0 + 24, 10)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 112))
    dx, dy = x0 + 150, y0 + 52
    d.ellipse([dx - 8, dy - 3, dx + 8, dy + 3], fill=(20, 20, 24))
    d.line([(dx - 16, dy - 4), (dx + 16, dy - 4)], fill=(20, 20, 24), width=2)
    d.rectangle([x0, y1 - 30, x1, y1], fill=(52, 44, 40))
    person(d, x0 + 120, y1 - 30, 1.1, (24, 24, 28), hat=True)
    person(d, x0 + 148, y1 - 30, 1.1, (24, 24, 28), hat=True)

def scene_gaza(d, box):
    x0, y0, x1, y1 = box
    sky_grad(d, box, (10, 14, 34), (44, 52, 96))
    for sx, sy in ((x0 + 20, y0 + 12), (x0 + 90, y0 + 20), (x0 + 170, y0 + 10), (x0 + 220, y0 + 24)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(240, 240, 220))
    for bx, bw, bh in ((x0 + 8, 34, 52), (x0 + 48, 26, 70), (x0 + 80, 40, 44), (x0 + 190, 30, 60), (x0 + 224, 26, 48)):
        d.rectangle([bx, y1 - 34 - bh, bx + bw, y1 - 34], fill=(18, 20, 34))
        for wy in range(y1 - 34 - bh + 8, y1 - 40, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 210, 90))
    fx, fy = x0 + 150, y0 + 34
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([(fx, fy), (fx + 26 * math.cos(a), fy + 26 * math.sin(a))], fill=(255, 196, 60), width=3)
    d.ellipse([fx - 10, fy - 10, fx + 10, fy + 10], fill=(255, 226, 120))
    d.rectangle([x0, y1 - 34, x1, y1], fill=(38, 34, 44))
    for i, px in enumerate((x0 + 30, x0 + 62, x0 + 96, x0 + 200, x0 + 232)):
        person(d, px, y1 - 30, 0.9, (16, 16, 20))
        d.ellipse([px + 6, y1 - 40, px + 12, y1 - 34], fill=(150, 120, 80))
    d.rectangle([x0 + 126, y1 - 30, x0 + 178, y1 - 16], fill=(232, 228, 218), outline=(20, 20, 24))
    d.text((x0 + 130, y1 - 29), "MINISTRY", font=F(SANS_B, 7), fill=(20, 20, 24))

def scene_hormuz(d, box):
    x0, y0, x1, y1 = box
    sky_grad(d, box, (244, 190, 120), (168, 200, 224))
    d.ellipse([x1 - 56, y0 + 6, x1 - 24, y0 + 38], fill=(255, 226, 150))
    d.rectangle([x0, y0 + 62, x1, y1], fill=(34, 92, 140))
    for wy in (y0 + 74, y0 + 88, y0 + 100):
        for wx in range(x0 + 6, x1 - 10, 26):
            d.arc([wx, wy, wx + 18, wy + 8], 200, 340, fill=(190, 220, 240), width=2)
    for tx, tw in ((x0 + 14, 74), (x0 + 130, 88)):
        d.rectangle([tx, y0 + 66, tx + tw, y0 + 82], fill=(22, 26, 34))
        d.rectangle([tx + tw - 18, y0 + 52, tx + tw - 8, y0 + 66], fill=(150, 40, 30))
        d.rectangle([tx + 8, y0 + 56, tx + 30, y0 + 66], fill=(232, 232, 228))
    mx, my = x0 + 112, y0 + 92
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 20, 24))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(mx + 7 * math.cos(a), my + 7 * math.sin(a)), (mx + 12 * math.cos(a), my + 12 * math.sin(a))], fill=(20, 20, 24), width=2)
    d.rectangle([x1 - 34, y0 + 40, x1 - 28, y0 + 62], fill=(30, 30, 34))
    d.ellipse([x1 - 38, y0 + 28, x1 - 24, y0 + 42], fill=(255, 150, 40))

def mini(d, box, kind):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    bg = {"ecb": (232, 226, 205), "kyiv": (226, 220, 214), "oil": (226, 214, 196),
          "eu": (214, 222, 244), "ebola": (244, 214, 214), "jab": (214, 232, 226),
          "chip": (220, 226, 240), "sat": (216, 220, 240), "tanker": (214, 228, 238),
          "mig": (232, 226, 214), "storm": (222, 224, 232), "troops": (228, 224, 214),
          "waves": (212, 230, 240)}[kind]
    d.rectangle(box, fill=bg, outline=(120, 116, 108))
    if kind == "ecb":
        d.rectangle([cx - 20, cy + 8, cx + 20, cy + 12], fill=(60, 60, 66))
        for px in (-16, -5, 6, 17):
            d.rectangle([cx + px - 2, cy - 8, cx + px + 2, cy + 8], fill=(60, 60, 66))
        d.polygon([(cx - 24, cy - 8), (cx + 24, cy - 8), (cx, cy - 20)], fill=(60, 60, 66))
        d.text((cx + 8, cy - 6), "\u20ac", font=F(SANS_B, 12), fill=(24, 90, 60))
    elif kind == "kyiv":
        d.polygon([(cx - 4, cy + 14), (cx + 2, cy + 14), (cx + 8, cy - 16), (cx + 2, cy - 16)], fill=(40, 40, 46))
        d.ellipse([cx + 2, cy - 22, cx + 14, cy - 10], fill=(255, 170, 40))
        d.line([(cx - 22, cy + 16), (cx - 10, cy + 16)], fill=(120, 120, 120), width=2)
        d.line([(cx + 12, cy + 16), (cx + 22, cy + 16)], fill=(120, 120, 120), width=2)
    elif kind == "oil":
        d.rectangle([cx - 12, cy - 14, cx + 12, cy + 16], fill=(40, 40, 46))
        d.rectangle([cx - 12, cy - 4, cx + 12, cy - 1], fill=(90, 90, 96))
        d.rectangle([cx - 12, cy + 6, cx + 12, cy + 9], fill=(90, 90, 96))
        d.line([(cx + 20, cy - 14), (cx + 20, cy + 8)], fill=(178, 34, 34), width=3)
        d.polygon([(cx + 14, cy + 8), (cx + 26, cy + 8), (cx + 20, cy + 16)], fill=(178, 34, 34))
    elif kind == "eu":
        for i in range(12):
            a = math.radians(i * 30 - 90)
            sx, sy = cx + 14 * math.cos(a), cy + 14 * math.sin(a)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 210, 60))
        d.text((cx - 6, cy - 9), "\u20ac", font=F(SANS_B, 16), fill=(30, 44, 84))
    elif kind == "ebola":
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(178, 34, 34))
        for i in range(8):
            a = math.radians(i * 45)
            d.line([(cx + 10 * math.cos(a), cy + 10 * math.sin(a)), (cx + 16 * math.cos(a), cy + 16 * math.sin(a))], fill=(178, 34, 34), width=3)
        d.ellipse([cx - 3, cy - 4, cx + 1, cy + 0], fill=(255, 255, 255))
    elif kind == "jab":
        d.line([(cx - 16, cy + 14), (cx + 8, cy - 10)], fill=(60, 60, 66), width=4)
        d.rectangle([cx - 2, cy - 18, cx + 12, cy - 6], fill=(90, 160, 200), outline=(40, 40, 46))
        d.line([(cx + 8, cy - 10), (cx + 18, cy - 20)], fill=(60, 60, 66), width=2)
    elif kind == "chip":
        d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(30, 44, 84), outline=(20, 20, 26))
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=(250, 210, 60))
        for i in range(-1, 2):
            d.line([(cx + i * 8, cy - 18), (cx + i * 8, cy - 12)], fill=(60, 60, 66), width=2)
            d.line([(cx + i * 8, cy + 12), (cx + i * 8, cy + 18)], fill=(60, 60, 66), width=2)
            d.line([(cx - 18, cy + i * 8), (cx - 12, cy + i * 8)], fill=(60, 60, 66), width=2)
            d.line([(cx + 12, cy + i * 8), (cx + 18, cy + i * 8)], fill=(60, 60, 66), width=2)
    elif kind == "sat":
        d.rectangle([cx - 8, cy - 5, cx + 8, cy + 5], fill=(40, 40, 46))
        d.rectangle([cx - 22, cy - 3, cx - 9, cy + 3], fill=(52, 110, 190))
        d.rectangle([cx + 9, cy - 3, cx + 22, cy + 3], fill=(52, 110, 190))
        d.ellipse([cx - 2, cy - 12, cx + 2, cy - 8], fill=(250, 210, 60))
        d.ellipse([cx - 20, cy + 12, cx - 17, cy + 15], fill=(250, 210, 60))
    elif kind == "tanker":
        d.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 14, cy + 14), (cx - 14, cy + 14)], fill=(22, 26, 34))
        d.rectangle([cx + 6, cy - 8, cx + 14, cy + 2], fill=(150, 40, 30))
        for wx in range(cx - 22, cx + 22, 10):
            d.arc([wx, cy + 14, wx + 8, cy + 20], 200, 340, fill=(52, 110, 190), width=2)
    elif kind == "mig":
        d.line([(cx - 18, cy - 8), (cx + 10, cy - 8)], fill=(34, 139, 92), width=3)
        d.polygon([(cx + 10, cy - 8), (cx + 2, cy - 13), (cx + 2, cy - 3)], fill=(34, 139, 92))
        d.line([(cx + 18, cy + 8), (cx - 10, cy + 8)], fill=(178, 34, 34), width=3)
        d.polygon([(cx - 10, cy + 8), (cx - 2, cy + 3), (cx - 2, cy + 13)], fill=(178, 34, 34))
    elif kind == "storm":
        d.ellipse([cx - 18, cy - 8, cx - 2, cy + 6], fill=(90, 96, 110))
        d.ellipse([cx - 6, cy - 14, cx + 12, cy + 4], fill=(70, 76, 92))
        d.ellipse([cx + 6, cy - 6, cx + 20, cy + 6], fill=(90, 96, 110))
        for rx in (-12, -2, 8):
            d.line([(cx + rx, cy + 10), (cx + rx - 3, cy + 18)], fill=(52, 110, 190), width=2)
    elif kind == "troops":
        d.ellipse([cx - 2, cy - 14, cx + 12, cy - 2], fill=(60, 64, 52))
        d.rectangle([cx - 2, cy - 6, cx + 12, cy - 2], fill=(60, 64, 52))
        d.rectangle([cx - 8, cy + 0, cx + 18, cy + 16], fill=(80, 84, 66))
        d.text((cx - 8, cy + 18), "490k", font=F(SANS_B, 8), fill=(60, 60, 60))
    elif kind == "waves":
        for wy, ww in ((cy - 10, 30), (cy + 0, 36), (cy + 10, 30)):
            d.arc([cx - ww // 2, wy, cx + ww // 2, wy + 12], 180, 360, fill=(34, 92, 140), width=3)
        d.line([(cx - 20, cy - 16), (cx + 20, cy - 16)], fill=(120, 90, 60), width=3)
        d.line([(cx - 14, cy - 16), (cx - 14, cy - 10)], fill=(120, 90, 60), width=2)
        d.line([(cx + 8, cy - 16), (cx + 8, cy - 10)], fill=(120, 90, 60), width=2)

# dotted world map: blob-rasterised land on a wide strip grid (230 x 15)
MAP_COLS, MAP_ROWS = 230, 15
BLOBS = [  # (cx, cy, rx, ry) in grid coords
    (30, 3, 24, 3), (62, 1.5, 6, 1.5), (50, 6, 8, 1.5), (62, 10, 11, 4),
    (112, 2.5, 8, 2), (120, 8, 11, 4.5), (132, 4, 12, 2.5), (165, 2.5, 32, 2.5),
    (170, 6, 18, 2.5), (182, 9, 11, 1.5), (196, 11, 11, 2.5), (206, 4, 3, 2),
]
PIN_POS = {  # (col, row) in grid coords -> story number
    (136, 5): "1", (130, 5): "2", (142, 6): "3", (116, 2): "5",
    (122, 9): "8", (110, 2): "7", (34, 4): "14",
}

def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 240, 244), outline=(150, 148, 140))
    d.text((x0 + 6, y0 + 3), "THE WORLD, DOTTED — PINS MARK STORIES 1, 2, 3, 5, 7, 8, 14",
           font=F(SANS_B, 8), fill=MUTED)
    gy0 = y0 + 14
    cw, ch = (x1 - x0) / MAP_COLS, (y1 - gy0) / MAP_ROWS
    for r in range(MAP_ROWS):
        for c in range(MAP_COLS):
            inside = False
            for bx, by, rx, ry in BLOBS:
                if ((c + 0.5 - bx) / rx) ** 2 + ((r + 0.5 - by) / ry) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([x0 + c * cw + 0.6, gy0 + r * ch + 0.6,
                           x0 + (c + 1) * cw - 0.6, gy0 + (r + 1) * ch - 0.6],
                          fill=(120, 128, 150))
    for (c, r), n in PIN_POS.items():
        px, py = x0 + (c + 0.5) * cw, gy0 + (r + 0.5) * ch
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=MAGENTA, outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), n, font=F(SANS_B, 8), fill=(255, 255, 255))

# ---------------------------------------------------------------- build
def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    MX = 14

    # masthead
    d.text((MX, 10), "Thursday 26 November 2026", font=F(SERIF_B, 44), fill=INK)
    d.text((MX, 62), "THE WORLD IN ONE PAGE", font=F(SANS_B, 11), fill=MUTED)
    tag = "33 STORIES"
    tw = text_w(d, tag, F(SANS_B, 15))
    d.rectangle([W - MX - tw - 20, 14, W - MX, 44], fill=DARK)
    d.text((W - MX - tw - 10, 20), tag, font=F(SANS_B, 15), fill=(255, 255, 255))
    d.text((W - MX - 118, 58), "ALL DRAWINGS,", font=F(SANS_B, 10), fill=MUTED)
    d.text((W - MX - 118, 70), "NOT PHOTOS", font=F(SANS_B, 10), fill=MUTED)
    d.rectangle([MX, 92, W - MX, 96], fill=RULE)
    d.rectangle([MX, 98, W - MX, 99], fill=RULE)

    # title line
    d.text((MX, 104), "33 Stories: Kuwait Drone Deaths, Gaza Strikes, Gulf Oil Threat",
           font=F(SERIF_B, 19), fill=INK)

    # markets strip
    y = 132
    d.text((MX, y + 2), "MARKETS", font=F(SANS_B, 10), fill=MUTED)
    mx = MX + 78
    for name, val, up in MARKETS:
        col = (34, 139, 92) if up is True else ((178, 34, 34) if up is False else INK)
        d.text((mx, y + 2), name, font=F(SANS_B, 10), fill=MUTED)
        mx += text_w(d, name, F(SANS_B, 10)) + 5
        d.text((mx, y), val, font=F(SANS_B, 13), fill=col)
        mx += text_w(d, val, F(SANS_B, 13)) + 16
    d.line([(MX, 156), (W - MX, 156)], fill=(180, 176, 168), width=1)

    # region strip
    y = 162
    d.text((MX, y + 2), "REGIONS", font=F(SANS_B, 10), fill=MUTED)
    rx, total = MX + 78, 33
    bar_w = W - MX - rx
    for name, n, col in REGIONS:
        w = bar_w * n / total
        d.rectangle([rx, y, rx + w - 2, y + 16], fill=col)
        d.text((rx + 3, y + 3), f"{name} {n}", font=F(SANS_B, 9), fill=(255, 255, 255))
        rx += w
    d.line([(MX, 186), (W - MX, 186)], fill=(180, 176, 168), width=1)

    # timeline strip
    y = 192
    d.text((MX, y + 2), "THURSDAY, UTC", font=F(SANS_B, 10), fill=MUTED)
    tx = MX + 108
    seg = (W - MX - tx) / len(TIMELINE)
    d.line([(tx, y + 8), (W - MX, y + 8)], fill=(150, 146, 138), width=2)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = tx + seg * i + 4
        d.ellipse([cx - 4, y + 4, cx + 4, y + 12], fill=MAGENTA, outline=(255, 255, 255), width=1)
        d.text((cx + 7, y - 1), t, font=F(SANS_B, 8), fill=MAGENTA)
        para(d, cx + 7, y + 9, txt, F(SANS, 8), INK, seg - 12, 9, max_lines=2)
    d.line([(MX, 216), (W - MX, 216)], fill=(180, 176, 168), width=1)

    # ---- main area: content + dark sidebar
    CX0, CX1 = MX, 812
    SX0, SX1 = 826, W - MX
    col_w = (CX1 - CX0 - 24) // 3
    lead_y, lead_h = 224, 200
    for i, L in enumerate(LEADS):
        x = CX0 + i * (col_w + 12)
        d.rectangle([x, lead_y, x + col_w, lead_y + lead_h], outline=(150, 146, 138), width=1)
        scene = {"kuwait": scene_kuwait, "gaza": scene_gaza, "hormuz": scene_hormuz}[L["scene"]]
        scene(d, (x + 1, lead_y + 1, x + col_w - 1, lead_y + 90))
        bw = text_w(d, L["badge"], F(SANS_B, 9)) + 10
        d.rectangle([x + 6, lead_y + 96, x + 6 + bw, lead_y + 110], fill=L["bc"])
        d.text((x + 11, lead_y + 98), L["badge"], font=F(SANS_B, 9), fill=(255, 255, 255))
        d.text((x + 6 + bw + 6, lead_y + 98), f"STORY {L['num']}", font=F(SANS_B, 9), fill=MUTED)
        ty = lead_y + 114
        ty = para(d, x + 6, ty, L["head"], F(SERIF_B, 14), INK, col_w - 12, 16, max_lines=3)
        para(d, x + 6, ty + 2, L["body"], F(SANS, 9), (60, 58, 52), col_w - 12, 11, max_lines=3)

    # dotted world map strip
    map_y, map_h = 432, 66
    draw_map(d, (CX0, map_y, CX1, map_y + map_h))

    # mid grid: 3 cols x 5 rows
    grid_y, cell_h = 506, 64
    for i, M in enumerate(MIDS):
        r, c = divmod(i, 3)
        x = CX0 + c * (col_w + 12)
        y = grid_y + r * cell_h
        d.rectangle([x, y, x + col_w, y + cell_h - 6], outline=(190, 186, 178), width=1)
        mini(d, (x + 5, y + 6, x + 63, y + cell_h - 12), M["scene"])
        tx0 = x + 68
        d.text((tx0, y + 4), f"{M['num']}.", font=F(SANS_B, 10), fill=MAGENTA)
        para(d, tx0 + 20, y + 4, M["head"], F(SANS_B, 10), INK, col_w - 92, 12, max_lines=2)
        para(d, tx0, y + 30, M["body"], F(SANS, 9), (60, 58, 52), col_w - 74, 11, max_lines=2)

    # dark sidebar: BY THE NUMBERS
    grid_bot = grid_y + 5 * cell_h - 6
    d.rectangle([SX0, lead_y, SX1, grid_bot], fill=DARK)
    d.text((SX0 + 10, lead_y + 8), "BY THE", font=F(SERIF_B, 20), fill=(255, 255, 255))
    d.text((SX0 + 10, lead_y + 30), "NUMBERS", font=F(SERIF_B, 20), fill=(255, 255, 255))
    d.rectangle([SX0 + 10, lead_y + 56, SX1 - 10, lead_y + 58], fill=MAGENTA)
    ny = lead_y + 66
    for big, lab in NUMBERS:
        d.text((SX0 + 10, ny), big, font=F(SERIF_B, 19), fill=(255, 210, 60))
        for j, ln in enumerate(lab.split("\n")):
            d.text((SX0 + 10, ny + 24 + j * 11), ln, font=F(SANS, 9), fill=(210, 210, 220))
        ny += 50
    d.text((SX0 + 10, ny + 2), "*S&P 500: Wed close /\nfutures — US markets closed.",
           font=F(SANS, 8), fill=(170, 170, 180))

    # ---- bottom: ALSO ON THURSDAY (2 cols)
    by = grid_bot + 4
    d.text((MX, by), "ALSO ON THURSDAY", font=F(SERIF_B, 15), fill=INK)
    d.rectangle([MX + 168, by + 8, W - MX, by + 10], fill=RULE)
    iy = by + 22
    col2_x = MX + 500
    for i, item in enumerate(ALSO):
        x = MX if i < 9 else col2_x
        y = iy + (i if i < 9 else i - 9) * 12
        d.text((x, y), f"{i + 1}.", font=F(SANS_B, 9), fill=MAGENTA)
        d.text((x + 20, y), item, font=F(SANS, 9), fill=INK)
    fy = iy + 9 * 12 + 4
    d.text((MX, fy), "DATE CHECK — first reported on another day, so not counted as Thursday's news:",
           font=F(SANS_B, 9), fill=(120, 30, 30))
    dc = "  \u00b7  ".join(DATECHECK)
    fy = para(d, MX, fy + 13, dc, F(SANS, 8), MUTED, W - 2 * MX, 10, max_lines=2)
    para(d, MX, fy + 4, SOURCES, F(SANS, 8), MUTED, W - 2 * MX, 10, max_lines=2)

    im.save("/home/hatch/workspace/makefun/news-image-20261126-entry/entry.png", optimize=True)
    print("saved entry.png", im.size)

if __name__ == "__main__":
    main()
