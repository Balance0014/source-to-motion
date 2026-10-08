"""Original tailscale stress-test visual direction, built on shared motion primitives."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from showcase_engine import SIZE, FPS, DURATION, render as _render

def render(t, facts):
    return _render(t, facts, "tailscale")
