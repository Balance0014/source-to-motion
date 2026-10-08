#!/usr/bin/env python3
"""Render a deterministic Pillow scene to an H.264 MP4 using local ffmpeg."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image


def load_scene(path: Path):
    spec = importlib.util.spec_from_file_location("source_to_motion_scene", path)
    if not spec or not spec.loader:
        raise ValueError(f"Cannot load scene: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fact_map(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("facts"), list):
        raise ValueError("facts.json must contain a facts array")
    facts = {}
    for item in data["facts"]:
        if not all(item.get(k) for k in ("id", "display", "evidence", "locator")):
            raise ValueError(f"Incomplete fact: {item}")
        if item["id"] in facts:
            raise ValueError(f"Duplicate fact id: {item['id']}")
        facts[item["id"]] = item
    return facts


def render(scene_path: Path, facts_path: Path, output: Path, audio: Path | None, timeout: int):
    if not scene_path.is_file() or not facts_path.is_file():
        raise FileNotFoundError("Scene and facts files are required")
    scene = load_scene(scene_path)
    facts = fact_map(facts_path)
    width, height = tuple(scene.SIZE)
    fps = int(scene.FPS)
    duration = float(scene.DURATION)
    if width < 320 or height < 180 or width * height > 4_147_200:
        raise ValueError("Scene dimensions must be from 320x180 to about 4 megapixels")
    if fps < 12 or fps > 60 or duration <= 0 or duration > 45:
        raise ValueError("Video must be 12–60 fps and at most 45 seconds")
    if not callable(getattr(scene, "render", None)):
        raise ValueError("Scene must define render(t, facts) -> PIL.Image")
    output.parent.mkdir(parents=True, exist_ok=True)
    frames = round(duration * fps)
    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{width}x{height}",
               "-framerate", str(fps), "-i", "-"]
    if audio:
        if not audio.is_file():
            raise FileNotFoundError(audio)
        command += ["-i", str(audio)]
    command += ["-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if audio:
        command += ["-af", "apad", "-c:a", "aac", "-b:a", "160k", "-t", str(duration)]
    command.append(str(output))
    start = time.monotonic()
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for index in range(frames):
            if time.monotonic() - start > timeout:
                raise TimeoutError(f"Render exceeded {timeout} seconds")
            t = index / fps
            frame = scene.render(t, facts)
            if not isinstance(frame, Image.Image) or frame.size != (width, height):
                raise ValueError(f"Frame {index} must be a PIL image of size {(width, height)}")
            process.stdin.write(frame.convert("RGB").tobytes())
        process.stdin.close()
        stderr = process.stderr.read().decode("utf-8", "replace")
        if process.wait(timeout=30):
            raise RuntimeError(f"ffmpeg failed: {stderr[-1200:]}")
    except Exception:
        process.kill()
        process.wait()
        output.unlink(missing_ok=True)
        raise
    finally:
        if process.stderr:
            process.stderr.close()
    print(json.dumps({"output": str(output.resolve()), "frames": frames,
                      "seconds": round(time.monotonic() - start, 2),
                      "size": [width, height], "fps": fps}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scene", type=Path, required=True)
    p.add_argument("--facts", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--audio", type=Path)
    p.add_argument("--timeout", type=int, default=600)
    a = p.parse_args()
    render(a.scene.resolve(), a.facts.resolve(), a.out.resolve(),
           a.audio.resolve() if a.audio else None, a.timeout)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"render failed: {exc}")
