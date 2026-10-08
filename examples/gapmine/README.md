# GapMine signal-to-opportunity concept film

This is a 16-second, 1080×1350 (4:5) **unofficial** visual concept based on the public [GapMine homepage](https://gapmine.com/). It is designed for a mobile social-feed card, not a GapMine endorsement or a live dashboard.

`source.json` records the homepage text captured at **2026-10-08 09:43:14 UTC**. The three displayed counters—**101,081** builder signals, **1,140** opportunity cards, and **124** communities—belong to that snapshot and may differ from today's site. `facts.json` keeps the source excerpts and locators; `scripts/verify.py` checks them before rendering.

The story centers on a large market landscape. Source signals converge on an unseen canyon; it lights up as an opportunity is found. Mobile-sized dashboard panels along the right and bottom edges show the input scale, source excerpt, recurring demand, five named signal dimensions, and the source-linked example opportunity. The example title, quote, status, and counts come from the captured homepage. No numerical score is invented. The landscape, signal streams, and dashboard responses are visual metaphors, not a recording of GapMine's actual software operation.

The two cinematic market plates in `assets/gapmine-market-dark.png` and `assets/gapmine-market-lit.png` provide non-factual art. `scene.py` animates the camera, reveal, evidence streams, scanner, responsive dashboard, and all exact text and numbers. `sound.py` generates its original audio bed. All image prompts are documented in [art-prompts.md](art-prompts.md).

From the repository root:

```bash
python3 examples/gapmine/sound.py
python3 scripts/render.py --scene examples/gapmine/scene.py --facts examples/gapmine/facts.json --audio examples/gapmine/audio.wav --out /tmp/gapmine.mp4
python3 scripts/verify.py --video /tmp/gapmine.mp4 --facts examples/gapmine/facts.json --source-json examples/gapmine/source.json --contact-sheet /tmp/gapmine-contact.jpg
```
