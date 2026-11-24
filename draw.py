#!/usr/bin/env python3
"""news-23 b182 heroes-scene: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
M = 24
CW = W - 2 * M  # 976

PAPER = (247, 243, 234)
INK = (17, 17, 17)
MUT = (90, 86, 78)
RED = (185, 28, 28)
REDBG = (252, 231, 231)
GOLD = (180, 130, 20)
BLUE = (29, 78, 216)
TEAL = (13, 148, 136)
GREEN = (21, 128, 61)
ORANGE = (234, 88, 12)
DARK = (24, 24, 24)
LINE = (200, 192, 178)

FD = "/usr/share/fonts/truetype/dejavu/"

def f(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if (serif and bold) else \
           "DejaVuSerif.ttf" if serif else \
           "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FD + name, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w, max_lines=None):
    """Word-wrap to lines that fit max_w (measured)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines:
        lines = lines[:max_lines]
    return lines

def fit1(text, font, max_w):
    """Single line, truncate with ellipsis to fit."""
    if d.textlength(text, font=font) <= max_w:
        return text
    while text and d.textlength(text + "\u2026", font=font) > max_w:
        text = text[:-1]
    return text + "\u2026"

def center(x0, x1, y, text, font, fill=INK):
    d.text(((x0 + x1 - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)

def chip(x, y, text, fill=GREEN):
    """Small REPORTED/CLAIM chip; returns width."""
    font = f(10, bold=True)
    tw = d.textlength(text, font=font)
    w, h = tw + 12, 16
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    d.text((x + 6, y + 2), text, font=font, fill=(255, 255, 255))
    return w

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 58], fill=DARK)
d.text((M, 8), "THE WORLD TODAY", font=f(38, bold=True, serif=True), fill=(255, 255, 255))
d.text((W - M - d.textlength("MONDAY 23 NOVEMBER 2026", font=f(15, bold=True)), 20),
       "MONDAY 23 NOVEMBER 2026", font=f(15, bold=True), fill=(255, 210, 90))
d.line([0, 58, W, 58], fill=GOLD, width=3)

# ---------------------------------------------------------------- kicker
center(M, W - M, 66, "ONE DAY  \u00b7  31 STORIES  \u00b7  FIVE CONTINENTS  \u00b7  EVERY NUMBER CHECKED",
       f(12, bold=True), fill=MUT)

# ---------------------------------------------------------------- number strip
NUMS = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES DRC"),
        ("10T WON", "SEOUL FUND"), ("2%", "BILLIONAIRE TAX"), ("$450M", "SKUBAL METS"),
        ("165", "MISSILES / WEEK"), ("12,000", "MANCHESTER"), ("264 KG", "LEBANON"),
        ("$107.3B", "ANTHROPIC IPO")]
d.rectangle([M, 86, W - M, 146], outline=LINE, width=1)
cw = CW / 5
for i, (num, lab) in enumerate(NUMS):
    r, c = divmod(i, 5)
    x0 = M + c * cw
    y0 = 86 + r * 30
    if c:
        d.line([x0, 90, x0, 142], fill=LINE, width=1)
    center(x0, x0 + cw, y0 + 1, num, f(17, bold=True), fill=RED if i == 0 else INK)
    center(x0, x0 + cw, y0 + 19, lab, f(9, bold=True), fill=MUT)
d.line([M, 116, W - M, 116], fill=LINE, width=1)

# ---------------------------------------------------------------- region bar
d.rectangle([M, 150, W - M, 172], fill=(232, 226, 212))
center(M, W - M, 156,
       "ASIA-PACIFIC 7   \u00b7   AMERICAS 8   \u00b7   MIDDLE EAST 6   \u00b7   EUROPE 5   \u00b7   AFRICA 3   \u00b7   WORLD 2",
       f(12, bold=True))

# ---------------------------------------------------------------- hero scenes
HX = [M, M + 328, M + 656]   # column x
HW = 320
HY0, HY1 = 178, 466
for x in HX:
    d.rectangle([x, HY0, x + HW, HY1], outline=LINE, width=1)

def hero_head(x, n, title, body, src, chip_text, chip_fill):
    """Headline + body + source line under a scene drawn in [x,178,x+320,316]."""
    lines = wrap(title, f(17, bold=True), HW - 16, 2)
    y = 322
    for ln in lines:
        d.text((x + 8, y), ln, font=f(17, bold=True), fill=INK)
        y += 21
    blines = wrap(body, f(11), HW - 16, 2)
    y = 368
    for ln in blines:
        d.text((x + 8, y), ln, font=f(11), fill=MUT)
        y += 14
    d.text((x + 8, 440), src, font=f(10, bold=True), fill=MUT)
    chip(x + HW - 8 - (d.textlength(chip_text, font=f(10, bold=True)) + 12), 438, chip_text, chip_fill)

# --- scene 1: Kospi skyline + falling chart
x = HX[0]
d.rectangle([x, HY0, x + HW, 316], fill=(16, 24, 40))
# skyline
import random
random.seed(23)
bx = x + 6
while bx < x + HW - 14:
    bw = random.randint(26, 44)
    bh = random.randint(38, 96)
    by = 316 - bh
    d.rectangle([bx, by, bx + bw, 316], fill=(38, 52, 74))
    for wy in range(by + 8, 310, 12):
        for wx in range(bx + 5, bx + bw - 4, 10):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    bx += bw + 4
