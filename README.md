# Obsidian Sender Skills

本仓库使用以下 Skill 目录，不再使用根目录 `./skills`：

- `.codex/skills/...`
- `.copilot/skills/...`

当前包含两个发送 Skill：

- `obsidian-feishu-group-sender`
- `obsidian-telegram-note-sender`

## Obsidian -> Feishu 群组发送

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

## Obsidian -> Telegram 话题发送

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
