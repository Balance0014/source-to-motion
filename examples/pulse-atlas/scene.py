"""Warm editorial dashboard demo from a fictional Word brief."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (960, 540)
FPS = 24
DURATION = 10.0
BG = (242, 239, 230)
INK = (21, 34, 40)
MUTED = (89, 103, 104)
CORAL = (239, 91, 67)
TEAL = (23, 127, 119)


def font(size, bold=False):
    choices = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in choices:
        if Path(path).exists():
            return ImageFont.truetype(path, size, index=1 if bold and path.endswith(".ttc") else 0)
    return ImageFont.load_default()


F12, F16, F20 = font(12), font(16), font(20)
F28, F40, F66 = font(28, True), font(40, True), font(66, True)


def clamp(x):
    return max(0, min(1, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def rgba(c, a=255):
    return (*c, int(255 * clamp(a)))


def text(d, x, y, value, ft, color, alpha=1, anchor=None):
    d.text((x, y), value, font=ft, fill=rgba(color, alpha), anchor=anchor)


def render(t, facts):
    frame = Image.new("RGBA", SIZE, (*BG, 255))
    d = ImageDraw.Draw(frame)
    # Editorial grid and an abstract living signal: no geographic or statistical meaning.
    for x in range(40, 961, 48):
        d.line((x, 70, x, 492), fill=(36, 64, 64, 13), width=1)
    for y in range(70, 493, 48):
        d.line((40, y, 920, y), fill=(36, 64, 64, 13), width=1)
    cx, cy = (694, 266)
    for i in range(5):
        rad = 58 + i * 40 + 9 * math.sin(t * 1.7 - i * .65)
        d.ellipse((cx-rad, cy-rad, cx+rad, cy+rad), outline=rgba(TEAL, .08 + .05*(i%2)), width=2)
    for i in range(17):
        a = i * 2.399 + t * (.45 + i%3*.09)
        r = 55 + ((i*33)%155)
        x, y = cx + math.cos(a)*r, cy + math.sin(a)*r
        size = 3 + i%3
        d.ellipse((x-size, y-size, x+size, y+size), fill=rgba(CORAL if i%4==0 else TEAL, .35+i%4*.12))
    d.ellipse((cx-13, cy-13, cx+13, cy+13), fill=rgba(CORAL, .93))
    d.ellipse((cx-5, cy-5, cx+5, cy+5), fill=rgba(BG, 1))
    d.line((40, 64, 920, 64), fill=rgba(INK, .17), width=1)
    d.line((40, 493, 920, 493), fill=rgba(INK, .17), width=1)
    text(d, 41, 27, facts["name"]["display"], F16, INK)
    text(d, 919, 29, "FICTIONAL DEMO  /  " + facts["period"]["display"], F12, MUTED, anchor="ra")
    d.rectangle((40, 492, 40+int(880*t/DURATION), 495), fill=rgba(CORAL, .95))
    text(d, 41, 507, "SOURCE  /  brief.docx", F12, MUTED)
    text(d, 919, 507, "SYNTHETIC TEST DATA", F12, MUTED, anchor="ra")
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    intro = 1-ease((t-2.55)/.55)
    if intro:
        x = 48 - 30*(1-ease(t/.7))
        text(d, x, 134, facts["identity"]["display"], F16, TEAL, intro)
        text(d, x-4, 175, "FROM SIGNAL", F66, INK, intro)
        text(d, x-4, 254, "TO ACTION.", F66, INK, intro)
        d.rectangle((x, 360, x+int(290*ease(t/1.1)), 364), fill=rgba(CORAL, intro))
        text(d, x, 389, facts["workflow"]["display"], F16, MUTED, intro)

    flow = ease((t-2.25)/.55) * (1-ease((t-5.1)/.6))
    if flow:
        text(d, 49, 132, "A CLEARER RESPONSE LOOP", F16, TEAL, flow)
        labels = ["SIGNALS", "TRIAGE", "RESPONSE"]
        for i, label in enumerate(labels):
            local = ease((t-2.65-i*.4)/.42)*flow
            if not local:
                continue
            x = 53+i*225
            y = 255-25*(1-local)
            d.rounded_rectangle((x,y,x+177,y+89), radius=12, fill=rgba(INK, local))
            d.ellipse((x+17,y+20,x+33,y+36), fill=rgba(CORAL if i==2 else BG, local))
            text(d, x+19, y+51, label, F20, BG, local)
            if i<2:
                d.line((x+181,y+44,x+218,y+44), fill=rgba(CORAL, local), width=3)
                d.polygon([(x+218,y+44),(x+209,y+38),(x+209,y+50)], fill=rgba(CORAL, local))
        text(d, 54, 379, facts["workflow"]["display"], F16, MUTED, flow)

    board = ease((t-4.95)/.65)
    if board:
        # A real dashboard composition with source-exact values and labels.
        d.rounded_rectangle((36, 82, 923, 465), radius=19, fill=rgba((255,255,252), board),
                            outline=rgba(INK, .13*board), width=2)
        text(d, 59, 105, "PULSE OVERVIEW", F16, TEAL, board)
        text(d, 59, 138, facts["identity"]["display"], F28, INK, board)
        d.line((59, 190, 897, 190), fill=rgba(INK, .13*board), width=1)
        cards = [
            ("events_label", "events"),
            ("tagging_label", "tagging"),
            ("response_label", "response"),
        ]
        for i, (label_id, fid) in enumerate(cards):
            local = ease((t-5.55-i*.28)/.52)*board
            if not local:
                continue
            x = 59+i*281
            y = 218+20*(1-local)
            d.rounded_rectangle((x,y,x+260,y+184), radius=12,
                                fill=rgba((248,247,242), local), outline=rgba(INK, .13*local))
            d.rectangle((x+16,y+18,x+38,y+22), fill=rgba(CORAL if i==1 else TEAL, local))
            text(d,x+17,y+40,facts[label_id]["display"],F16,MUTED,local)
            text(d,x+14,y+75,facts[fid]["display"],F40,INK,local)
            d.line((x+17,y+145,x+241,y+145), fill=rgba(INK,.12*local),width=1)
            text(d,x+17,y+155,facts["period"]["display"],F16,MUTED,local)
        text(d, 59, 428, "SOURCE-BOUND VALUES  /  FICTIONAL BRIEF", F12, MUTED, board)
    return Image.alpha_composite(frame, layer).convert("RGB")
