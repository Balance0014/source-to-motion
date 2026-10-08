# Scene contract

The renderer imports a Python scene file. It must provide:

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

Use paths relative to `__file__` for assets. The renderer outputs H.264 video with yuv420p pixel format for broad compatibility. It accepts 12–60 fps, 1–45 seconds, and frames up to roughly 4 megapixels. There is no stock template: generate the scene for each source. `examples/gapmine/scene.py` shows source quote cards flying into a rotating scoring structure and an evidence card emerging, with captured-source fact binding. `examples/uv/scene.py` shows typography, particles, paths, and background art.

Motion checks to apply during review:

1. At least two scene elements change shape, position, state, or relationship independently.
2. Key text can be read when paused at each beat.
3. A viewer can state the product and one real capability after one watch.
4. Numbers and chart scales come from `facts.json`; decoration must not resemble an unlabeled factual chart.
5. First and last frames look intentional, with no blank gap.
6. For a cinematic brief, watch the video at normal speed. Verify that the environment, camera, and focal element progress through at least two distinct compositions; a contact sheet alone can hide weak motion.
