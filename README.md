# Source to Motion

**English** · [简体中文](README.zh-CN.md)

**Turn a project link or document into a short, original motion video. Keep the numbers honest.**

[![GapMine cinematic signal-field video poster](media/gapmine-poster.jpg)](examples/gapmine/preview.mp4)

[Watch GapMine](examples/gapmine/preview.mp4) · [Six GitHub stress-test films](examples/SHOWCASE.md) · [看中文仪表盘](examples/pulse-atlas-zh/preview.mp4)

[![Six source-specific GitHub concept films](media/showcase-grid.jpg)](examples/SHOWCASE.md)

Source to Motion is an open-source **agent skill**, not a hosted video service. Give your coding agent a GitHub repo, product site, PDF, Word document, or brief. The agent reads the source, chooses a visual concept, writes an editable animation, renders the MP4 locally, and records displayed facts against source excerpts.

It provides a repeatable production workflow, source extraction, a fact manifest, a local Pillow/FFmpeg renderer, procedural audio, and a verification script. The finished style is designed for each source. The GapMine film demonstrates spatial, cinematic direction; the English and Chinese dashboard videos show how to localize wording while preserving the same numeric evidence.

## Try it with Codex

Requirements: Python 3.10+, FFmpeg on your `PATH`, and a coding agent able to run local Python. Optional image generation uses **your own** agent/tool access. The scripts themselves make no model API calls and need no API key.