# orange falling chart, lower right, clear of the big number and sub-line
pts = [(x + 220, 240), (x + 258, 254), (x + 288, 268), (x + 308, 280)]
d.line(pts, fill=ORANGE, width=4, joint="curve")
d.text((x + 14, 184), "-3.3%", font=f(30, bold=True), fill=(255, 255, 255))
d.text((x + 14, 222), "KOSPI  4,708.54  \u00b7  -161 PTS", font=f(11, bold=True), fill=(255, 210, 90))
d.rectangle([x, 288, x + HW, 316], fill=(16, 24, 40))
d.text((x + 14, 294), "SAMSUNG -3.1%   SK HYNIX -2.5%", font=f(11, bold=True), fill=(255, 255, 255))
hero_head(x, 1, "AI ROUT HITS ASIA",
          "Chip stocks lead a broad sell-off; Seoul readies a 10T-won stabilisation fund.",
          "SEOUL \u00b7 WIRES", "REPORTED", GREEN)

# --- scene 2: Guterres globe (right) + headline text (left, clear of globe)
x = HX[1]
d.rectangle([x, HY0, x + HW, 316], fill=(12, 42, 60))
cx, cy, r = x + 252, 178 + 55, 42
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 90, 120), outline=(255, 210, 90), width=3)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=1)
d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 90, 270, fill=(255, 255, 255), width=1)
d.text((x + 14, 198), "REGULATE AI", font=f(22, bold=True), fill=(255, 210, 90))
d.text((x + 14, 226), "BEFORE IT'S", font=f(16, bold=True), fill=(255, 255, 255))
d.text((x + 14, 248), "TOO LATE", font=f(16, bold=True), fill=(255, 255, 255))
d.text((x + 14, 278), "BRIDGETOWN SUMMIT \u00b7 BARBADOS", font=f(10, bold=True), fill=(180, 220, 235))
# 4 small flags along the bottom of the scene
flag_cols = [(0, 90, 160), (255, 210, 90), (185, 28, 28), (21, 128, 61)]
for i, col in enumerate(flag_cols):
    fx = x + 14 + i * 30
    d.rectangle([fx, 296, fx + 22, 308], fill=col, outline=(255, 255, 255), width=1)
hero_head(x, 2, "GUTERRES: REGULATE AI",
          "150 delegates back a risk framework at Bridgetown; a blueprint, not a treaty.",
          "BARBADOS \u00b7 UN", "REPORTED", GREEN)

# --- scene 3: Power Index bars
x = HX[2]
d.rectangle([x, HY0, x + HW, 316], fill=(248, 244, 236))
d.text((x + 14, 184), "ASIA POWER INDEX 2026", font=f(13, bold=True), fill=INK)
bars = [("US", 78.9, BLUE), ("CHINA", 73.6, RED), ("INDIA", 40.5, TEAL)]
by = 208
for name, val, col in bars:
    d.text((x + 14, by), name, font=f(12, bold=True), fill=INK)
    d.rectangle([x + 76, by + 2, x + 76 + int(val * 2.2), by + 16], fill=col)
    d.text((x + 76 + int(val * 2.2) + 6, by), f"{val:.1f}", font=f(12, bold=True), fill=INK)
    by += 24
d.text((x + 14, 276), "US DIPLOMATIC INFLUENCE -6 TO 76.7", font=f(10, bold=True), fill=MUT)
d.text((x + 14, 294), "GAP 5.3 \u2014 NARROWEST SINCE 2018", font=f(12, bold=True), fill=RED)
hero_head(x, 3, "US LEAD OVER CHINA AT RECORD LOW",
          "Washington 78.9, Beijing 73.6; India holds third at 40.5.",
          "LOWY INSTITUTE", "REPORTED", GREEN)

d.line([M, 472, W - M, 472], fill=LINE, width=1)

# ---------------------------------------------------------------- 10 cards
CARDS = [
    ("Bessent presses Nvidia", "Treasury chief demands answers.", "REPORTED", GREEN),
    ("FBI probes NCIC hack", "Police-database breach probed.", "REPORTED", GREEN),
    ("Trump: Iran strikes may resume", "US warns of New Year action.", "REPORTED", GREEN),
    ("Nasdaq futures +3%", "Holiday week lifts tech.", "REPORTED", GREEN),
    ("Skubal signs $450M Mets deal", "Nine years, a pitcher record.", "REPORTED", GREEN),
    ("Tom Jackson dies at 75", "NFL star turned broadcaster.", "REPORTED", GREEN),
    ("States sue SpaceX", "AI safety claims challenged.", "REPORTED", GREEN),
    ("Anthropic IPO at $107.3B", "Priced $83; debut close $97.17.", "REPORTED", GREEN),
    ("Poland: 3 Russian missiles", "Kh-101s crossed airspace.", "CLAIM", RED),
    ("Intel: Russian nuclear satellite", "Warning over an orbit weapon.", "CLAIM", RED),
]
cy0 = 478
for i, (head, body, ctext, cfill) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x0 = M + c * (CW / 5)
    y0 = cy0 + r * 86
    x1 = x0 + CW / 5 - 8
    d.rectangle([x0, y0, x1, y0 + 80], outline=LINE, width=1)
    hl = wrap(head, f(12, bold=True), x1 - x0 - 12, 2)
    y = y0 + 6
    for ln in hl:
        d.text((x0 + 6, y), ln, font=f(12, bold=True), fill=INK)
        y += 15
    d.text((x0 + 6, y0 + 40), fit1(body, f(10), x1 - x0 - 12), font=f(10), fill=MUT)
    chip(x1 - 6 - (d.textlength(ctext, font=f(10, bold=True)) + 12), y0 + 58, ctext, cfill)

