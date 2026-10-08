"""Original cinematic uv example. Background plate is generated art; factual text is drawn from facts.json."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = (960, 540)
FPS = 24
DURATION = 11.5

ROOT = Path(__file__).resolve().parents[2]
PLATE = Image.open(ROOT / "assets" / "uv_energy.png").convert("RGB")
PLATE = PLATE.resize((1030, 580), Image.Resampling.LANCZOS)
WHITE = (237, 246, 255)
MUTED = (156, 187, 219)
BLUE = (99, 227, 255)
VIOLET = (187, 139, 255)


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Avenir Next.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size, index=1 if bold and candidate.endswith(".ttc") else 0)
    return ImageFont.load_default()


F12 = font(12)
F16 = font(16)
F22 = font(22)
F32 = font(32, True)
F58 = font(58, True)
F84 = font(84, True)
F120 = font(120, True)


def clamp(v):
    return max(0.0, min(1.0, v))


def smooth(v):
    v = clamp(v)
    return v * v * (3 - 2 * v)


def window(t, start, end, fade=0.45):
    return smooth((t - start) / fade) * smooth((end - t) / fade)


def txt(layer, pos, value, ft, color, alpha=255, anchor=None):
    d = ImageDraw.Draw(layer)
    d.text(pos, value, font=ft, fill=(*color, int(255 * clamp(alpha / 255))), anchor=anchor)


def line(layer, coords, fill, width=1):
    ImageDraw.Draw(layer).line(coords, fill=fill, width=width)


def render(t, facts):
    # The plate moves slowly, while the particles, gauges, nodes and type animate independently.
    drift = int(12 * math.sin(t * 0.34))
    zoom = 1 + 0.025 * math.sin(t * 0.25)
    w, h = int(PLATE.width * zoom), int(PLATE.height * zoom)
    bg = PLATE.resize((w, h), Image.Resampling.BILINEAR)
    frame = bg.crop(((w - 960) // 2 + drift, (h - 540) // 2, (w + 960) // 2 + drift, (h + 540) // 2))
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(0, 760, 8):
        a = int(218 * (1 - x / 760) ** 1.6)
        sd.rectangle((x, 0, x + 8, 540), fill=(3, 8, 24, a))
    sd.rectangle((0, 0, 960, 540), fill=(2, 5, 15, 25))
    frame = Image.alpha_composite(frame.convert("RGBA"), shade)
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Purposeful motion around the energy core, not a static image pan.
    for i in range(42):
        angle = i * 2.39996 + t * (0.52 + (i % 5) * 0.055)
        radius = 74 + (i * 43 % 290) + 8 * math.sin(t * 0.8 + i)
        x = 604 + math.cos(angle) * radius * 1.12
        y = 261 + math.sin(angle) * radius * 0.53
        r = 1 + (i % 4 == 0)
        opacity = int(42 + 95 * (0.5 + 0.5 * math.sin(t * 1.5 + i)))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*BLUE, opacity))
    for i in range(4):
        radius = 82 + i * 38 + 7 * math.sin(t * 1.8 - i)
        opacity = int(35 + 20 * math.sin(t + i) ** 2)
        draw.arc((604-radius*1.38, 261-radius*.75, 604+radius*1.38, 261+radius*.75),
                 start=int((t * 28 + i * 88) % 360), end=int((t * 28 + i * 88 + 94) % 360),
                 fill=(*BLUE, opacity), width=2)

    # Minimal fixed HUD furniture grounds every beat.
    txt(overlay, (45, 31), "ASTRAL  /  UV", F16, WHITE, 220)
    txt(overlay, (914, 33), "SOURCE  /  ASTRAL", F12, MUTED, 190, anchor="ra")
    line(overlay, [(46, 62), (914, 62)], (*BLUE, 70))
    line(overlay, [(46, 479), (914, 479)], (*BLUE, 70))
    progress = int(868 * clamp(t / DURATION))
    draw.rectangle((46, 478, 46 + progress, 481), fill=(*BLUE, 180))
    txt(overlay, (46, 499), "SOURCE  github.com/astral-sh/uv  /  README", F12, MUTED, 170)

    a = window(t, 0, 3.35, .5)
    if a > 0:
        x = 48 + int((1 - smooth(t / .65)) * -35)
        txt(overlay, (x, 138), "A NEW VELOCITY FOR PYTHON", F16, BLUE, int(210*a))
        txt(overlay, (x - 4, 171), "uv", F120, WHITE, int(255*a))
        txt(overlay, (x, 310), facts["identity"]["display"], F22, WHITE, int(245*a))
        txt(overlay, (x, 345), facts["rust"]["display"], F16, MUTED, int(210*a))
        line(overlay, [(x, 384), (x + int(224*smooth(t/.9)), 384)], (*BLUE, int(190*a)), 2)

    b = window(t, 2.7, 7.1, .55)
    if b > 0:
        txt(overlay, (48, 120), "01 / CONSOLIDATE", F16, BLUE, int(225*b))
        txt(overlay, (45, 157), facts["single_tool"]["display"], F58, WHITE, int(255*b))
        txt(overlay, (49, 239), facts["scope"]["display"], F22, WHITE, int(230*b))
        labels = [facts["package_manager"]["display"], facts["project_manager"]["display"], facts["python_versions"]["display"]]
        for i, label in enumerate(labels):
            local = smooth((t - 3.25 - i * .26) / .48) * b
            if local <= 0:
                continue
            y = 302 + i * 42
            width = int(360 * local)
            draw.rounded_rectangle((49, y, 49+width, y+32), radius=7,
                                   fill=(8, 21, 46, int(185*local)), outline=(*BLUE, int(75*local)))
            txt(overlay, (62, y+7), label, F16, WHITE, int(230*local))
            draw.ellipse((387, y+12, 393, y+18), fill=(*BLUE, int(220*local)))
        # Thin data paths converge into the core.
        phase = (t - 3) * 1.6
        for i in range(3):
            y0 = 316 + i * 42
            x2 = 600 + 28 * math.sin(phase + i)
            line(overlay, [(403, y0), (481, y0), (x2, 261)], (*BLUE, int(65*b)), 2)
            q = (phase + i*.28) % 1
            px = 403 + (x2-403)*q
            py = y0 + (261-y0)*max(0, (q-.4)/.6)
            draw.ellipse((px-3, py-3, px+3, py+3), fill=(*WHITE, int(180*b)))

    c = window(t, 6.55, 12.2, .6)
    if c > 0:
        txt(overlay, (48, 115), "02 / PERFORMANCE", F16, BLUE, int(220*c))
        txt(overlay, (43, 155), facts["speed"]["display"], F84, WHITE, int(255*c))
        txt(overlay, (49, 267), facts["speed_comparison"]["display"], F32, WHITE, int(235*c))
        txt(overlay, (49, 317), "As stated in the uv README", F16, MUTED, int(210*c))
        draw.rounded_rectangle((48, 379, 439, 430), radius=9,
                               fill=(6, 15, 34, int(175*c)), outline=(*BLUE, int(80*c)))
        txt(overlay, (63, 396), "EVIDENCE  /  README → BENCHMARKS", F16, BLUE, int(235*c))
        scan_x = 605 + 120 * math.sin(t*2.5)
        draw.line((scan_x, 118, scan_x+28, 406), fill=(*VIOLET, int(40*c)), width=2)

    # Upper corner values are scene/time identifiers, never invented product metrics.
    frame = Image.alpha_composite(frame, overlay)
    return frame.convert("RGB")