The [skills CLI](https://www.skills.sh/docs/cli) detects this repository's skill. To install the skill into Codex:

```bash
npx skills add Balance0014/source-to-motion -g -a codex -y
```

Then install the Python requirements from the installed skill directory shown by the CLI. If you prefer a direct clone with a known path, use:

```bash
git clone https://github.com/Balance0014/source-to-motion.git ~/.codex/skills/source-to-motion
python3 -m pip install -r ~/.codex/skills/source-to-motion/requirements.txt
ffmpeg -version
```

Open a new Codex chat and say:

> Use $source-to-motion to make a 12-second cinematic video from https://github.com/astral-sh/uv. Use source-backed wording and numbers. Deliver the MP4 and editable project.

To make a Chinese video from an English source, state the output language explicitly:

> Use $source-to-motion to turn this English product brief into a 10-second Chinese motion video. Keep the original evidence quotes and verify every translated metric.

You can replace the link with a product page, local PDF, Word file, or a brief. The user chooses the output language; if none is given, the skill follows the source language. For formats the extractor cannot read directly, the agent can use its native file/vision tools and continue through the same fact and render workflow. A source that cannot be read cannot yield verified claims.

## What makes this useful

| Included | What it does |
| --- | --- |
| `SKILL.md` | Directs the agent from source to video, with a quality gate. |
| `scripts/ingest.py` | Extracts bounded text from GitHub, websites, PDF, DOCX, text files, and OCR images when Tesseract is available. |
| `facts.json` convention | Binds on-screen claims and numbers to exact source excerpts and locators. |
| `scripts/render.py` | Turns a source-specific Pillow scene into a shareable H.264 MP4 using local FFmpeg. |
| `scripts/sound.py` | Makes an original, optional electronic audio bed without a music subscription. |
| `scripts/verify.py` | Rejects missing evidence or new numbers, checks video metadata, and creates a contact sheet. |
| Nine editable videos | GapMine, six different GitHub projects, and English and Chinese Word dashboards. |

The verifier is a guardrail, not a fact-checking oracle. It finds exact excerpts and catches numeric additions; the agent still needs to check meaning, units, attribution, legibility, pacing, and the actual video. A publisher's benchmark is labeled as that publisher's claim.

## Examples

| Input | Visual idea | Source-checked content |
| --- | --- | --- |
| [GapMine public website](https://gapmine.com/) | Real builder discussions fly into a five-signal scoring structure; a source-linked example opportunity emerges | Homepage snapshot: **101,081** builder signals analyzed, **1,140** opportunity cards, **124** communities; [evidence](examples/gapmine/facts.json) |
| [uv GitHub repository](https://github.com/astral-sh/uv) | Package paths lock into a kinetic build core | Python package/project manager; Astral's qualified **10–100×** comparison to pip |
| [Ollama GitHub repository](https://github.com/ollama/ollama) | Open-model input lights an inference chamber | Open models, model chat, REST API |
| [Trivy GitHub repository](https://github.com/aquasecurity/trivy) | A scan plane exposes an artifact's security layers | Container images, CVEs, misconfigurations, secrets; no fictional finding counts |
| [DuckDB GitHub repository](https://github.com/duckdb/duckdb) | A query plane cuts through data columns | SQL queries over CSV/Parquet; no fictional result values |
| [Tailscale GitHub repository](https://github.com/tailscale/tailscale) | Separate device islands become a private mesh | Private WireGuard networks, daemon and CLI |
| [Excalidraw GitHub repository](https://github.com/excalidraw/excalidraw) | A suspended hand-drawn canvas builds a shared diagram | Infinite canvas, collaboration, PNG/SVG export |
| [Fictional Word brief](examples/pulse-atlas/brief.docx) | Warm editorial incident dashboard | **2,480** events, **97.4%** auto-tagged, **12 min** median response, all marked synthetic demo data |
| [Same English brief → Chinese video](examples/pulse-atlas-zh/preview.mp4) | Localized editorial dashboard | Same **2,480**, **97.4%**, and **12 分钟**, with original English evidence retained in [facts.json](examples/pulse-atlas-zh/facts.json) |

The GapMine example is a **16-second, 1080×1350 (4:5) unofficial concept film** designed for a mobile social-feed card and based on a [public homepage snapshot](examples/gapmine/source.json) captured on **8 October 2026 at 09:43 UTC**; its live counters will change. A giant market landscape with a buried gap is the central visual subject. Source streams converge; illumination travels down and across the gap while source-backed panels respond. Two generated art plates contain no factual text. Camera movement, localized reveal, signal veins, dashboard, and exact numbers are rendered in code. The scene is a visual metaphor, not a recording of GapMine software; no numerical score is invented.

The six [GitHub stress-test films](examples/SHOWCASE.md) use six different physical subjects and commit-pinned README excerpts. Each perimeter dashboard shows six project-specific facts or commands plus Stars and Forks from a **dated 8 October 2026 UTC GitHub API snapshot**; the latter measure repository popularity, not product performance. Their generated art contains no factual text; claims are drawn from editable manifests. The illustrations are not screenshots, actual scan findings, actual query results, or real network topologies. The Word dashboard examples share one fictional brief. The Chinese scene includes an [OFL-licensed font subset](assets/fonts/README.md). Every example has an editable scene, fact manifest, MP4, and contact sheet under `examples/`.

## Run the included example manually

```bash
python3 examples/gapmine/sound.py
python3 scripts/render.py --scene examples/gapmine/scene.py --facts examples/gapmine/facts.json --audio examples/gapmine/audio.wav --out /tmp/gapmine.mp4
python3 scripts/verify.py --video /tmp/gapmine.mp4 --facts examples/gapmine/facts.json --source-json examples/gapmine/source.json --contact-sheet /tmp/gapmine-contact.jpg
```

The direct renderer requires a scene file. The **skill** tells the agent to create that file for a new input. This is agent-driven automation, not a fixed template that can produce a professional video from any URL with one deterministic CLI call.

For the Chinese sample, use `examples/pulse-atlas-zh/scene.py`, `examples/pulse-atlas-zh/facts.json`, and `examples/pulse-atlas/source.json`. See the [localization rules](references/localization.md) before translating product claims.

## Scope and limits

- Default target: 8–20 seconds. Rendering is local CPU/FFmpeg work; optional AI artwork uses the user's own model access.
- Text-based GitHub pages, ordinary websites, PDFs, DOCX, Markdown, and common images are supported directly when their text is readable. OCR requires Tesseract. Slide decks and unusual sources need the agent's native reader or conversion.
- Scanned, blocked, private, or misleading sources may require user-provided access or clarification. The agent must omit unsupported metrics.
- Current output is H.264 motion graphics, including generated art plates, 2.5D camera moves, spatial reveals, procedural subject layers, and optional original audio. There is no voiceover, 3D engine, or guaranteed studio-grade result for every source.
- Do not put private source snapshots in a public repository.

Read the [privacy notes](PRIVACY.md) before using private sources, and use the [showcase issue form](https://github.com/Balance0014/source-to-motion/issues/new/choose) only for material you can publish.

## Development

```bash
python3 -m unittest discover -s tests -v
```

Licensed under MIT. The bundled Chinese sample font retains its [SIL Open Font License](assets/fonts/OFL.txt). Example uv source content remains attributable to [Astral's uv project](https://github.com/astral-sh/uv); the uv video is an unofficial demo. The Pulse Atlas brief is fictional test material.
