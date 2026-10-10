#!/usr/bin/env python3
"""Keep the small installable skill in sync with the repository runtime.

The case-study videos stay outside skill/source-to-motion so the skills CLI
installs only the tools and instructions a new user needs.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skill" / "source-to-motion"
RUNTIME = (
    "LICENSE",
    "requirements.txt",
    "requirements-browser.txt",
    "agents/openai.yaml",
    "scripts/canvas_core.js",
    "scripts/ingest.py",
    "scripts/preview_browser.py",
    "scripts/render.py",
    "scripts/render_browser.py",
    "scripts/sound.py",
    "scripts/verify.py",
    "references/art-direction.md",
    "references/localization.md",
    "references/scene-contract.md",
    "references/source-and-facts.md",
    "assets/fonts/OFL.txt",
    "assets/fonts/README.md",
    "assets/fonts/STM-Sans-SC-Bold.ttf",
    "assets/fonts/STM-Sans-SC-Regular.ttf",
    "assets/fonts/SpaceGrotesk-OFL.txt",
    "assets/fonts/SpaceGrotesk-Variable.ttf",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the package differs from the runtime")
    args = parser.parse_args()
    if not (PACKAGE / "SKILL.md").is_file():
        raise SystemExit("The canonical skill/source-to-motion/SKILL.md is missing")
    expected = {Path(name) for name in RUNTIME}
    actual = {p.relative_to(PACKAGE) for p in PACKAGE.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    extras = actual - expected - {Path("SKILL.md"), Path("README.md")}
    if extras:
        raise SystemExit("Unexpected files in installable skill: " + ", ".join(map(str, sorted(extras))))
    stale = []
    for rel in sorted(expected):
        src, dst = ROOT / rel, PACKAGE / rel
        if not src.is_file():
            raise SystemExit(f"Runtime source is missing: {src}")
        if args.check:
            if not dst.is_file() or src.read_bytes() != dst.read_bytes():
                stale.append(str(rel))
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    if stale:
        raise SystemExit("Installable skill is stale: " + ", ".join(stale))
    print(f"{'Checked' if args.check else 'Synced'} {len(expected)} runtime files in {PACKAGE}")


if __name__ == "__main__":
    main()
