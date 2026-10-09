# uv · dependency resolution as a moving graph

**Industry read.** A Python project declares requirements; uv resolves dependencies into a lockfile, syncs an environment, and runs commands. The [official locking and syncing docs](https://docs.astral.sh/uv/concepts/projects/sync/) distinguish resolution, lock, and sync. The dated README snapshot in `source.json` supplies the visible claims.

**Input → mechanism → output.** Python packages → dependencies visibly traverse and converge → universal lockfile, then `uv sync` and `uv run example.py`.

**Direction choice.** A graph changing its relationships is more faithful than a generic speedometer. A package warehouse was considered but rejected because moving boxes would show transport rather than resolution. The first shot begins inside a dense unresolved web; orange routes propagate, then a bright lock structure forms. The camera moves from close graph detail to a broader resolved structure. Commands appear only after the lock action.

**Evidence and boundary.** The graph is illustrative; it is not an actual uv dependency tree. `10–100× VS PIP` is Astral's qualified claim, paired with the benchmark caveat. Product text is drawn from `facts.json`; artwork contains no text.
