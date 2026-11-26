#!/usr/bin/env python3
"""Generate a 1024x1024 newspaper front page: The World in One Page.

Draws a classic broadsheet front page with Pillow: a red-accented
masthead, one lead story with a large headline and an illustration
panel, and six smaller stories arranged in a two-column grid below.
Run from the entry directory:

    python3 make-image.py

and the page is written to entry.png next to this script.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Page geometry and palette
# ---------------------------------------------------------------------------

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 44
GUTTER = 24

PAPER = (250, 246, 232)      # warm off-white paper
INK = (18, 18, 18)           # near-black text
SOFT_INK = (74, 74, 74)      # grey for decks and captions
RULE = (40, 40, 40)          # rule lines
RED = (178, 34, 34)          # masthead accent red
RED_DARK = (140, 22, 22)
PANEL = (232, 224, 200)      # illustration panel fill
PANEL_LINE = (120, 110, 88)
GOLD = (176, 141, 60)

TITLE = "The World in One Page"
DATE_LINE = "Wednesday 26 November 2026"
ISSUE_LINE = "No. 331  |  World Edition  |  Price: Free"

LEAD_KICKER = "MIDDLE EAST"
LEAD_HEADLINE = "Houthis fire three missile waves at Saudi targets"
LEAD_DECK = (
    "Riyadh airport, Khamis Mushait and Jizan hit after Saudi "
    "strikes on Sanaa escalate the cross-border exchange."
)
LEAD_BODY = (
    "Riyadh came under fire in three successive waves on Tuesday as "
    "Houthi forces launched missiles toward the capital's airport, "
    "the southern city of Khamis Mushait and the port of Jizan. "
    "Saudi air defences said they intercepted most of the incoming "
    "fire, while officials reported damage and disruption at the "
    "airport. The salvo followed Saudi air strikes on Sanaa, and "
    "raised fears of a wider round of retaliation across the region."
)
LEAD_CAPTION = "Smoke rises over the capital after the latest exchange of fire."

STORIES = [
    (
        "SPACE",
        "First Pakistani astronaut to Tiangong space station",
        "Islamabad hails a milestone for its space programme as its "
        "first astronaut prepares to fly to China's Tiangong station, "
        "a mission officials say will carry out joint research.",
    ),
    (
        "TRADE",
        "Trump imposes tariffs on 14 trading partners",
        "Washington unveiled sweeping new duties on fourteen trading "
        "partners, rattling markets and drawing swift warnings of "
        "retaliation from several capitals.",
    ),
    (
        "EGYPT",
        "Cairo fuel-tanker fire kills 31",
        "A fuel tanker caught fire in Cairo, killing at least 31 "
        "people and injuring dozens more, in one of the city's "
        "deadliest road disasters in years.",
    ),
    (
        "LABOUR",
        "Bangladesh garment workers win 36% pay rise",
        "Garment workers in Bangladesh secured a 36 per cent pay "
        "rise after weeks of protest, a landmark settlement for the "
        "country's largest export industry.",
    ),
    (
        "PACIFIC",
        "Australia-Solomon Islands security pact signed",
        "Canberra and Honiara signed a new security pact, deepening "
        "policing and defence cooperation across the Pacific.",
    ),
    (
        "CRICKET",
        "Sooryavanshi scores 204 off 53 balls",
        "The young opener smashed 204 from just 53 balls, one of the "
        "fastest double centuries in the history of the game.",
    ),
]

FOOTER = "The World in One Page  |  Compiled from wire reports  |  Page 1 of 1"


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

def _try_font(paths, size):
    """Return the first usable TrueType font from paths, else None."""
    for path in paths:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return None


def load_fonts():
    """Load serif fonts when available, falling back to the default font."""
    serif_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    ]
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ]
    title = _try_font(serif_paths, 64)
    headline = _try_font(bold_paths, 44)
    subhead = _try_font(bold_paths, 26)
    body = _try_font(serif_paths, 19)
    small = _try_font(serif_paths, 16)
    caption = _try_font(serif_paths, 15)
    fallback = ImageFont.load_default()
    return {
        "title": title or fallback,
        "headline": headline or fallback,
        "subhead": subhead or fallback,
        "body": body or fallback,
        "small": small or fallback,
        "caption": caption or fallback,
    }


def wrap(draw, text, font, max_width):
    """Wrap text to fit max_width pixels, returning a list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        width = draw.textlength(trial, font=font)
        if width <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_height(draw, lines, font, leading):
    """Total pixel height of wrapped lines at the given leading."""
    if not lines:
        return 0
    ascent, descent = font.getmetrics()
    return len(lines) * leading + (len(lines) - 1) * 2


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_masthead(draw, fonts, width):
    """Draw the red-accented masthead and return the y below it."""
    y = 28
    draw.rectangle([MARGIN, y, width - MARGIN, y + 6], fill=RED)
    y += 22
    title_w = draw.textlength(TITLE, font=fonts["title"])
    draw.text(((width - title_w) / 2, y), TITLE, font=fonts["title"],
              fill=RED_DARK)
    y += 76
    draw.line([MARGIN, y, width - MARGIN, y], fill=RULE, width=3)
    y += 10
    date_w = draw.textlength(DATE_LINE, font=fonts["subhead"])
    draw.text(((width - date_w) / 2, y), DATE_LINE,
              font=fonts["subhead"], fill=INK)
    y += 34
    issue_w = draw.textlength(ISSUE_LINE, font=fonts["small"])
    draw.text(((width - issue_w) / 2, y), ISSUE_LINE,
              font=fonts["small"], fill=SOFT_INK)
    y += 26
    draw.line([MARGIN, y, width - MARGIN, y], fill=RULE, width=3)
    draw.line([MARGIN, y + 5, width - MARGIN, y + 5], fill=RULE, width=1)
    return y + 14


