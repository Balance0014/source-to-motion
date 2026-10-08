#!/usr/bin/env python3
"""Create the repository's original vector-style social preview (1280×640 PNG)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "social-preview.png"
SCALE = 2
W, H = 1280 * SCALE, 640 * SCALE


def font(size, bold=False):
    paths = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if Path(path).is_file():
            return ImageFont.truetype(path, size*SCALE, index=1 if bold and path.endswith(".ttc") else 0)
    return ImageFont.load_default()


def box(rect):
    return tuple(round(v*SCALE) for v in rect)


def point(x, y):
    return round(x*SCALE), round(y*SCALE)


def main():
    image = Image.new("RGB", (W, H), (4, 10, 27))
    d = ImageDraw.Draw(image)
    for y in range(H):
        k = y / H
        d.line((0, y, W, y), fill=(int(5+6*k), int(11+7*k), int(29+16*k)))

    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    g = ImageDraw.Draw(glow)
    g.ellipse(box((722,40,1310,660)), fill=(48,79,203,110))
    g.ellipse(box((844,144,1190,500)), fill=(52,211,249,82))
    glow = glow.filter(ImageFilter.GaussianBlur(95*SCALE))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    d = ImageDraw.Draw(image)

    # Source cards flowing into one video frame.
    for i,(short,y) in enumerate((("REPO",175),("PDF",270),("WEB",365))):
        x = 730 - i*16
        d.rounded_rectangle(box((x,y,x+135,y+64)),radius=12*SCALE,
                            fill=(14,31,65,235),outline=(67,103,154,180),width=2*SCALE)
        d.text(point(x+19,y+20),short,font=font(18,True),fill=(169,215,235))
        d.line((point(x+136,y+32),point(900,y+32)),fill=(69,179,220,100),width=2*SCALE)
    d.rounded_rectangle(box((900,112,1210,500)),radius=26*SCALE,
                        fill=(15,31,62,255),outline=(83,150,224,245),width=3*SCALE)
    d.rounded_rectangle(box((923,135,1187,455)),radius=18*SCALE,
                        fill=(8,17,38,255),outline=(45,84,134,255),width=2*SCALE)
    for i in range(7):
        radius = (58+i*21)*SCALE
        cx,cy=1055*SCALE,292*SCALE
        start=int(32+i*44)
        d.arc((cx-radius,cy-radius,cx+radius,cy+radius),start=start,end=start+130,
              fill=(61+min(i*5,40),148+min(i*9,70),237,140),width=3*SCALE)
    d.ellipse(box((1008,245,1102,339)),fill=(27,138,184,255),outline=(142,240,255,255),width=3*SCALE)
    d.polygon([point(1044,266),point(1044,318),point(1083,292)],fill=(238,250,255))
    d.line((point(944,423),point(1167,423)),fill=(46,86,140),width=6*SCALE)
    d.line((point(944,423),point(1095,423)),fill=(98,228,249),width=6*SCALE)
    d.ellipse(box((1088,416,1102,430)),fill=(237,250,255))

    d.rounded_rectangle(box((66,55,312,95)),radius=20*SCALE,
                        fill=(15,46,74),outline=(61,163,196),width=2*SCALE)
    d.text(point(84,63),"OPEN SOURCE SKILL",font=font(16,True),fill=(137,226,242))
    d.text(point(65,167),"SOURCE",font=font(91,True),fill=(243,249,255))
    d.text(point(65,265),"TO MOTION.",font=font(91,True),fill=(103,228,249))
    d.text(point(70,392),"Project links and docs become motion videos",font=font(27),fill=(194,215,230))
    d.text(point(70,431),"with facts you can trace back to the source.",font=font(27),fill=(194,215,230))
    d.line((point(69,511),point(657,511)),fill=(65,116,151),width=2*SCALE)
    d.text(point(70,533),"GITHUB  •  WEBSITE  •  PDF  •  WORD",font=font(17,True),fill=(125,174,200))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").resize((1280,640),Image.Resampling.LANCZOS).save(OUT,optimize=True)
    print(OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
