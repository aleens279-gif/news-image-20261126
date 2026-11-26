#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: a 1024x1024 PNG newspaper,
rendered with Pillow and DejaVu fonts so all text is spelled correctly
and legible at small sizes.

Structure: black masthead with the date, one lead story, six stories in
a two-by-three grid, and a navy footer strip of short items.
Run: python3 make-image.py  ->  writes entry.png in this directory.
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (250, 246, 236)
INK = (20, 20, 20)
BODY = (51, 51, 51)
MUTED = (90, 90, 90)
RULE = (180, 175, 160)
GOLD = (201, 162, 39)
NAVY = (20, 33, 61)
WHITE = (255, 255, 255)
CREAM = (216, 201, 138)

FONTS = "/usr/share/fonts/truetype/dejavu/"

MASTHEAD_DATE = "THURSDAY  26  NOVEMBER  2026"
MASTHEAD_TITLE = "THE WORLD IN ONE PAGE"

LEAD_STORY = {
    "tag": "MIDDLE EAST",
    "tag_color": (121, 85, 0),
    "headline": "HOUTHIS FIRE THREE MISSILE WAVES AT SAUDI TARGETS",
    "summary": (
        "Missiles hit Riyadh airport, Khamis Mushait air base and a "
        "Jizan naval base after Saudi strikes on Sanaa; Riyadh sounds "
        "its third night of alerts."
    ),
}

GRID_STORIES = [
    {
        "tag": "SPACE",
        "tag_color": (29, 78, 137),
        "headline": "First Pakistani astronaut reaches Tiangong station",
        "summary": (
            "China's Shenzhou crew blasts off with Muhammad Zeeshan Ali, "
            "the first foreign astronaut to visit the Tiangong station."
        ),
    },
    {
        "tag": "TRADE",
        "tag_color": (21, 101, 192),
        "headline": "Trump proposes tariffs on 14 trading partners",
        "summary": (
            "US plans levies on goods from 14 partners, including the EU "
            "and China; markets fall as the tariff threat spreads."
        ),
    },
    {
        "tag": "EGYPT",
        "tag_color": (156, 27, 27),
        "headline": "31 killed as fuel tanker overturns and burns",
        "summary": (
            "A petroleum vehicle overturns on a Cairo ring road and "
            "erupts in flames, killing 31 people."
        ),
    },
    {
        "tag": "ASIA",
        "tag_color": (0, 121, 107),
        "headline": "Bangladesh garment workers win 36% pay rise",
        "summary": (
            "Dhaka raises the minimum wage for entry-level garment "
            "workers by more than a third."
        ),
    },
    {
        "tag": "PACIFIC",
        "tag_color": (106, 27, 154),
        "headline": "Australia signs security pact with Solomons",
        "summary": (
            "Canberra and Honiara sign a landmark security deal seen as "
            "a check on China's sway in the Pacific."
        ),
    },
    {
        "tag": "SPORT",
        "tag_color": (46, 125, 50),
        "headline": "Teenager, 15, smashes 204 off 53 balls",
        "summary": (
            "Vaibhav Sooryavanshi sets a world-record T20 innings as "
            "India pile up runs against the UAE."
        ),
    },
]

FOOTER_ITEMS = [
    "Macy's parade put off to Saturday by storm",
    "Sudan strikes kill 19 civilians",
    "N. Korea expels Swiss envoy",
    "Andy Taylor of Duran Duran dies at 65",
]