# ---------------------------------------------------------------- map + ALSO
d.rectangle([M, 648, 500, 892], outline=LINE, width=1)
d.text((M + 10, 654), "WORLD MAP \u2014 13 PLACES", font=f(12, bold=True), fill=INK)
# stylised continents: two blobs
d.ellipse([58, 690, 222, 856], fill=(198, 222, 205))          # Americas
d.ellipse([240, 672, 492, 862], fill=(198, 222, 205))         # Eurasia + Africa
d.ellipse([330, 800, 470, 880], fill=(198, 222, 205))         # Africa lobe
PINS = [(450, 715), (165, 815), (110, 745), (320, 720), (300, 692),
        (395, 705), (365, 730), (375, 770), (400, 790), (435, 815),
        (350, 795), (385, 835), (300, 850)]
for i, (px, py) in enumerate(PINS, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
    t = str(i)
    d.text((px - d.textlength(t, font=f(9, bold=True)) / 2, py - 6), t,
           font=f(9, bold=True), fill=(255, 255, 255))
d.text((M + 10, 864), fit1("1 Seoul \u00b7 2 Bridgetown \u00b7 3 Washington \u00b7 4 Paris \u00b7 5 Manchester \u00b7 6 Kyiv \u00b7 7 Warsaw",
                           f(9), 500 - M - 20), font=f(9), fill=MUT)
d.text((M + 10, 878), fit1("8 Gaza \u00b7 9 Beirut \u00b7 10 Manama \u00b7 11 Benghazi \u00b7 12 Khartoum \u00b7 13 Kinshasa",
                           f(9), 500 - M - 20), font=f(9), fill=MUT)

# ALSO list (2 columns x 9 rows)
d.rectangle([512, 648, W - M, 892], outline=LINE, width=1)
d.text((522, 654), "ALSO ON MONDAY", font=f(12, bold=True), fill=INK)
ALSO = ["Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week", "COP31: day after, Antalya pact out",
        "Israel unity talks resume", "Gaza: two killed in Israeli strike",
        "West Bank settler attacks", "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives", "Bahrain: strike hits plant, 2 hurt",
        "Benghazi: UN probe of attacks", "Sudan: drones downed",
        "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if returns",
        "Seoul minister quits over AI exams", "SK Telecom \u22127.3%",
        "China eases margin rules to 80%", "Seoul readies 10T-won fund"]
CLAIMS = {10, 11}  # 0-based indices carrying [CLAIM]
for i, item in enumerate(ALSO):
    c = i // 9
    r = i % 9
    ax = 522 + c * 240
    ay = 678 + r * 24
    base = fit1(item, f(11), 232 - (46 if i in CLAIMS else 0) - 12)
    d.text((ax, ay), "\u2022 " + base, font=f(11), fill=INK)
    if i in CLAIMS:
        tw = d.textlength("\u2022 " + base + " ", font=f(11))
        d.text((ax + tw, ay), "[CLAIM]", font=f(10, bold=True), fill=RED)

# ---------------------------------------------------------------- DATE CHECK
d.rectangle([M, 898, W - M, 976], fill=REDBG, outline=RED, width=2)
d.text((M + 10, 904), "DATE CHECK \u2014 LEFT OUT: NOT 23 NOVEMBER", font=f(12, bold=True), fill=RED)
LEFT = ["Dems reach 258 (22 Nov)", "Sparta II fire (22 Nov)", "El Chapo captured (22 Nov)",
        "EU\u2013Indonesia pact (21 Nov)", "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)"]
for i, t in enumerate(LEFT):
    r, c = divmod(i, 3)
    d.text((M + 10 + c * 325, 926 + r * 18), "\u2022 " + t, font=f(11), fill=INK)
d.text((M + 10, 960), fit1("NOT YET: Dymer search (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating Ebola staff",
                           f(10, bold=True), CW - 20), font=f(10, bold=True), fill=RED)

# ---------------------------------------------------------------- footer
center(M, W - M, 984, "Sources: wires, Lowy Institute, UN, company filings. Illustrations are drawn, not photographs.",
       f(10), fill=MUT)
center(M, W - M, 1000, "REPORTED = confirmed by wires   \u00b7   CLAIM = one side's claim, not independently verified",
       f(10, bold=True), fill=MUT)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
