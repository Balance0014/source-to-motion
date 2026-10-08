# Source to Motion

[English](README.md) · **简体中文**

**给一个项目链接或文档，做出有真实动态、数字有出处的短视频。**

![中文仪表盘样片静帧](media/pulse-zh-poster.jpg)

[看中文完整视频](examples/pulse-atlas-zh/preview.mp4) · [看 uv 项目视频](examples/uv/preview.mp4) · [看英文仪表盘视频](examples/pulse-atlas/preview.mp4)

Source to Motion 是一套开源的 **Agent Skill + 本地视频工具**。把 GitHub 仓库、产品网站、PDF、Word 或产品简介交给自己的 Codex，Agent 会读资料、设计符合项目内容的画面、编写可编辑动画、在本机渲染 MP4，并把画面上的产品事实和原文对应起来。

你使用自己的 Codex/模型额度；Python 和 FFmpeg 在你的电脑上渲染。仓库没有托管渲染服务，也不需要把 API Key 交给仓库作者。可选的 AI 背景图同样使用你自己的工具额度。

## 直接使用

需要 Python 3.10+、FFmpeg，以及能运行本地 Python 的 Codex。安装 Skill 有两种方式：

也可以用已验证的 [skills CLI](https://www.skills.sh/docs/cli) 安装 Skill：

```bash
npx skills add Balance0014/source-to-motion -g -a codex -y
```

CLI 会显示安装位置；随后在该目录安装 `requirements.txt`。如果想要明确的固定目录，直接运行：

```bash
git clone https://github.com/Balance0014/source-to-motion.git ~/.codex/skills/source-to-motion
python3 -m pip install -r ~/.codex/skills/source-to-motion/requirements.txt
ffmpeg -version
```

新开 Codex 对话，给它链接和语言要求：

> 用 $source-to-motion 把这个 GitHub 项目做成 12 秒中文动态短片：https://github.com/astral-sh/uv。画面要有独立创意，数字和比较必须有原文依据，交付 MP4 和可编辑工程。

也可以输入本地 PDF、Word、产品网站或简报。想做英文视频就写“输出英文”；没有指定语言时，默认跟随资料的主要语言。**每支视频用一种清楚的主语言**；只有明确需要双语字幕时才做双语布局。

## 它实际提供什么

| 内容 | 作用 |
| --- | --- |
| [SKILL.md](SKILL.md) | 指导 Agent 从资料到成片，并执行质量检查。 |
| [资料抽取脚本](scripts/ingest.py) | 读取 GitHub、普通网页、PDF、DOCX、文本；图片可在安装 Tesseract 后做 OCR。 |
| `facts.json` 事实清单 | 保存每条画面文案、数字对应的原文片段和位置。 |
| [渲染脚本](scripts/render.py) | 用 Pillow + 本地 FFmpeg 输出常见播放器可用的 H.264 MP4。 |
| [配乐脚本](scripts/sound.py) | 可选的原创程序配乐，不依赖音乐订阅。 |
| [核验脚本](scripts/verify.py) | 检查证据片段、乱加的数字、视频元数据，并生成逐段画面检查图。 |
| 三支可编辑样片 | uv 项目视频，以及同一份 Word 简报的英文和中文仪表盘视频。 |

核验器是防错工具：它能发现缺失出处和凭空加入的数字，**不能代替人判断翻译是否准确、画面是否好看**。Agent 必须查看实际视频，检查单位、时间范围、出处、字幕和声音。

## 样片和数字

| 输入 | 视觉方向 | 画面里核对的事实 |
| --- | --- | --- |
| [uv 的公开 GitHub 仓库](https://github.com/astral-sh/uv) | 能量核心与汇聚的工具路径 | Python 包/项目管理器、单一工具，以及 uv 自己在 README 中给出的 **10–100×** 对 pip 的比较 |
| [虚构 Word 简报](examples/pulse-atlas/brief.docx) | 明亮的事件仪表盘 | 最近 30 天 **2,480** 件事件、**97.4%** 自动标记、**12 分钟**响应时间中位数 |
| [同一英文简报 → 中文视频](examples/pulse-atlas-zh/preview.mp4) | 针对中文重排文字与卡片 | 数字保持相同；[中文事实清单](examples/pulse-atlas-zh/facts.json)保留英文原句作为证据 |

Word 简报及其数字都是**虚构测试资料**，视频画面也明确标注。uv 的背景是[生成的美术素材](assets/uv_energy.png)；产品文字和数字由代码绘制，没有烘焙在图片里。中文样片使用了随仓库提供的、遵循 [OFL 字体许可](assets/fonts/README.md)的小字库。

## 自己复现样片

在仓库根目录运行：

```bash
python3 scripts/render.py --scene examples/pulse-atlas-zh/scene.py --facts examples/pulse-atlas-zh/facts.json --audio examples/pulse-atlas/audio.wav --out /tmp/pulse-zh.mp4
python3 scripts/verify.py --video /tmp/pulse-zh.mp4 --facts examples/pulse-atlas-zh/facts.json --source-json examples/pulse-atlas/source.json --contact-sheet /tmp/pulse-zh-contact.jpg
```

直接调用渲染脚本时需要已有 `scene.py`；**Skill 的作用是让 Agent 根据新资料创建新场景**，不是把同一个固定模板套在所有产品上。英文资料做中文视频时，原文放在 `evidence`，中文画面文字放在 `display`；具体规则见[多语言说明](references/localization.md)。

## 边界

- 默认目标是 8–20 秒的二维动态图形视频。没有内置配音、3D 引擎，也不保证任何资料都能一次生成影视级画面。
- 扫描件需要 OCR 或 Agent 视觉读取；PPT 和少见格式需要 Agent 自行读取或转换。资料不可访问时，不能编造内容。
- 新中文项目若使用样片字库以外的汉字，需要系统安装完整的中文字体或另行提供字体。
- 私人项目的 `source.json` 可能包含原文，不要把它提交到公开仓库。

更具体的说明见[隐私说明](PRIVACY.md)。如想分享成片，请使用[展示入口](https://github.com/Balance0014/source-to-motion/issues/new/choose)，只提交有权公开的资料。

## 开发与许可

```bash
python3 -m unittest discover -s tests -v
```

仓库代码使用 MIT 许可；[中文样片字库](assets/fonts/OFL.txt)使用 SIL Open Font License 1.1。uv 示例资料归属于 [Astral 的 uv 项目](https://github.com/astral-sh/uv)，本仓库的 uv 视频是非官方演示。
