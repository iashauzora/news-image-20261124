#!/usr/bin/env python3
"""Render entry.png — 'THE WORLD IN A DAY', Tuesday 24 November 2026.

A newspaper front page summing up the day's world news in one image.
Stories and citations: design/sources.md.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (18, 18, 18)
GREY = (90, 86, 78)
ACCENT = (142, 26, 26)
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, y, text, fnt, fill=INK):
    w_ = draw.textlength(text, font=fnt)
    draw.text(((W - w_) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def story(draw, x, y, w_, kicker, headline, deck, h_size=28, d_size=16):
    draw.text((x, y), kicker, font=font(SANS_B, 14), fill=ACCENT)
    y += 22
    y = text_block(draw, x, y, headline, font(SERIF_B, h_size), w_, h_size + 5)
    y += 4
    y = text_block(draw, x, y, deck, font(SERIF, d_size), w_, d_size + 5, fill=(40, 40, 40))
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 46  # margin
CW = W - 2 * M  # content width

# ---- Masthead -------------------------------------------------------------
d.line([(M, 30), (W - M, 30)], fill=INK, width=5)
d.line([(M, 40), (W - M, 40)], fill=INK, width=1)
y = centered(d, 52, "THE WORLD IN A DAY", font(SERIF_B, 68))
y += 10
d.line([(M, y), (W - M, y)], fill=INK, width=1)
y += 8
centered(d, y, "TUESDAY 24 NOVEMBER 2026", font(SANS_B, 25))
y += 36
d.line([(M, y), (W - M, y)], fill=INK, width=3)
y += 16

# ---- Lead story -----------------------------------------------------------
d.text((M, y), "LEAD STORY · BUSINESS", font=font(SANS_B, 15), fill=ACCENT)
y += 24
y = text_block(d, M, y, "NVIDIA BOARD REINSTATES JENSEN HUANG AS CEO",
               font(SERIF_B, 44), CW - 190, 51)
y += 6
lead_deck = ("Unanimous vote restores the founder to the top of the AI chip "
             "giant after a Washington lobbying push. Asian tech shares surge "
             "on the news — South Korea's SK hynix jumps 20%.")
y = text_block(d, M, y, lead_deck, font(SERIF, 19), CW - 190, 26, fill=(40, 40, 40))
# chip motif, right of the lead
cx, cy, cs = W - M - 150, 218, 118
d.rectangle([cx, cy, cx + cs, cy + cs], outline=INK, width=4)
for i in range(4):
    p = cy + 18 + i * 26
    d.line([(cx - 22, p), (cx, p)], fill=INK, width=4)
    d.line([(cx + cs, p), (cx + cs + 22, p)], fill=INK, width=4)
    q = cx + 18 + i * 26
    d.line([(q, cy - 22), (q, cy)], fill=INK, width=4)
    d.line([(q, cy + cs), (q, cy + cs + 22)], fill=INK, width=4)
d.rectangle([cx + 26, cy + 26, cx + cs - 26, cy + cs - 26], outline=INK, width=3)
tw = d.textlength("AI", font=font(SANS_B, 30))
d.text((cx + (cs - tw) / 2, cy + 40), "AI", font=font(SANS_B, 30), fill=ACCENT)
y += 14
d.line([(M, y), (W - M, y)], fill=INK, width=2)
y += 16

# ---- Two-column stories ----------------------------------------------------
COLW = (CW - 28) // 2
LX, RX = M, M + COLW + 28
col_top = y
left_end = story(
    d, LX, col_top, COLW, "WAR IN UKRAINE",
    "Leaked data puts Russia's war death toll near 700,000",
    "Analysis of classified government figures suggests the toll is far "
    "above anything Moscow has admitted, media report.")
left_end += 18
left_end = story(
    d, LX, left_end, COLW, "WAR IN UKRAINE",
    "Pentagon yet to approve 60 Patriot interceptors for Ukraine",
    "Defence chief Hegseth has not signed off on PAC-3 and PAC-2 missiles "
    "already allocated and paid for by allies, the FT reports.")
right_end = story(
    d, RX, col_top, COLW, "BUSINESS",
    "SpaceX and Tesla set five directors on $3.5 trillion merger",
    "The two boards entrust a small team to hash out the details of a "
    "combination, racing to finalise a deal by year-end.")
right_end += 12
right_end = story(
    d, RX, right_end, COLW, "ASIA-PACIFIC",
    "South Korea scrambles jets as Russian warplanes enter air zone",
    "Seoul issues an alert and mobilises fighter jets after Russian "
    "aircraft breach its air defence identification zone.")
y = max(left_end, right_end) + 16
d.line([(M, y), (W - M, y)], fill=INK, width=2)
y += 16

# ---- Bottom story, full width ---------------------------------------------
y = story(
    d, M, y, CW, "TRADE · SOUTH-EAST ASIA",
    "Malaysia tells data centres to cut off US-blacklisted firms",
    "Kuala Lumpur advises operators not to host or serve seven blacklisted "
    "companies, including Singapore-based Megaspeed, and vows that US export "
    "curbs will not be circumvented through Malaysia.",
    h_size=25, d_size=16)
y += 14
d.line([(M, y), (W - M, y)], fill=INK, width=1)
y += 8
centered(d, y, "Reported 24 Nov 2026 by AP, Reuters, the FT, the Kyiv Independent and others —",
         font(SERIF_I, 14), fill=GREY)
y += 20
centered(d, y, "full citations in design/sources.md", font(SERIF_I, 14), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, "final y:", y)
