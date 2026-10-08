# Privacy / 隐私

## English

The repository's Python scripts run on your machine. They do not include telemetry, a hosted render service, or a request to send your source files to the repository owner. `ingest.py` contacts a URL only when you supply that URL; local files are read locally. It saves extracted source text to the output path you choose. Generated videos, fact manifests, and contact sheets remain local unless you upload them yourself.

Your AI agent and any optional image-generation tool may use their own online services under your account. Review those tools' data settings before feeding them private material. Treat `source.json`, `facts.json`, and generated scenes as potentially sensitive: they can contain excerpts, file paths, or internal product claims. Do not commit private outputs to a public repository.

The checked-in examples use the public GapMine homepage, six public GitHub repositories, and a clearly fictional Pulse Atlas brief. They do not include private customer documents, credentials, or unpublished product data.

## 简体中文

仓库里的 Python 脚本在你的电脑上运行，没有向仓库作者回传资料的遥测，也没有托管渲染服务。只有你输入网页链接时，`ingest.py` 才会请求该网页；本地文件在本地读取。抽取的原文保存到你指定的位置，视频、事实清单和检查图默认也留在本地。

你自己的 Codex 和可选的图片生成工具可能使用其账户下的在线服务。处理私人资料前，请按你使用的工具检查其数据设置。`source.json`、`facts.json` 和生成场景可能包含原文、文件路径或内部数字，**不要把私人输出提交到公开仓库**。

仓库内的样例只使用 GapMine 公开首页、六个公开 GitHub 仓库和明确标为虚构的 Pulse Atlas 简报，没有上传私人客户文档、凭据或未公开产品数据。
