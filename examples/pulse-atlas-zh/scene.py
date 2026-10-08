"""Chinese localization of the fictional Pulse Atlas brief, with editable source-bound type."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (960, 540)
FPS = 24
DURATION = 10.0
ROOT = Path(__file__).resolve().parents[2]
BG = (242, 239, 230)
INK = (21, 34, 40)
MUTED = (87, 102, 104)
CORAL = (238, 88, 67)
TEAL = (20, 124, 116)


def font(size: int, bold: bool = False):
    path = ROOT / "assets" / "fonts" / ("STM-Sans-SC-Bold.ttf" if bold else "STM-Sans-SC-Regular.ttf")
    if not path.is_file():
        raise FileNotFoundError(f"The example needs its bundled OFL font: {path}")
    return ImageFont.truetype(str(path), size)


F12, F16, F20 = font(12), font(16), font(20)
F25, F31, F42, F66 = font(25, True), font(31, True), font(42, True), font(66, True)


def clamp(x):
    return max(0, min(1, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def rgba(c, a=1):
    return (*c, int(255 * clamp(a)))


def label(d, x, y, value, ft, color, alpha=1, anchor=None):
    d.text((x, y), value, font=ft, fill=rgba(color, alpha), anchor=anchor)


def render(t, facts):
    base = Image.new("RGBA", SIZE, (*BG, 255))
    d = ImageDraw.Draw(base)
    for x in range(40, 961, 48):
        d.line((x, 70, x, 492), fill=rgba(INK, .055), width=1)
    for y in range(70, 493, 48):
        d.line((40, y, 920, y), fill=rgba(INK, .055), width=1)
    cx, cy = 698, 265
    for i in range(5):
        r = 61 + i*39 + 8*math.sin(t*1.55-i*.62)
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=rgba(TEAL,.13),width=2)
    for i in range(23):
        a = i*2.399 + t*(.42+i%4*.06)
        r = 47 + i*31%166
        x,y = cx+math.cos(a)*r, cy+math.sin(a)*r
        radius = 2+i%3
        d.ellipse((x-radius,y-radius,x+radius,y+radius),
                  fill=rgba(CORAL if i%5==0 else TEAL,.45+i%3*.12))
    core = 10 + 3*math.sin(t*2.8)
    d.ellipse((cx-core,cy-core,cx+core,cy+core),fill=rgba(CORAL,.94))
    d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=rgba(BG))
    d.line((40,64,920,64),fill=rgba(INK,.17))
    d.line((40,493,920,493),fill=rgba(INK,.17))
    d.rectangle((40,492,40+int(880*t/DURATION),495),fill=rgba(CORAL,.95))
    label(d,41,25,facts["name"]["display"],F16,INK)
    label(d,918,24,facts["demo"]["display"]+"  /  "+facts["period"]["display"],F16,MUTED,anchor="ra")
    label(d,41,508,"资料来源 / brief.docx",F12,MUTED)
    label(d,919,508,"数据均为虚构示例",F12,MUTED,anchor="ra")

    layer = Image.new("RGBA", SIZE, (0,0,0,0))
    d = ImageDraw.Draw(layer)
    intro = 1-ease((t-2.55)/.55)
    if intro:
        x = 48-30*(1-ease(t/.7))
        label(d,x,131,facts["identity"]["display"],F20,TEAL,intro)
        parts = facts["story"]["display"].split("，")
        label(d,x-3,183,parts[0],F66,INK,intro)
        label(d,x-3,270,parts[1],F66,INK,intro)
        d.rectangle((x,368,x+int(285*ease(t/1.1)),372),fill=rgba(CORAL,intro))
        label(d,x,394,facts["workflow"]["display"],F20,MUTED,intro)

    flow = ease((t-2.28)/.53)*(1-ease((t-5.05)/.6))
    if flow:
        label(d,49,130,facts["identity"]["display"],F20,TEAL,flow)
        words = facts["workflow"]["display"].split(" → ")
        for i, word in enumerate(words):
            local = ease((t-2.65-i*.4)/.42)*flow
            if not local:
                continue
            x = 52+i*228
            y = 256-22*(1-local)
            d.rounded_rectangle((x,y,x+181,y+90),radius=12,fill=rgba(INK,local))
            d.ellipse((x+18,y+20,x+34,y+36),fill=rgba(CORAL if i==2 else BG,local))
            label(d,x+19,y+46,word,F25,BG,local)
            if i<2:
                d.line((x+184,y+45,x+221,y+45),fill=rgba(CORAL,local),width=3)
                d.polygon([(x+221,y+45),(x+211,y+39),(x+211,y+51)],fill=rgba(CORAL,local))
        label(d,54,381,facts["workflow"]["display"],F20,MUTED,flow)

    board = ease((t-4.95)/.65)
    if board:
        d.rounded_rectangle((36,82,923,465),radius=19,fill=rgba((255,255,252),board),
                            outline=rgba(INK,.12*board),width=2)
        label(d,58,105,facts["name"]["display"],F16,TEAL,board)
        label(d,58,135,facts["identity"]["display"],F31,INK,board)
        d.line((59,190,897,190),fill=rgba(INK,.13*board))
        cards = [("events_label","events"),("tagging_label","tagging"),("response_label","response")]
        for i,(label_id,value_id) in enumerate(cards):
            local=ease((t-5.56-i*.28)/.52)*board
            if not local:
                continue
            x,y=59+i*281,218+21*(1-local)
            d.rounded_rectangle((x,y,x+260,y+184),radius=12,
                                fill=rgba((248,247,242),local),outline=rgba(INK,.12*local))
            d.rectangle((x+17,y+18,x+40,y+22),fill=rgba(CORAL if i==1 else TEAL,local))
            label(d,x+17,y+39,facts[label_id]["display"],F20,MUTED,local)
            label(d,x+15,y+77,facts[value_id]["display"],F42,INK,local)
            d.line((x+17,y+145,x+242,y+145),fill=rgba(INK,.12*local))
            label(d,x+17,y+155,facts["period"]["display"],F16,MUTED,local)
        label(d,59,427,facts["demo"]["display"]+"  /  数字对照原始简报",F16,MUTED,board)
    return Image.alpha_composite(base,layer).convert("RGB")
