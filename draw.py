#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026.

A single 1024x1024 newspaper-style image: a masthead naming the day, six
panels, one per leading story of the day, each with a small pictogram drawn
from shapes, a headline and one factual caption, plus a footer line of
smaller items. Every story was verified against at least two independent
reputable sources on 26 November 2026 before it was drawn.

Deterministic: the same script always writes the same bytes (no timestamps,
no randomness, fixed PNG compression).
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 16
GUTTER = 16

PAPER = (246, 241, 231)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
RED = (179, 32, 44)
PANEL_BG = (255, 255, 255)
PANEL_LINE = (205, 198, 184)
FOOTER_INK = (70, 66, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font_obj, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font_obj) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, font_obj, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms
# Each pictogram is drawn inside a square box (bx, by, side) with one accent
# colour. They are simple flat shapes: a bar chart, a refinery flame, a jet,
# a tanker, a rocket and a set of scales.

def pic_tariffs(d, bx, by, s, c):
    # Three rising bars and a percent sign above them.
    base_y = by + s - 18
    widths = [26, 26, 26]
    heights = [34, 56, 82]
    for i, h in enumerate(heights):
        x0 = bx + 12 + i * 34
        d.rectangle([x0, base_y - h, x0 + widths[i], base_y], fill=c)
    d.line([bx + 6, base_y, bx + s - 6, base_y], fill=INK, width=4)
    d.text((bx + 2, by + 0), "%", font=font(SANS_BOLD, 40), fill=c)


def pic_refinery(d, bx, by, s, c):
    # A derrick tower with a flame on top.
    cx = bx + s // 2
    d.polygon([(cx - 34, by + s - 14), (cx - 12, by + 34),
               (cx + 12, by + 34), (cx + 34, by + s - 14)], outline=c, width=5)
    d.line([cx - 34, by + s - 14, cx + 34, by + s - 14], fill=c, width=5)
    d.line([cx - 26, by + 76, cx + 26, by + 76], fill=c, width=4)
    d.line([cx - 18, by + 52, cx + 18, by + 52], fill=c, width=4)
    d.polygon([(cx - 12, by + 34), (cx, by + 2), (cx + 12, by + 34)],
              fill=(216, 74, 31))
    d.polygon([(cx - 5, by + 34), (cx, by + 18), (cx + 5, by + 34)],
              fill=(240, 180, 40))


def pic_jet(d, bx, by, s, c):
    # A jet seen from above, nose up, with a small burst behind it.
    cx = bx + s // 2
    cy = by + s // 2 - 6
    d.polygon([(cx, cy - 52), (cx + 9, cy - 8), (cx + 9, cy + 18),
               (cx, cy + 34), (cx - 9, cy + 18), (cx - 9, cy - 8)], fill=c)
    d.polygon([(cx - 9, cy - 12), (cx - 44, cy + 26), (cx - 44, cy + 34),
               (cx - 9, cy + 6)], fill=c)
    d.polygon([(cx + 9, cy - 12), (cx + 44, cy + 26), (cx + 44, cy + 34),
               (cx + 9, cy + 6)], fill=c)
    d.polygon([(cx - 8, cy + 22), (cx - 26, cy + 48), (cx - 20, cy + 52),
               (cx - 4, cy + 34)], fill=c)
    d.polygon([(cx + 8, cy + 22), (cx + 26, cy + 48), (cx + 20, cy + 52),
               (cx + 4, cy + 34)], fill=c)
    for dx, dy in ((-46, -38), (-30, -48), (-14, -44), (10, -48),
                   (28, -40), (44, -30)):
        d.line([cx + dx, cy + dy, cx + dx + 12, cy + dy + 12],
               fill=(216, 74, 31), width=4)


