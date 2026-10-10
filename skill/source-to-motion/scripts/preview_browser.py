#!/usr/bin/env python3
"""Capture three independent frames before spending time on a full browser render."""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

from render import fact_map


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scene", type=Path, required=True)
    p.add_argument("--facts", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--times", nargs="*", type=float)
    a = p.parse_args()
    facts = fact_map(a.facts)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
            page.goto(a.scene.resolve().as_uri(), wait_until="load", timeout=30000)
            page.wait_for_function("window.SCENE && window.SCENE.ready === true", timeout=30000)
            duration = float(page.evaluate("SCENE.duration"))
            times = a.times or [0, duration * .48, duration * .92]
            page.evaluate("facts => { window.__sourceFacts = facts }", facts)
            canvas = page.locator("canvas#frame")
            images = []
            for t in times:
                page.evaluate("t => SCENE.render(t, window.__sourceFacts)", t)
                images.append(Image.open(io.BytesIO(canvas.screenshot(type="png"))).convert("RGB"))
            w = 440
            h = round(images[0].height * w / images[0].width)
            contact = Image.new("RGB", (w * len(images), h + 44), (8, 12, 20))
            d = ImageDraw.Draw(contact)
            for i, (t, image) in enumerate(zip(times, images)):
                contact.paste(image.resize((w, h), Image.Resampling.LANCZOS), (i * w, 0))
                d.text((i * w + 12, h + 12), f"{t:.1f}s", fill=(220, 232, 244))
            a.out.parent.mkdir(parents=True, exist_ok=True)
            contact.save(a.out, quality=93)
            print(json.dumps({"contact": str(a.out.resolve()), "times": times}))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
