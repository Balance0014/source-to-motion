#!/usr/bin/env python3
"""Verify evidence bindings and media integrity; make a visual contact sheet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def numbers(text: str) -> list[str]:
    tokens = re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?", text)
    return [token.replace(",", "") for token in tokens]


def verify_facts(facts_path: Path, source_path: Path | None):
    data = json.loads(facts_path.read_text(encoding="utf-8"))
    facts = data.get("facts", [])
    if not facts:
        raise ValueError("At least one source-backed fact is required")
    source = json.loads(source_path.read_text(encoding="utf-8"))["text"] if source_path else None
    ids = set()
    for fact in facts:
        fid = fact.get("id")
        if not fid or fid in ids:
            raise ValueError(f"Missing or duplicate fact id: {fid}")
        ids.add(fid)
        quote, display, locator = (fact.get(k, "") for k in ("evidence", "display", "locator"))
        if not quote or not display or not locator:
            raise ValueError(f"Fact {fid} needs evidence, display, and locator")
        if source and normalized(quote) not in normalized(source):
            raise ValueError(f"Fact {fid} evidence was not found in extracted source")
        quoted = set(numbers(quote))
        displayed = set(numbers(display))
        if displayed and not displayed.issubset(quoted):
            raise ValueError(f"Fact {fid} displays numbers absent from its evidence: {displayed - quoted}")
    return len(facts)


def video_details(path: Path):
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path)], capture_output=True, text=True, timeout=15)
    log = proc.stderr
    d = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", log)
    size = re.search(r"Video:.*?(\d{3,4})x(\d{3,4})", log)
    fps = re.search(r"Video:.*?(\d+(?:\.\d+)?) fps", log)
    if not (d and size and fps):
        raise ValueError(f"Video metadata unreadable: {log[-700:]}")
    duration = int(d[1])*3600 + int(d[2])*60 + float(d[3])
    return {"duration": duration, "width": int(size[1]), "height": int(size[2]),
            "fps": float(fps[1]), "audio": "Audio:" in log}


def contact_sheet(video: Path, output: Path, duration: float):
    with tempfile.TemporaryDirectory(prefix="stm-check-") as tmp:
        pattern = str(Path(tmp) / "frame-%02d.jpg")
        fps = min(1.5, 9 / duration)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
                        "-vf", f"fps={fps},scale=480:-1", "-frames:v", "12", pattern], check=True, timeout=45)
        files = sorted(Path(tmp).glob("frame-*.jpg"))
        if not files:
            raise ValueError("Could not extract frames")
        with Image.open(files[0]) as thumb:
            tw, th = thumb.size
        columns = 3
        rows = (len(files)+columns-1)//columns
        sheet = Image.new("RGB", (columns*tw, rows*(th+28)), (11, 15, 31))
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.load_default()
        for i, file in enumerate(files):
            x, y = (i%columns)*tw, (i//columns)*(th+28)
            with Image.open(file) as frame:
                sheet.paste(frame, (x, y))
            draw.text((x+7, y+th+7), f"frame {i+1} / {len(files)}", fill=(185, 205, 226), font=font)
        output.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(output, quality=90)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--facts", type=Path, required=True)
    p.add_argument("--source-json", type=Path, required=True)
    p.add_argument("--contact-sheet", type=Path, required=True)
    a = p.parse_args()
    count = verify_facts(a.facts, a.source_json)
    details = video_details(a.video)
    if not 1 <= details["duration"] <= 45:
        raise ValueError("Video duration is outside the short-form range")
    if details["width"] < 640 or details["height"] < 360:
        raise ValueError("Video resolution is too small")
    contact_sheet(a.video, a.contact_sheet, details["duration"])
    print(json.dumps({"facts_checked": count, "video": details,
                      "contact_sheet": str(a.contact_sheet.resolve())}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"verify failed: {exc}")
