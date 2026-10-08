# Six GitHub stress-test films / 六个 GitHub 压测案例

Each 12-second, 1080×1350 film is an **unofficial visual concept**. Each `source.json` cites a commit-pinned public README excerpt and a dated GitHub API snapshot; `facts.json` binds on-screen claims to those sources. The central images are original generated metaphors, not product screenshots or verified output. The perimeter now shows six concrete source-backed product details plus repository stars and forks captured on **8 October 2026 UTC**. Repository popularity is not a product performance metric. No scan findings, query results, model throughput, or network measurements were invented. All six videos use one ingest/verification/render pipeline and different source-specific hero actions.

每条都是 12 秒、1080×1350 的**非官方视觉概念片**。`source.json` 固定到公开 README 的具体提交，并记录带日期的 GitHub API 快照；`facts.json` 把画面文案与原文关联。周边面板展示六项有出处的产品细节，以及 **2026 年 10 月 8 日 UTC** 抓取的仓库 Star/Fork 数。仓库热度不是产品效果数据；没有编造扫描结果、查询值、推理速度或网络测量。中央美术是原创视觉隐喻，不是产品截图或真实运行结果。六条共用取材、验真与渲染工具，但主角和运动按项目重新设计。

| Project / 项目 | Film / 视频 | Real dashboard content / 真实面板内容 | GitHub snapshot: Stars / Forks | Evidence / 事实 |
| --- | --- | --- | ---: | --- |
| [uv](https://github.com/astral-sh/uv) | [MP4](uv/preview.mp4) | `uv init`, lockfile, `uv sync`, script run, Python versions, cache | 90,501 / 3,635 | [manifest](uv/facts.json) |
| [Ollama](https://github.com/ollama/ollama) | [MP4](ollama/preview.mp4) | Open models, `ollama run`, REST API, local endpoint, Python/JS clients | 182,581 / 18,156 | [manifest](ollama/facts.json) |
| [Trivy](https://github.com/aquasecurity/trivy) | [MP4](trivy/preview.mp4) | Container, repo and filesystem targets; CVE, config, secret checks | 38,295 / 746 | [manifest](trivy/facts.json) |
| [DuckDB](https://github.com/duckdb/duckdb) | [MP4](duckdb/preview.mp4) | CSV/Parquet, exact README SQL examples, window functions, clients | 41,986 / 3,882 | [manifest](duckdb/facts.json) |
| [Tailscale](https://github.com/tailscale/tailscale) | [MP4](tailscale/preview.mp4) | WireGuard network, daemon, CLI, supported device platforms | 37,275 / 3,299 | [manifest](tailscale/facts.json) |
| [Excalidraw](https://github.com/excalidraw/excalidraw) | [MP4](excalidraw/preview.mp4) | Infinite canvas, hand-drawn style, collaboration, encryption, export | 133,691 / 15,622 | [manifest](excalidraw/facts.json) |

For each case, the editable `scene.py`, `facts.json`, `source.json`, `audio.wav`, and `contact.jpg` sit beside its MP4. Shared compositing lives in [`scripts/showcase_engine.py`](../scripts/showcase_engine.py). These six custom hero scenes are test examples, not six fixed presets for future inputs. A new product still requires its own business reading and visual direction.

The [art prompts](SHOWCASE-ART.md) and generated plates are included for reproducibility. The videos themselves add spatial reveals, subject-layer motion, source-checked type, and sound in code.

uv's 10–100× comparison is **Astral's own README claim**. Its linked benchmark says performance varies by operating system, filesystem, and packages. The on-screen attribution and caveat are deliberate; do not read the number as an independent benchmark by this project.
