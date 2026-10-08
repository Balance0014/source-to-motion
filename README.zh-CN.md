# Source to Motion

把 GitHub 项目、产品网站、PDF、Word 或产品简介，做成 **8–20 秒有真实动态的短视频**。画面上的数字和产品说法要能找到原文依据。

这是一个开源的 **Codex Skill + 本地脚本**，不是收费的视频服务。你用自己的 Codex/模型额度；Python 和 FFmpeg 在你的电脑上渲染。可选的 AI 背景图也使用你自己的工具额度，仓库作者不收取 API 费用。

[看 uv 样片](examples/uv/preview.mp4) · [看 Word 仪表盘样片](examples/pulse-atlas/preview.mp4) · [完整英文说明](README.md)

## 安装

先安装 Python 3.10+ 和 FFmpeg，再运行：

```bash
git clone https://github.com/Balance0014/source-to-motion.git ~/.codex/skills/source-to-motion
python3 -m pip install -r ~/.codex/skills/source-to-motion/requirements.txt
```

新开 Codex 对话，直接说：

> 用 $source-to-motion 把这个项目做成 12 秒短视频：https://github.com/astral-sh/uv。画面要有独立创意，所有数字对照原文，交付 MP4 和可编辑工程。

Skill 会指导 Agent：读资料 → 摘出有出处的事实 → 为这个项目设计画面 → 编写动画 → 本地渲染 → 核对数字和视频。不是把同一个模板套到所有产品上。

## 已经交付的东西

- 资料抽取：GitHub、网站、PDF、Word、文本；图片可选 OCR。
- 事实清单：每个数字都保存原文片段和位置。
- 可编辑的逐帧动画工程、MP4 渲染器、原创程序配乐、核验工具。
- 两个完整样片：uv 项目和虚构的 Word 数据仪表盘，视觉方向不同。

**边界说清楚：** 这是 Agent 主导的自动制作流程，不是纯命令行“一贴任何链接就保证顶级成片”。扫描件、PPT 等需要 Agent 自己读取；读不到的资料不能编造。核验脚本能抓缺失出处和乱加数字，最终画面与表述仍要由 Agent 检查。
