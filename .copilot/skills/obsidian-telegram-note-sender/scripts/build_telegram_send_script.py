#!/usr/bin/env python3
"""Build a Telegram payload + runnable curl shell script from an Obsidian markdown note."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import secrets
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def parse_front_matter(markdown_text: str) -> Tuple[Dict[str, object], str]:
    if not markdown_text.startswith("---\n"):
        return {}, markdown_text

    end_marker = "\n---\n"
    end = markdown_text.find(end_marker, 4)
    if end == -1:
        return {}, markdown_text

    raw_meta = markdown_text[4:end]
    body = markdown_text[end + len(end_marker) :]

    meta: Dict[str, object] = {}
    current_key: str | None = None

    for raw_line in raw_meta.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        list_match = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if list_match and current_key:
            value = list_match.group(1).strip().strip('"\'')
            existing = meta.get(current_key)
            if isinstance(existing, list):
                existing.append(value)
            elif existing is None:
                meta[current_key] = [value]
            else:
                meta[current_key] = [str(existing), value]
            continue

        kv_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if not kv_match:
            current_key = None
            continue

        key = kv_match.group(1).strip().lower()
        value = kv_match.group(2).strip()
        current_key = key

        if not value:
            meta[key] = []
            continue

        if value.startswith("[") and value.endswith("]"):
            items = [p.strip().strip('"\'') for p in value[1:-1].split(",") if p.strip()]
            meta[key] = items
        else:
            meta[key] = value.strip('"\'')

    return meta, body


def normalize_tags(meta: Dict[str, object]) -> List[str]:
    raw_tags = meta.get("tags", [])
    if isinstance(raw_tags, str):
        tags = [raw_tags]
    elif isinstance(raw_tags, list):
        tags = [str(item) for item in raw_tags]
    else:
        tags = []

    normalized: List[str] = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned.startswith("output/"):
            cleaned = cleaned[len("output/") :]
        if cleaned:
            normalized.append(cleaned)
    return normalized


def tag_to_hashtag(tag: str) -> str:
    candidate = tag.strip().lstrip("#")
    if not candidate:
        return ""
    candidate = re.sub(r"[^\w]+", "_", candidate, flags=re.UNICODE)
    candidate = candidate.strip("_")
    if not candidate:
        return ""
    return f"#{candidate}"


def convert_inline_markdown(text: str) -> str:
    escaped = html.escape(text)

    code_placeholders: List[str] = []

    def store_code(match: re.Match[str]) -> str:
        code_placeholders.append(f"<code>{match.group(1)}</code>")
        return f"@@CODE{len(code_placeholders)-1}@@"

    escaped = re.sub(r"`([^`]+)`", store_code, escaped)

    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>',
        escaped,
    )

    inline_rules = [
        (r"\|\|(.+?)\|\|", r"<tg-spoiler>\1</tg-spoiler>"),
        (r"~~(.+?)~~", r"<s>\1</s>"),
        (r"__(.+?)__", r"<u>\1</u>"),
        (r"\*\*(.+?)\*\*", r"<b>\1</b>"),
        (r"\*(.+?)\*", r"<i>\1</i>"),
        (r"_(.+?)_", r"<i>\1</i>"),
    ]

    for pattern, repl in inline_rules:
        escaped = re.sub(pattern, repl, escaped)

    for idx, code in enumerate(code_placeholders):
        escaped = escaped.replace(f"@@CODE{idx}@@", code)

    return escaped


def markdown_to_telegram_html(markdown_body: str) -> str:
    lines = markdown_body.splitlines()
    out: List[str] = []

    in_code = False
    code_lang = ""
    code_lines: List[str] = []

    in_quote = False
    quote_lines: List[str] = []

    def flush_quote() -> None:
        nonlocal in_quote, quote_lines
        if not in_quote:
            return
        joined = "\n".join(quote_lines)
        out.append(f"<blockquote>{joined}</blockquote>")
        in_quote = False
        quote_lines = []

    def flush_code() -> None:
        nonlocal in_code, code_lang, code_lines
        if not in_code:
            return
        body = html.escape("\n".join(code_lines))
        lang_attr = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
        out.append(f"<pre><code{lang_attr}>{body}</code></pre>")
        in_code = False
        code_lang = ""
        code_lines = []

    for line in lines:
        fence = re.match(r"^```([A-Za-z0-9_-]*)\s*$", line)
        if fence:
            if in_code:
                flush_code()
            else:
                flush_quote()
                in_code = True
                code_lang = fence.group(1)
            continue

        if in_code:
            code_lines.append(line)
            continue

        quote_match = re.match(r"^>\s?(.*)$", line)
        if quote_match:
            in_quote = True
            quote_lines.append(convert_inline_markdown(quote_match.group(1)))
            continue

        flush_quote()

        if not line.strip():
            out.append("")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            text = convert_inline_markdown(heading.group(2).strip())
            prefix = "#" * level
            out.append(f"<b>{prefix} {text}</b>")
            continue

        bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if bullet:
            out.append(f"• {convert_inline_markdown(bullet.group(1).strip())}")
            continue

        numbered = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if numbered:
            out.append(f"{numbered.group(1)}. {convert_inline_markdown(numbered.group(2).strip())}")
            continue

        out.append(convert_inline_markdown(line.strip()))

    flush_quote()
    flush_code()

    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()

    return "\n".join(out)


def format_meta(meta: Dict[str, object], tags: List[str]) -> List[str]:
    _ = meta  # keep signature stable; only tags are rendered per current requirement
    hashtags = [tag_to_hashtag(tag) for tag in tags]
    hashtags = [h for h in hashtags if h]
    if not hashtags:
        return []
    return [html.escape(" ".join(hashtags))]


def make_send_script_text(payload_path: Path, token_env: str) -> str:
    payload_abs = str(payload_path.resolve())
    return f"""#!/usr/bin/env bash
