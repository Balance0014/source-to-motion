#!/usr/bin/env python3
"""Build the repository's social preview from frames of its published films."""

from __future__ import annotations

import io
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "social-preview.jpg"
W, H = 1280, 640


def ffmpeg_executable() -> str:
    if executable := shutil.which("ffmpeg"):
        return executable
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise SystemExit("FFmpeg is required to extract the film frames") from exc


def film_frame(name: str, seconds: float) -> Image.Image:
    video = ROOT / "examples" / "director-tests" / name / "preview.mp4"
    result = subprocess.run(
        [
            ffmpeg_executable(), "-hide_banner", "-loglevel", "error",
            "-ss", str(seconds), "-i", str(video), "-frames:v", "1",
            "-f", "image2pipe", "-vcodec", "mjpeg", "pipe:1",
        ],
        capture_output=True,
        check=True,
        timeout=25,
    )
    return Image.open(io.BytesIO(result.stdout)).convert("RGB")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    face = ImageFont.truetype(ROOT / "assets" / "fonts" / "SpaceGrotesk-Variable.ttf", size)
    if bold:
        face.set_variation_by_name("Bold")
    return face


def paste_wedge(canvas: Image.Image, frame: Image.Image, polygon: list[tuple[int, int]], left: int, right: int) -> None:
    # Each wedge uses a frame from a different finished video, never invented artwork.
    frame = frame.crop((0, int(frame.height * 0.12), frame.width, int(frame.height * 0.86)))
    art = ImageOps.fit(frame, (right - left, H), centering=(0.5, 0.42))
    plate = Image.new("RGB", (W, H))
    plate.paste(art, (left, 0))
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    canvas.paste(plate, (0, 0), mask)


def main() -> None:
    canvas = Image.new("RGB", (W, H), "#030916")
    paste_wedge(canvas, film_frame("uv", 10), [(0, 0), (492, 0), (357, H), (0, H)], 0, 500)
    paste_wedge(canvas, film_frame("gapmine", 9), [(492, 0), (927, 0), (795, H), (357, H)], 350, 930)
    paste_wedge(canvas, film_frame("tailscale", 8), [(927, 0), (W, 0), (W, H), (795, H)], 790, W)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = overlay.load()
    for y in range(H):
        # Let the finished artwork dominate, then give the wordmark a readable base.
        bottom = max(0, min(250, int((y - 340) / 95 * 250)))
        top = max(0, min(250, int((165 - y) / 60 * 250)))
        for x in range(W):
            pixels[x, y] = (1, 5, 13, max(bottom, top))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    d = ImageDraw.Draw(canvas)

    d.text((68, 52), "OPEN SOURCE AGENT SKILL", font=font(22, True), fill="#D9F7FF")
    d.line((68, 91, 307, 91), fill="#5DD9E9", width=3)
    d.text((65, 443), "SOURCE TO MOTION", font=font(96, True), fill="#F7FAFF", stroke_width=1, stroke_fill="#182132")
    d.text((70, 565), "PROJECT LINKS & DOCUMENTS  →  ORIGINAL MOTION FILMS", font=font(24, True), fill="#CDE2EF")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT, quality=88, optimize=True, progressive=True, subsampling=0)
    if OUT.stat().st_size >= 1_000_000:
        raise SystemExit(f"Social preview must be under 1 MB: {OUT.stat().st_size} bytes")
    print(OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
