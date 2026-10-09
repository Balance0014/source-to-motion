# Scene contracts

## Python/Pillow scene

`scripts/render.py` imports a Python scene file. It must provide:

```python
SIZE = (960, 540)
FPS = 24
DURATION = 12.0

def render(t: float, facts: dict) -> PIL.Image.Image:
    # t is seconds from 0 to DURATION.
    # facts maps id to the source-backed objects in facts.json.
    # Return an RGB or RGBA image of exactly SIZE.
    ...
```

Use paths relative to `__file__` for assets. The renderer outputs H.264 video with yuv420p pixel format for broad compatibility. It accepts 12–60 fps, 1–45 seconds, and frames up to roughly 4 megapixels.

## Browser canvas scene

`scripts/render_browser.py` opens a **local** HTML file in headless Chromium. The file must contain one `canvas#frame` with exact pixel dimensions and define:

```js
window.SCENE = {
  width: 1080,
  height: 1350,
  fps: 24,
  duration: 12,
  ready: true, // set only after local images and fonts have loaded
  render(t, facts) { /* draw a deterministic frame on canvas#frame */ }
};
```

`facts` is the same map of source-backed fact IDs as in Python. The renderer evaluates `SCENE.render` at each frame time and captures the canvas. Avoid random values inside `render` unless they are seeded and repeatable; build random particles once at load time. Do not load remote scripts, fonts, or images: bundle the assets with the editable scene. Install `requirements-browser.txt` and run `python -m playwright install chromium` once. `scripts/preview_browser.py` captures three frames before a full render.

```bash
python scripts/preview_browser.py --scene scene.html --facts facts.json --out contact.jpg
python scripts/render_browser.py --scene scene.html --facts facts.json --audio audio.wav --out video.mp4
```

The browser renderer enables authored motion fields and spatial compositions; it does not select or generate a concept. The examples under `examples/director-tests/` are distinct case studies, not templates for arbitrary products.

Motion checks to apply during review:

1. At least two scene elements change shape, position, state, or relationship independently.
2. Key text can be read when paused at each beat.
3. A viewer can state the product and one real capability after one watch.
4. Numbers and chart scales come from `facts.json`; decoration must not resemble an unlabeled factual chart.
5. First and last frames look intentional, with no blank gap.
6. For a cinematic brief, watch the video at normal speed. Verify that the environment, camera, and focal element progress through at least two distinct compositions; a contact sheet alone can hide weak motion.
