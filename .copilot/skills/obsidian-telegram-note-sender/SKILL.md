---
name: obsidian-telegram-note-sender
description: Convert Obsidian Markdown notes into Telegram Bot API messages and generate runnable curl shell scripts for Telegram groups/topics. Use when asked to send markdown notes to Telegram, map Obsidian front matter to message metadata, strip `output/` from tags, or produce/send `sendMessage` payloads with token injected via environment variables only.
---

# Obsidian Telegram Note Sender

## Inputs

Require these inputs before execution:
- `markdown_path`: absolute or relative path to an Obsidian markdown note.
- `chat_id`: Telegram group chat ID (can be numeric or string style ID).
- `thread_id`: Telegram topic/thread ID (`message_thread_id`) inside the group.
- `token_env`: environment variable name storing the bot token. Default to `TELEGRAM_BOT_TOKEN`.
- `unique_id` (optional): unique filename suffix. If omitted, auto-generate `YYYYmmddHHMMSS-randomhex`.

Never accept raw token values in command arguments or files. Use environment variables only.

## Workflow

1. Read and normalize markdown metadata.
2. Convert markdown body to Telegram-supported format.
3. Generate runnable shell script that sends by `curl`.

Use `scripts/build_telegram_send_script.py` for deterministic generation.

## Step 1: Parse Obsidian Metadata

Run:

```bash
python3 scripts/build_telegram_send_script.py \
  --markdown <markdown_path> \
  --chat-id <chat_id> \
  --thread-id <thread_id> \
  --token-env <token_env> \
  --output-dir <output_dir>
```

Metadata behavior:
- Parse YAML front matter if present.
- Extract `tags` and remove `output/` prefix from every tag.
- Ignore other metadata fields for now.
- Render tags as Telegram hashtags (for example: `#ai #agent`) at the top of Telegram text.

## Step 2: Convert Markdown to Telegram Message Text

Default `parse_mode` is `HTML`.

Telegram `sendMessage` has no dedicated `tag` parameter, so tags must be embedded in `text` (as hashtags) rather than passed in a separate payload field.

Conversion rules in `HTML` mode:
- Convert headings to bold lines.
- Convert inline formatting: bold, italic, underline, strikethrough, spoiler.
- Convert fenced code blocks to `<pre><code class="language-...">...</code></pre>`.
- Convert inline code to `<code>...</code>`.
- Convert blockquotes to `<blockquote>...</blockquote>`.
- Convert links `[text](url)` to `<a href="url">text</a>`.
- Escape unsafe HTML characters before wrapping tags.

If caller requests `--parse-mode MarkdownV2`, keep Telegram payload mode as MarkdownV2 (no extra escaping helper is bundled here).

## Step 3: Generate Runnable Curl Script

The script generates two files in `--output-dir`:
- `<prefix>.<unique_id>.payload.json`: Bot API payload.
- `<prefix>.<unique_id>.send.sh`: runnable sender script.

If `--output-dir` is omitted, default output directory is `/tmp`.

Execute:

```bash
chmod +x <prefix>.send.sh
<token_env>=<token_value> ./<prefix>.send.sh
```

Dry run without sending:

```bash
DRY_RUN=1 <token_env>=dummy ./<prefix>.send.sh
```

## Resource Files

- `scripts/build_telegram_send_script.py`: Parse markdown, transform message text, write payload and shell sender.
- `references/telegram-sendmessage-cheatsheet.md`: Supported `sendMessage` fields and formatting reminders.
