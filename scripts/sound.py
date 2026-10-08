#!/usr/bin/env python3
"""Generate a modest original electronic bed with optional transition cues."""

import argparse
import math
import wave
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--duration", required=True, type=float)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--bpm", type=float, default=100)
    p.add_argument("--cue", action="append", type=float, default=[])
    a = p.parse_args()
    if not 1 <= a.duration <= 45 or not 50 <= a.bpm <= 180:
        raise SystemExit("duration must be 1–45 s and BPM 50–180")
    sr = 48000
    n = round(sr * a.duration)
    beat_seconds = 60 / a.bpm
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(a.out), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        chunk = bytearray()
        for i in range(n):
            t = i / sr
            fade = min(1, t / .35, (a.duration - t) / .55)
            pad = .045 * math.sin(2*math.pi*55*t) + .025 * math.sin(2*math.pi*110*t)
            phase = t % beat_seconds
            beat = .11 * math.sin(2*math.pi*(95-30*phase)*phase) * math.exp(-24*phase)
            cue = 0.0
            for when in a.cue:
                u = t - when
                if 0 <= u < .45:
                    cue += .075 * math.sin(2*math.pi*(520-280*u)*u) * math.exp(-8*u)
            sample = max(-1, min(1, (pad + beat + cue) * 2.2 * fade))
            chunk += int(sample * 32767).to_bytes(2, "little", signed=True)
            if len(chunk) >= 65536:
                wav.writeframes(chunk)
                chunk.clear()
        if chunk:
            wav.writeframes(chunk)
    print(a.out.resolve())


if __name__ == "__main__":
    main()