def draw_skyline(draw, x, y, width, panel_h):
    """Draw a row of dark tower silhouettes along the panel baseline."""
    base = y + panel_h
    towers = [(0, 96), (70, 60), (140, 112), (210, 48), (280, 88),
              (350, 64), (420, 104), (490, 56), (560, 92), (630, 70),
              (700, 108), (770, 62), (840, 96)]
    for offset, height in towers:
        tx = x + offset
        draw.rectangle([tx, base - height, tx + 46, base],
                       fill=(52, 48, 40))
    draw.line([x, base - 6, x + width, base - 6], fill=(52, 48, 40),
              width=2)


def draw_lead(draw, fonts, x, y, width):
    """Draw the lead story and return the y below it."""
    draw.text((x, y), LEAD_KICKER, font=fonts["subhead"], fill=RED)
    y += 34
    head_lines = wrap(draw, LEAD_HEADLINE, fonts["headline"], width)
    for line in head_lines:
        draw.text((x, y), line, font=fonts["headline"], fill=INK)
        y += 52
    y += 4
    deck_lines = wrap(draw, LEAD_DECK, fonts["body"], width)
    for line in deck_lines:
        draw.text((x, y), line, font=fonts["body"], fill=SOFT_INK)
        y += 26
    y += 10
    # Illustration panel: a skyline silhouette under a gold sun.
    panel_h = 110
    draw.rectangle([x, y, x + width, y + panel_h], fill=PANEL,
                   outline=PANEL_LINE, width=2)
    draw.ellipse([x + width - 150, y + 22, x + width - 80, y + 92],
                 fill=GOLD)
    draw_skyline(draw, x, y, width, panel_h)
    y += panel_h + 8
    draw.text((x, y), LEAD_CAPTION, font=fonts["caption"], fill=SOFT_INK)
    y += 22
    body_lines = wrap(draw, LEAD_BODY, fonts["body"], width)
    for line in body_lines[:2]:
        draw.text((x, y), line, font=fonts["body"], fill=INK)
        y += 24
    return y + 6


def draw_story(draw, fonts, x, y, width, kicker, headline, body):
    """Draw one small grid story and return the y below it."""
    draw.text((x, y), kicker, font=fonts["small"], fill=RED)
    y += 20
    head_lines = wrap(draw, headline, fonts["subhead"], width)
    for line in head_lines:
        draw.text((x, y), line, font=fonts["subhead"], fill=INK)
        y += 28
    y += 2
    body_lines = wrap(draw, body, fonts["small"], width)
    for line in body_lines[:2]:
        draw.text((x, y), line, font=fonts["small"], fill=SOFT_INK)
        y += 20
    return y


def draw_footer(draw, fonts, width):
    """Draw the footer rule and line at the bottom of the page."""
    y = PAGE_H - 40
    draw.line([MARGIN, y, width - MARGIN, y], fill=RULE, width=2)
    foot_w = draw.textlength(FOOTER, font=fonts["caption"])
    draw.text(((width - foot_w) / 2, y + 10), FOOTER,
              font=fonts["caption"], fill=SOFT_INK)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def main():
    """Build the front page and save it as entry.png."""
    image = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(image)
    fonts = load_fonts()

    content_w = PAGE_W - 2 * MARGIN
    y = draw_masthead(draw, fonts, PAGE_W)
    y = draw_lead(draw, fonts, MARGIN, y, content_w)

    draw.line([MARGIN, y, PAGE_W - MARGIN, y], fill=RULE, width=2)
    y += 16

    col_w = (content_w - GUTTER) // 2
    row_y = y
    for index, (kicker, headline, body) in enumerate(STORIES):
        col = index % 2
        row = index // 2
        cell_x = MARGIN + col * (col_w + GUTTER)
        cell_y = row_y + row * 118
        if col == 1:
            draw.line([MARGIN + col_w + GUTTER // 2, cell_y,
                       MARGIN + col_w + GUTTER // 2, cell_y + 100],
                      fill=(190, 182, 160), width=1)
        draw_story(draw, fonts, cell_x, cell_y, col_w,
                   kicker, headline, body)

    draw_footer(draw, fonts, PAGE_W)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png")
    image.save(out_path, "PNG")
    print(f"Saved {out_path} ({PAGE_W}x{PAGE_H})")


if __name__ == "__main__":
    main()
