---
name: obsidian-feishu-group-sender
description: Convert Obsidian Markdown notes to Feishu custom-bot messages and generate runnable curl scripts for posting into Feishu group chats via webhook. Use when asked to publish markdown notes to Feishu groups, normalize Obsidian tags (remove `output/` prefix), or automate Feishu webhook sending with secrets injected from environment variables.
---

# Obsidian Feishu Group Sender

## Inputs

Require these inputs:
- `markdown_path`: path to an Obsidian markdown file.
- `webhook_env`: environment variable name containing Feishu webhook URL. Default `FEISHU_BOT_WEBHOOK`.
- `secret_env` (optional): environment variable name containing bot secret for signature mode. Default `FEISHU_BOT_SECRET`.

Never hardcode webhook URL or secret in files. Inject via environment variables.

## Workflow

1. Parse markdown and extract tags from front matter.
2. Convert content to Feishu message payload (`text` or `post`).
3. Generate runnable shell script using `curl` to send payload.

Use `scripts/build_feishu_send_script.py` for deterministic generation.

## Step 1: Parse Markdown Meta

Behavior:
- Parse YAML front matter if present.
- Read only `tags` metadata.
- Remove `output/` prefix from each tag.
- Convert tags to hashtag line (for example: `#ai #agent`).

## Step 2: Convert Markdown Body

Supported output modes:
- `text` (default): convert markdown to plain text and preserve structure markers.
- `post`: build Feishu post payload (`content.post.zh_cn`).

Conversion behavior:
- Convert markdown links to `text (url)` in plain text mode.
- Keep heading/bullet structure for readability.
- Prepend normalized tags line before body when tags exist.

## Step 3: Generate Payload + Curl Script

Run:

```bash
python3 scripts/build_feishu_send_script.py \
  --markdown <markdown_path> \
  --msg-type text \
  --output-dir /tmp \
  --name-prefix feishu-note
```

Outputs:
- `<prefix>.<unique_id>.payload.json`
- `<prefix>.<unique_id>.send.sh`

Run sender:

```bash
FEISHU_BOT_WEBHOOK='<webhook_url>' \
FEISHU_BOT_SECRET='<optional_secret>' \
./<prefix>.<unique_id>.send.sh
```

Dry run:

```bash
DRY_RUN=1 FEISHU_BOT_WEBHOOK='https://example.invalid' ./<prefix>.<unique_id>.send.sh
```

## Resource Files

- `scripts/build_feishu_send_script.py`: Parse Obsidian note, convert content, and generate payload/sender script.
- `references/feishu-custom-bot-notes.md`: Official links and implementation notes for custom-bot webhook usage.