def load_font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width (greedy word wrap)."""
    wrapped = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                wrapped.append(current)
            current = word
    if current:
        wrapped.append(current)
    return wrapped


def draw_tag(draw, x, y, label, color, font):
    """A small rounded colour chip with white bold text; returns its size."""
    text_w = draw.textlength(label, font=font)
    pad_x, pad_y = 10, 5
    w = int(text_w) + 2 * pad_x
    h = font.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=color)
    draw.text((x + pad_x, y + pad_y - 1), label, font=font, fill=WHITE)
    return w, h


def draw_masthead(draw):
    draw.rectangle([0, 0, 1024, 116], fill=(0, 0, 0))
    title_font = load_font("DejaVuSerif-Bold.ttf", 56)
    title_w = draw.textlength(MASTHEAD_TITLE, font=title_font)
    draw.text(((1024 - title_w) / 2, 24), MASTHEAD_TITLE,
              font=title_font, fill=WHITE)
    date_font = load_font("DejaVuSans.ttf", 22)
    date_w = draw.textlength(MASTHEAD_DATE, font=date_font)
    draw.text(((1024 - date_w) / 2, 84), MASTHEAD_DATE,
              font=date_font, fill=CREAM)
    draw.rectangle([0, 116, 1024, 120], fill=GOLD)


def draw_lead(draw):
    x, y = 36, 140
    tag_font = load_font("DejaVuSans-Bold.ttf", 17)
    draw_tag(draw, x, y, LEAD_STORY["tag"], LEAD_STORY["tag_color"], tag_font)
    y += 40
    head_font = load_font("DejaVuSerif-Bold.ttf", 44)
    head_lines = wrap_text(draw, LEAD_STORY["headline"], head_font, 1024 - 72)
    assert len(head_lines) <= 2, "lead headline too long: %s" % head_lines
    for line in head_lines:
        draw.text((x, y), line, font=head_font, fill=INK)
        y += 56
    y += 8
    sum_font = load_font("DejaVuSans.ttf", 23)
    sum_lines = wrap_text(draw, LEAD_STORY["summary"], sum_font, 1024 - 72)
    assert len(sum_lines) <= 2, "lead summary too long: %s" % sum_lines
    for line in sum_lines:
        draw.text((x, y), line, font=sum_font, fill=BODY)
        y += 32
    draw.line([(36, 366), (1024 - 36, 366)], fill=RULE, width=2)


def draw_grid(draw):
    col_w = (1024 - 72 - 28) // 2
    row_h = 178
    top = 384
    tag_font = load_font("DejaVuSans-Bold.ttf", 15)
    head_font = load_font("DejaVuSans-Bold.ttf", 25)
    sum_font = load_font("DejaVuSans.ttf", 19)
    for index, story in enumerate(GRID_STORIES):
        row, col = divmod(index, 2)
        cx = 36 + col * (col_w + 28)
        cy = top + row * row_h
        draw_tag(draw, cx, cy, story["tag"], story["tag_color"], tag_font)
        hy = cy + 32
        head_lines = wrap_text(draw, story["headline"], head_font, col_w)
        assert len(head_lines) <= 2, "grid headline too long: %s" % head_lines
        for line in head_lines:
            draw.text((cx, hy), line, font=head_font, fill=INK)
            hy += 31
        hy += 4
        sum_lines = wrap_text(draw, story["summary"], sum_font, col_w)
        assert len(sum_lines) <= 3, "grid summary too long: %s" % sum_lines
        for line in sum_lines:
            draw.text((cx, hy), line, font=sum_font, fill=BODY)
            hy += 25
        if col == 0:
            draw.line([(512, cy + 4), (512, cy + row_h - 14)],
                      fill=RULE, width=1)
        if row < 2:
            draw.line([(36, cy + row_h - 6), (1024 - 36, cy + row_h - 6)],
                      fill=RULE, width=1)


def draw_footer(draw):
    draw.rectangle([0, 930, 1024, 1024], fill=NAVY)
    label_font = load_font("DejaVuSans-Bold.ttf", 20)
    item_font = load_font("DejaVuSans.ttf", 20)
    label = "ALSO TODAY:  "
    label_w = draw.textlength(label, font=label_font)
    joined = "  •  ".join(FOOTER_ITEMS)
    lines = wrap_text(draw, joined, item_font, 1024 - 72 - int(label_w))
    assert len(lines) <= 2, "footer too long: %s" % lines
    fy = 942
    draw.text((36, fy), label, font=label_font, fill=CREAM)
    draw.text((36 + label_w, fy), lines[0], font=item_font, fill=(235, 235, 235))
    if len(lines) > 1:
        draw.text((36, fy + 27), lines[1], font=item_font, fill=(235, 235, 235))


def build():
    image = Image.new("RGB", CANVAS, PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_footer(draw)
    image.save("entry.png", optimize=True)
    print("wrote entry.png", image.size)


if __name__ == "__main__":
    build()
