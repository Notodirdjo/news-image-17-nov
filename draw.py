#!/usr/bin/env python3
"""Render the 17 November 2026 world-news front page as a 1024x1024 PNG.

Draws only with Pillow and the facts hard-coded below (researched from
Al Jazeera / Reuters / Outlook India / HKFP reporting of 17 Nov 2026).
Run:  python3 draw.py   -> writes entry.png next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
MARGIN = 48
CONTENT = WIDTH - 2 * MARGIN  # 928

PAPER = (248, 244, 235)
NAVY = (18, 38, 75)
RED = (176, 42, 48)
INK = (26, 26, 26)
GREY = (90, 86, 78)
RULE = (201, 194, 178)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


TITLE_FONT = font("DejaVuSerif-Bold.ttf", 56)
DATE_FONT = font("DejaVuSans-Bold.ttf", 38)
TAG_FONT = font("DejaVuSans-Bold.ttf", 22)
HEAD_FONT = font("DejaVuSans-Bold.ttf", 30)
SUMMARY_FONT = font("DejaVuSans.ttf", 21)
ALSO_HEAD_FONT = font("DejaVuSans-Bold.ttf", 22)
ALSO_FONT = font("DejaVuSans.ttf", 19)
SOURCE_FONT = font("DejaVuSans.ttf", 15)

STORIES = [
    (
        "UKRAINE",
        "Kerch Bridge hit again; Kyiv's bridges struck",
        "Ukraine struck the Kerch Bridge early Tuesday, the second attack in "
        "under 24 hours; part of the road span collapsed. Missiles hit Kyiv's "
        "North and South bridges.",
    ),
    (
        "STRAIT OF HORMUZ",
        "Tankers hit by mines; third US carrier arrives",
        "Oil tankers struck mines and caught fire near the Strait of Hormuz; "
        "one was left disabled. A third US carrier arrived \u2014 the first "
        "three-carrier force there since April.",
    ),
    (
        "SHENZHEN",
        "Xi, Trump and Putin to meet on Thursday",
        "China confirmed the first three-way meeting of Xi Jinping, Donald "
        "Trump and Vladimir Putin, on Thursday in Shenzhen, to discuss "
        "nuclear risks and Ukraine.",
    ),
    (
        "EUROPE",
        "Five states plan a joint migrant return hub in Rwanda",
        "Germany, Denmark, Austria, Greece and the Netherlands announced a "
        "partnership to build a joint return facility in Rwanda for rejected "
        "asylum seekers.",
    ),
    (
        "WASHINGTON",
        "Pentagon fails its audit for a ninth straight year",
        "Independent auditors again issued a disclaimer on the Pentagon's "
        "books for fiscal 2026 \u2014 accounts covering more than $4.8 "
        "trillion in assets could not be verified.",
    ),
]

ALSO_TODAY = [
    "US moves to close the AI-chip loophole letting China rent US computing power.",
    "Japan scrambles fighter jets after Russian aircraft enter its airspace.",
    "Houthi forces advance in Yemen as Saudi-backed troops pull back toward Aden.",
    "G\u00e9rard Depardieu admits a sexual assault charge in a Paris court.",
]


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, measured with the font."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, WIDTH, 160], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    d.text(((WIDTH - d.textlength(title, font=TITLE_FONT)) / 2, 22),
           title, font=TITLE_FONT, fill=(255, 255, 255))
    d.rectangle([MARGIN, 92, WIDTH - MARGIN, 96], fill=RED)
    date = "Tuesday 17 November 2026"
    d.text(((WIDTH - d.textlength(date, font=DATE_FONT)) / 2, 106),
           date, font=DATE_FONT, fill=(255, 255, 255))

    # ---- Story blocks ---------------------------------------------------
    y = 172
    for i, (tag, headline, summary) in enumerate(STORIES):
        d.text((MARGIN, y), tag, font=TAG_FONT, fill=NAVY)
        y += 27
        for line in wrap(d, headline, HEAD_FONT, CONTENT):
            d.text((MARGIN, y), line, font=HEAD_FONT, fill=INK)
            y += 35
        y += 3
        for line in wrap(d, summary, SUMMARY_FONT, CONTENT):
            d.text((MARGIN, y), line, font=SUMMARY_FONT, fill=(52, 52, 52))
            y += 25
        y += 8
        if i < len(STORIES) - 1:
            d.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=RULE, width=1)
            y += 9

    # ---- Also today -----------------------------------------------------
    d.rectangle([0, y + 4, WIDTH, y + 8], fill=RED)
    y += 18
    d.text((MARGIN, y), "ALSO TODAY", font=ALSO_HEAD_FONT, fill=RED)
    y += 30
    for item in ALSO_TODAY:
        d.text((MARGIN, y), "\u2022  " + item, font=ALSO_FONT, fill=INK)
        y += 24

    # ---- Source line ----------------------------------------------------
    source = "Sources: Al Jazeera, Reuters, Outlook India, HKFP \u2014 17 Nov 2026"
    d.text((MARGIN, HEIGHT - 28), source, font=SOURCE_FONT, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
