#!/usr/bin/env python3
"""Render a deterministic local HTML canvas scene to H.264 with Playwright.

The HTML file owns art direction. This driver owns only capture and encoding.
No remote page or hosted rendering service is involved.
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from render import fact_map


def render(scene: Path, facts_path: Path, output: Path, audio: Path | None,
           timeout: int, frames_limit: int | None = None) -> dict:
    if not scene.is_file() or not facts_path.is_file():
        raise FileNotFoundError("Scene and facts files are required")
    facts = fact_map(facts_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    ffmpeg = None
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=[
            "--allow-file-access-from-files", "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
        ])
        try:
            page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
            page.goto(scene.resolve().as_uri(), wait_until="load", timeout=30000)
            page.wait_for_function("window.SCENE && window.SCENE.ready === true", timeout=30000)
            info = page.evaluate("() => ({width: SCENE.width, height: SCENE.height, fps: SCENE.fps, duration: SCENE.duration})")
            width, height = int(info["width"]), int(info["height"])
            fps, duration = int(info["fps"]), float(info["duration"])
            if width < 320 or height < 180 or width * height > 4_147_200:
                raise ValueError("Canvas size must be 320x180 to about 4 megapixels")
            if fps < 12 or fps > 60 or duration <= 0 or duration > 45:
                raise ValueError("Video must be 12–60 fps and at most 45 seconds")
            page.set_viewport_size({"width": width, "height": height})
            canvas = page.locator("canvas#frame")
            if canvas.count() != 1:
                raise ValueError("Scene must contain one canvas#frame")
            if canvas.evaluate("el => [el.width, el.height]") != [width, height]:
                raise ValueError("Canvas pixel dimensions must match SCENE dimensions")
            page.evaluate("facts => { window.__sourceFacts = facts }", facts)
            command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                       "-f", "image2pipe", "-framerate", str(fps), "-vcodec", "mjpeg", "-i", "-"]
            if audio:
                if not audio.is_file():
                    raise FileNotFoundError(audio)
                command += ["-i", str(audio)]
            command += ["-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
            if audio:
                command += ["-af", "apad", "-c:a", "aac", "-b:a", "160k"]
            command += ["-t", str(duration if frames_limit is None else min(duration, frames_limit / fps)), str(output)]
            ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            frames = min(round(duration * fps), frames_limit or round(duration * fps))
            for index in range(frames):
                if time.monotonic() - started > timeout:
                    raise TimeoutError(f"Render exceeded {timeout} seconds")
                page.evaluate("t => SCENE.render(t, window.__sourceFacts)", index / fps)
                data_url = page.evaluate("() => document.querySelector('canvas#frame').toDataURL('image/jpeg', .94)")
                ffmpeg.stdin.write(base64.b64decode(data_url.split(',', 1)[1]))
            ffmpeg.stdin.close()
            stderr = ffmpeg.stderr.read().decode("utf-8", "replace")
            if ffmpeg.wait(timeout=30):
                raise RuntimeError(f"ffmpeg failed: {stderr[-1200:]}")
            return {"output": str(output.resolve()), "frames": frames,
                    "seconds": round(time.monotonic() - started, 2), "size": [width, height], "fps": fps}
        except Exception:
            if ffmpeg and ffmpeg.poll() is None:
                ffmpeg.kill()
                ffmpeg.wait()
            output.unlink(missing_ok=True)
            raise
        finally:
            if ffmpeg and ffmpeg.stderr:
                ffmpeg.stderr.close()
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", type=Path, required=True)
    parser.add_argument("--facts", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--frames", type=int, help="Short development render; omit for full video")
    args = parser.parse_args()
    result = render(args.scene, args.facts, args.out, args.audio, args.timeout, args.frames)
    print(json.dumps(result))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"browser render failed: {exc}")