set -euo pipefail

TOKEN_ENV=\"{token_env}\"
PAYLOAD_FILE=\"{payload_abs}\"

if [ ! -f \"$PAYLOAD_FILE\" ]; then
  echo \"payload file not found: $PAYLOAD_FILE\" >&2
  exit 1
fi

TOKEN=\"${{!TOKEN_ENV:-}}\"
if [ -z \"$TOKEN\" ]; then
  echo \"environment variable $TOKEN_ENV is required\" >&2
  exit 1
fi

if [ \"${{DRY_RUN:-0}}\" = \"1\" ]; then
  echo \"DRY_RUN=1, payload:\"
  cat \"$PAYLOAD_FILE\"
  exit 0
fi

curl -sS -X POST \"https://api.telegram.org/bot${{TOKEN}}/sendMessage\" \\
  -H \"Content-Type: application/json\" \\
  --data @\"$PAYLOAD_FILE\"
"""


def build_payload(
    text: str,
    chat_id: str,
    thread_id: int | None,
    parse_mode: str,
) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "chat_id": int(chat_id) if re.fullmatch(r"-?\d+", chat_id) else chat_id,
        "parse_mode": parse_mode,
        "text": text,
    }
    if thread_id is not None:
        payload["message_thread_id"] = thread_id
    return payload


def build_unique_suffix() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = secrets.token_hex(3)
    return f"{timestamp}-{rand}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Telegram payload JSON + send shell script from an Obsidian markdown note"
    )
    parser.add_argument("--markdown", required=True, help="Path to markdown file")
    parser.add_argument("--chat-id", help="Telegram chat id; fallback env TELEGRAM_CHAT_ID")
    parser.add_argument(
        "--thread-id",
        type=int,
        help="Telegram message_thread_id; fallback env TELEGRAM_THREAD_ID",
    )
    parser.add_argument(
        "--parse-mode",
        choices=["HTML", "MarkdownV2"],
        default="HTML",
        help="Telegram parse mode",
    )
    parser.add_argument(
        "--token-env",
        default="TELEGRAM_BOT_TOKEN",
        help="Environment variable name that stores bot token",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp",
        help="Directory for generated payload.json and send_telegram.sh",
    )
    parser.add_argument(
        "--name-prefix",
        default="telegram_note",
        help="Prefix for generated files",
    )
    parser.add_argument(
        "--unique-id",
        help="Optional unique suffix for output filenames. Defaults to timestamp-random.",
    )
    args = parser.parse_args()

    markdown_path = Path(args.markdown)
    raw_text = markdown_path.read_text(encoding="utf-8")

    chat_id = args.chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        raise SystemExit("chat id is required: pass --chat-id or set TELEGRAM_CHAT_ID")

    thread_id = args.thread_id
    if thread_id is None:
        env_thread = os.environ.get("TELEGRAM_THREAD_ID")
        if env_thread:
            thread_id = int(env_thread)

    meta, body = parse_front_matter(raw_text)
    tags = normalize_tags(meta)
    body_html = markdown_to_telegram_html(body)

    meta_lines = format_meta(meta, tags)
    full_text = "\n".join(meta_lines + ([""] if meta_lines and body_html else []) + [body_html])

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    unique_id = args.unique_id or build_unique_suffix()
    payload_path = output_dir / f"{args.name_prefix}.{unique_id}.payload.json"
    send_script_path = output_dir / f"{args.name_prefix}.{unique_id}.send.sh"

    payload = build_payload(
        text=full_text,
        chat_id=chat_id,
        thread_id=thread_id,
        parse_mode=args.parse_mode,
    )
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    send_script_path.write_text(
        make_send_script_text(payload_path=payload_path, token_env=args.token_env),
        encoding="utf-8",
    )
    send_script_path.chmod(0o755)

    print(f"generated payload: {payload_path}")
    print(f"generated script:  {send_script_path}")


if __name__ == "__main__":
    main()
