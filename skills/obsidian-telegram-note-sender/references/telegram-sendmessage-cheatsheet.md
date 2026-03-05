# Telegram `sendMessage` Cheatsheet

## Required fields

- `chat_id`
- `text`

## Topic support

- Use `message_thread_id` to send into a specific topic/thread inside a group.

## Parse modes

- `HTML`: supports tags like `<b>`, `<i>`, `<u>`, `<s>`, `<tg-spoiler>`, `<a>`, `<code>`, `<pre>`, `<blockquote>`.
- `MarkdownV2`: stricter escaping requirements.

## Curl pattern

```bash
curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  --data @payload.json
```

## Security

- Keep bot token in environment variables only.
- Do not hardcode token in scripts, markdown files, or git history.