def pic_tanker(d, bx, by, s, c):
    # A fuel tanker with a flame above its tank.
    d.rounded_rectangle([bx + 8, by + 52, bx + 92, by + 92], radius=18, fill=c)
    d.polygon([(bx + 92, by + 60), (bx + 118, by + 60), (bx + 118, by + 92),
               (bx + 92, by + 92)], fill=c)
    d.rectangle([bx + 96, by + 66, bx + 114, by + 78], fill=PAPER)
    for wx in (bx + 30, bx + 66, bx + 106):
        d.ellipse([wx - 11, by + 92, wx + 11, by + 114], fill=INK)
        d.ellipse([wx - 4, by + 99, wx + 4, by + 107], fill=PAPER)
    d.line([bx + 8, by + 118, bx + 122, by + 118], fill=INK, width=4)
    cx = bx + 52
    d.polygon([(cx - 14, by + 52), (cx, by + 14), (cx + 14, by + 52)],
              fill=(216, 74, 31))
    d.polygon([(cx - 6, by + 52), (cx, by + 30), (cx + 6, by + 52)],
              fill=(240, 180, 40))


def pic_rocket(d, bx, by, s, c):
    # A rocket climbing, with exhaust flame and two stars.
    cx = bx + s // 2
    cy = by + s // 2 - 4
    d.polygon([(cx, cy - 56), (cx + 13, cy - 18), (cx + 13, cy + 22),
               (cx, cy + 34), (cx - 13, cy + 22), (cx - 13, cy - 18)],
              fill=c)
    d.ellipse([cx - 4, cy - 34, cx + 4, cy - 26], fill=PAPER)
    d.polygon([(cx - 13, cy + 6), (cx - 34, cy + 34), (cx - 13, cy + 26)],
              fill=c)
    d.polygon([(cx + 13, cy + 6), (cx + 34, cy + 34), (cx + 13, cy + 26)],
              fill=c)
    d.polygon([(cx - 8, cy + 34), (cx, cy + 62), (cx + 8, cy + 34)],
              fill=(216, 74, 31))
    d.polygon([(cx - 3, cy + 34), (cx, cy + 50), (cx + 3, cy + 34)],
              fill=(240, 180, 40))
    for sx, sy in ((bx + 8, by + 14), (bx + s - 18, by + 84)):
        d.polygon([(sx, sy - 8), (sx + 2, sy - 2), (sx + 8, sy),
                   (sx + 2, sy + 2), (sx, sy + 8), (sx - 2, sy + 2),
                   (sx - 8, sy), (sx - 2, sy - 2)], fill=(240, 180, 40))


def pic_scales(d, bx, by, s, c):
    # Scales of justice: a post, a beam and two hanging pans.
    cx = bx + s // 2
    d.rectangle([cx - 4, by + 18, cx + 4, by + s - 22], fill=c)
    d.line([cx - 48, by + 22, cx + 48, by + 22], fill=c, width=6)
    d.ellipse([cx - 7, by + 12, cx + 7, by + 26], fill=c)
    for side in (-1, 1):
        px = cx + side * 48
        d.line([px, by + 22, px, by + 62], fill=c, width=3)
        d.polygon([(px - 24, by + 62), (px + 24, by + 62),
                   (px, by + 84)], fill=c)
    d.rectangle([cx - 34, by + s - 22, cx + 34, by + s - 14], fill=c)


# ------------------------------------------------------------------- stories
# Headline and caption text are kept short so they stay legible at 300 px.

