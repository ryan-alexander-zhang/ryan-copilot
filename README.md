# Skills Overview

本仓库主要维护 Codex/Copilot 可复用 skills。当前不使用根目录 `./skills`，而是使用：

- `.codex/skills/...`
- `.copilot/skills/...`

其中 `.codex/skills` 是主维护目录；`.copilot/skills` 目前只保留部分发送类 skill 的副本。

## 当前 Skills

### `.codex/skills`

| Skill | 作用 | 路径 |
| --- | --- | --- |
| `alphaxiv-paper-lookup` | 通过 alphaxiv 获取 arXiv 论文的结构化 AI 摘要，避免直接读原始 PDF | `.codex/skills/alphaxiv-paper-lookup` |
| `context-hub-doc-builder` | 从 URL、OpenAPI/Swagger 或本地文件生成可 `chub build` 的私有 Context Hub docs，并输出测试 CLI 与手动配置提示 | `.codex/skills/context-hub-doc-builder` |
| `github-repo-capability-validator` | 对 GitHub 仓库执行 README-first 的 capability 分析、代码核验、任务拆分和报告输出 | `.codex/skills/github-repo-capability-validator` |
| `markdownlint-cli2-validator` | 用 `markdownlint-cli2` 校验和自动修复 Markdown | `.codex/skills/markdownlint-cli2-validator` |
| `obsidian-feishu-group-sender` | 将 Obsidian Markdown 转成 Feishu 机器人消息并生成可执行发送脚本 | `.codex/skills/obsidian-feishu-group-sender` |
| `obsidian-telegram-note-sender` | 将 Obsidian Markdown 转成 Telegram Bot API 消息并生成可执行发送脚本 | `.codex/skills/obsidian-telegram-note-sender` |

### `.copilot/skills`

| Skill | 作用 | 路径 |
| --- | --- | --- |
| `obsidian-feishu-group-sender` | Feishu 群消息发送副本 | `.copilot/skills/obsidian-feishu-group-sender` |
| `obsidian-telegram-note-sender` | Telegram 话题消息发送副本 | `.copilot/skills/obsidian-telegram-note-sender` |

## 重点 Skills

### GitHub Repo Capability Validator

- Skill 路径: `.codex/skills/github-repo-capability-validator`
- 作用: 对 GitHub 仓库做严格的 README-first capability 分析，并输出可 review 的 Markdown 报告 bundle

当前能力：

- 先 `git clone` 仓库，本地分析默认分支源码
- 从 README 提取核心 capabilities，避免代码反推 capability
- 输出任务拆分文档、入口/主流程文档、逐 capability 文档和最终汇总文档
- 对每个 capability 做代码核验
- 默认尽量输出 Mermaid 图：
  - 架构图
  - 调用时序图
  - 状态/生命周期图
  - 数据/存储结构图
- 报告默认写到：
  - `reports/<repo-name>-capability-audit/`

典型输出结构：

- `00-task-breakdown.md`
- `01-readme-capability-extraction.md`
- `02-entrypoints-and-main-flow.md`
- `03-capability-<name>.md`
- `99-final-consistency-summary.md`

适用场景：

- 分析一个 GitHub 仓库 README 中的核心能力到底怎么实现
- 核对 README claim 和代码现实是否一致
- 生成足够支撑“复刻级理解”的工程分析报告

### AlphaXiv Paper Lookup

- Skill 路径: `.codex/skills/alphaxiv-paper-lookup`
- 作用: 给出 arXiv 论文的结构化概览，适合快速理解研究论文

适用场景：

- 用户给出 arXiv 链接或 paper ID
- 需要快速总结或解释一篇论文
- 希望用比 PDF 更适合 LLM/agent 的结构化内容做分析

### Context Hub Doc Builder

- Skill 路径: `.codex/skills/context-hub-doc-builder`
- 作用: 从 URL、OpenAPI/Swagger 或本地文件生成私有 Context Hub 文档目录，供 `chub build` 构建本地 registry
- 生成脚本: `.codex/skills/context-hub-doc-builder/scripts/scaffold_context_hub_doc.py`

适用场景：

- 需要把内部 API、命令文档或本地资料转换成 `author/docs/<entry>/DOC.md`
- 需要自动补齐 Context Hub frontmatter、`references/` 目录和测试 CLI
- 需要给 `~/.chub/config.yaml` 生成本地 source 配置片段

示例：

```bash
python3 .codex/skills/context-hub-doc-builder/scripts/scaffold_context_hub_doc.py \
  --content-root /tmp/chub-content \
  --author mycompany \
  --entry-name internal-api \
  --source-input ./openapi.yaml \
  --description "Internal API docs" \
  --language http \
  --version 1.0.0 \
  --source-trust official
```

注意：

- 脚本最终输出会明确提示 `~/.chub/config.yaml` 需要手动修改
- 如果配置里只保留本地 source，`chub search "openai"` 之类的公共内容检索会消失
- 如果需要同时保留公共和本地内容，应继续保留 `community` source

### Markdownlint CLI2 Validator

- Skill 路径: `.codex/skills/markdownlint-cli2-validator`
- 作用: 校验 Markdown 文件格式，默认先尝试自动修复，再输出剩余 lint 问题

适用场景：

- 检查 `.md` 文件或文档目录
- 自动修复 markdownlint-cli2 可修复的问题
- 生成剩余 lint 报告

## Obsidian Sender Skills

### Obsidian -> Feishu 群组发送

- Skill 路径: `.codex/skills/obsidian-feishu-group-sender`（`.copilot` 下也有同名副本）
- 生成脚本: `.codex/skills/obsidian-feishu-group-sender/scripts/build_feishu_send_script.py`

环境变量：

```bash
export FEISHU_BOT_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/xxxx'
export FEISHU_BOT_SECRET='your_signing_secret' # 可选，开启签名校验时需要
```

生成发送文件：

```bash
python3 .codex/skills/obsidian-feishu-group-sender/scripts/build_feishu_send_script.py \
  --markdown /absolute/path/to/note.md \
  --msg-type text \
  --output-dir /tmp \
  --name-prefix note-to-feishu
```

发送：

```bash
/tmp/note-to-feishu.<unique>.send.sh
```

### Obsidian -> Telegram 话题发送

- Skill 路径: `.codex/skills/obsidian-telegram-note-sender`（`.copilot` 下也有同名副本）
- 生成脚本: `.codex/skills/obsidian-telegram-note-sender/scripts/build_telegram_send_script.py`
- 线程映射: `.codex/skills/obsidian-telegram-note-sender/config/thread_map.json`

环境变量：

```bash
export TELEGRAM_BOT_TOKEN='your_bot_token'
export TELEGRAM_CHAT_ID='-100xxxxxxxxxx' # 可不设，若命令中显式传 --chat-id
```

生成发送文件（支持 `thread_id` 直接传别名，如 `resource` / `digest`）：

```bash
python3 .codex/skills/obsidian-telegram-note-sender/scripts/build_telegram_send_script.py \
  --markdown /absolute/path/to/note.md \
  --chat-id -100xxxxxxxxxx \
  --thread-id resource \
  --output-dir /tmp
```

脚本会输出：

- `/tmp/telegram_note.<unique>.payload.json`
- `/tmp/telegram_note.<unique>.send.sh`
- 并在终端直接打印上述两个文件内容（便于确认）

发送（建议先确认 payload，再执行）：

```bash
/tmp/telegram_note.<unique>.send.sh
```
