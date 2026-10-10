# Contributing / 参与

Bug reports and improvements are welcome. Include your operating system, Python version, FFmpeg version, the command you ran, and the smallest reproducible input. Remove API keys, private paths, and customer data before posting.

To share a video made with the skill, open a [showcase issue](https://github.com/Balance0014/source-to-motion/issues/new/choose) with a **public** source URL, a video link, the output language, and a short note on which claims were checked. Share only material you have permission to publish. A useful showcase may be linked from the README after review.

欢迎提交问题和改进。请附上系统、Python/FFmpeg 版本、运行命令和可公开的最小复现资料，先删掉密钥、私人路径和客户内容。分享成片时，请提供可公开的原始链接、视频链接、输出语言，以及数字核对说明；只提交你有权公开的内容。

The canonical skill instructions live in `skill/source-to-motion/SKILL.md`. When changing root `scripts/`, `references/`, requirements, or fonts, run `python3 scripts/sync_skill_package.py` before committing. CI checks the copy and publishes the small package to the `skill-only` branch after tests pass. The branch is part of this same repository; do not edit it by hand.

Skill 指令以 `skill/source-to-motion/SKILL.md` 为准。修改根目录的脚本、参考资料、依赖或字体后，先运行 `python3 scripts/sync_skill_package.py`；CI 会检查副本，并在测试通过后同步到同仓库的 `skill-only` 分支。