STORIES = [
    {
        "kicker": "TRADE  ·  WASHINGTON",
        "accent": (179, 32, 44),
        "pic": pic_tariffs,
        "headline": "US proposes new tariffs on 14 partners",
        "caption": "China, the EU, Japan and India among those hit in a plan aimed at factory overcapacity.",
    },
    {
        "kicker": "ENERGY  ·  THE GULF",
        "accent": (199, 122, 26),
        "pic": pic_refinery,
        "headline": "Houthis strike Saudi Arabia's biggest refinery",
        "caption": "Ras Tanura attacked; oil prices climb on fears of supply disruption.",
    },
    {
        "kicker": "WAR  ·  UKRAINE",
        "accent": (58, 90, 140),
        "pic": pic_jet,
        "headline": "Ukraine hits Russian airbase; five jets damaged",
        "caption": "Kyiv says it also struck two oil refineries in the Samara region.",
    },
    {
        "kicker": "DISASTER  ·  CAIRO",
        "accent": (216, 74, 31),
        "pic": pic_tanker,
        "headline": "Fuel tanker fire kills at least 31 on Cairo ring road",
        "caption": "A tanker overturned and burst into flames; about 21 people were hurt.",
    },
    {
        "kicker": "NUCLEAR  ·  PYONGYANG",
        "accent": (91, 45, 142),
        "pic": pic_rocket,
        "headline": "Kim orders wider tactical nuclear deployment",
        "caption": "North Korea to expand nuclear material production, state media KCNA says.",
    },
    {
        "kicker": "ISRAEL  ·  JERUSALEM",
        "accent": (31, 111, 92),
        "pic": pic_scales,
        "headline": "Judges urge dropping gravest Netanyahu charge",
        "caption": "Court says the bribery case is unlikely to convict; PM calls for trial to end.",
    },
]

FOOTER = ("ALSO TODAY — Bank of Korea raises its rate to 3.25%  ·  "
          "AI sell-off drags Nasdaq toward a bear market  ·  "
          "MiniMax user data reached by unknown parties")


def draw_panel(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=PANEL_LINE,
                width=2)
    d.rectangle([x, y, x + w, y + 6], fill=story["accent"])
    kicker_f = font(SANS_BOLD, 17)
    head_f = font(SANS_BOLD, 29)
    cap_f = font(SANS, 18)
    tx = x + 18
    d.text((tx, y + 20), story["kicker"], font=kicker_f,
           fill=story["accent"])
    # Pictogram on the right, headline and caption on the left.
    pic_side = 128
    pic_x = x + w - pic_side - 14
    pic_y = y + 58
    story["pic"](d, pic_x, pic_y, pic_side, story["accent"])
    text_w = pic_x - tx - 14
    head_lines = wrap(d, story["headline"], head_f, text_w)
    cy = draw_lines(d, head_lines, tx, y + 52, head_f, INK, 36)
    cap_lines = wrap(d, story["caption"], cap_f, text_w)
    draw_lines(d, cap_lines, tx, cy + 8, cap_f, MUTED, 24)


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, SIZE, 10], fill=RED)
    title_f = font(SERIF_BOLD, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((SIZE - tw) / 2, 26), title, font=title_f, fill=INK)
    date_f = font(SANS_BOLD, 36)
    date = "THURSDAY  26  NOVEMBER  2026"
    dw = d.textlength(date, font=date_f)
    d.text(((SIZE - dw) / 2, 104), date, font=date_f, fill=RED)
    d.line([MARGIN, 156, SIZE - MARGIN, 156], fill=INK, width=3)
    d.line([MARGIN, 162, SIZE - MARGIN, 162], fill=INK, width=1)

    # Six story panels, two columns by three rows.
    panel_w = (SIZE - 2 * MARGIN - GUTTER) // 2
    panel_h = 246
    top = 180
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (panel_w + GUTTER)
        y = top + row * (panel_h + GUTTER)
        draw_panel(d, story, x, y, panel_w, panel_h)

    # Footer line of smaller items.
    fy = top + 3 * panel_h + 2 * GUTTER + 12
    d.line([MARGIN, fy - 8, SIZE - MARGIN, fy - 8], fill=INK, width=2)
    foot_f = font(SANS_BOLD, 17)
    lines = wrap(d, FOOTER, foot_f, SIZE - 2 * MARGIN)
    draw_lines(d, lines, MARGIN, fy, foot_f, FOOTER_INK, 24)

    img.save("entry.png", format="PNG", compress_level=9)


if __name__ == "__main__":
    main()
