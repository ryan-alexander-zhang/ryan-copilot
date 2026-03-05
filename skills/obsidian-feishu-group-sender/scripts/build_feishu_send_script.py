#!/usr/bin/env python3
"""Build Feishu custom-bot payload + runnable curl shell script from an Obsidian markdown note."""

from __future__ import annotations

import argparse
import json
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


def markdown_to_plain_text(markdown_body: str) -> str:
    lines = markdown_body.splitlines()
    out: List[str] = []

    in_code = False
    for line in lines:
        fence = re.match(r"^```", line)
        if fence:
            in_code = not in_code
            continue

        if in_code:
            out.append(line)
            continue

        line = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r"\1 (\2)", line)
        line = re.sub(r"`([^`]+)`", r"\1", line)
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"__(.*?)__", r"\1", line)
        line = re.sub(r"\*(.*?)\*", r"\1", line)
        line = re.sub(r"_(.*?)_", r"\1", line)
        line = re.sub(r"~~(.*?)~~", r"\1", line)

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            out.append(f"{'#' * level} {heading.group(2).strip()}")
            continue

        bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if bullet:
            out.append(f"- {bullet.group(1).strip()}")
            continue

        out.append(line.rstrip())

    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()

    return "\n".join(out)


def build_unique_suffix() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = secrets.token_hex(3)
    return f"{timestamp}-{rand}"


def build_text_payload(text: str) -> Dict[str, object]:
    return {
        "msg_type": "text",
        "content": {
            "text": text,
        },
    }


def build_post_payload(title: str, text: str) -> Dict[str, object]:
    content_rows = []
    for line in text.splitlines():
        if not line.strip():
            content_rows.append([{"tag": "text", "text": " "}])
            continue
        content_rows.append([{"tag": "text", "text": line}])

    return {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": content_rows,
                }
            }
        },
    }


def make_send_script_text(payload_path: Path, webhook_env: str, secret_env: str) -> str:
    payload_abs = str(payload_path.resolve())
    return f"""#!/usr/bin/env bash
set -euo pipefail

WEBHOOK_ENV=\"{webhook_env}\"
SECRET_ENV=\"{secret_env}\"
PAYLOAD_FILE=\"{payload_abs}\"

if [ ! -f \"$PAYLOAD_FILE\" ]; then
  echo \"payload file not found: $PAYLOAD_FILE\" >&2
  exit 1
fi

WEBHOOK_URL=\"${{!WEBHOOK_ENV:-}}\"
if [ -z \"$WEBHOOK_URL\" ]; then
  echo \"environment variable $WEBHOOK_ENV is required\" >&2
  exit 1
fi

SEND_PAYLOAD=\"$PAYLOAD_FILE\"
TEMP_PAYLOAD=\"\"
SECRET=\"${{!SECRET_ENV:-}}\"

if [ -n \"$SECRET\" ]; then
  timestamp=$(date +%s)
  sign=$(python3 -c 'import base64, hashlib, hmac, sys; ts, sec = sys.argv[1], sys.argv[2]; msg=f"{{ts}}\\n{{sec}}".encode("utf-8"); print(base64.b64encode(hmac.new(sec.encode("utf-8"), msg, hashlib.sha256).digest()).decode("utf-8"))' "$timestamp" "$SECRET")

  TEMP_PAYLOAD=$(mktemp)
  python3 -c 'import json, sys; p=json.load(open(sys.argv[1], "r", encoding="utf-8")); p["timestamp"]=sys.argv[2]; p["sign"]=sys.argv[3]; print(json.dumps(p, ensure_ascii=False))' "$PAYLOAD_FILE" "$timestamp" "$sign" > "$TEMP_PAYLOAD"
  SEND_PAYLOAD=\"$TEMP_PAYLOAD\"
fi

if [ \"${{DRY_RUN:-0}}\" = \"1\" ]; then
  echo \"DRY_RUN=1, webhook env: $WEBHOOK_ENV\"
  cat \"$SEND_PAYLOAD\"
  [ -z \"$TEMP_PAYLOAD\" ] || rm -f \"$TEMP_PAYLOAD\"
  exit 0
fi

curl -sS -X POST \"$WEBHOOK_URL\" \\
  -H \"Content-Type: application/json\" \\
  --data @\"$SEND_PAYLOAD\"

[ -z \"$TEMP_PAYLOAD\" ] || rm -f \"$TEMP_PAYLOAD\"
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Feishu payload JSON + send shell script from an Obsidian markdown note"
    )
    parser.add_argument("--markdown", required=True, help="Path to markdown file")
    parser.add_argument(
        "--webhook-env",
        default="FEISHU_BOT_WEBHOOK",
        help="Environment variable name storing webhook URL",
    )
    parser.add_argument(
        "--secret-env",
        default="FEISHU_BOT_SECRET",
        help="Environment variable name storing bot secret for signature",
    )
    parser.add_argument(
        "--msg-type",
        choices=["text", "post"],
        default="text",
        help="Feishu message type",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp",
        help="Directory for generated payload and send script",
    )
    parser.add_argument(
        "--name-prefix",
        default="feishu_note",
        help="Prefix for generated files",
    )
    parser.add_argument(
        "--unique-id",
        help="Optional unique suffix for output filenames. Defaults to timestamp-random.",
    )
    args = parser.parse_args()

    markdown_path = Path(args.markdown)
    raw_text = markdown_path.read_text(encoding="utf-8")

    meta, body = parse_front_matter(raw_text)
    tags = normalize_tags(meta)
    hashtags = [tag_to_hashtag(tag) for tag in tags]
    hashtags = [h for h in hashtags if h]

    body_text = markdown_to_plain_text(body)
    final_text = "\n".join(([
        " ".join(hashtags),
        "",
    ] if hashtags else []) + [body_text]).strip()

    note_title = str(meta.get("title") or markdown_path.stem)

    if args.msg_type == "text":
        payload = build_text_payload(final_text)
    else:
        payload = build_post_payload(title=note_title, text=final_text)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    unique_id = args.unique_id or build_unique_suffix()
    payload_path = output_dir / f"{args.name_prefix}.{unique_id}.payload.json"
    send_script_path = output_dir / f"{args.name_prefix}.{unique_id}.send.sh"

    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    send_script_path.write_text(
        make_send_script_text(
            payload_path=payload_path,
            webhook_env=args.webhook_env,
            secret_env=args.secret_env,
        ),
        encoding="utf-8",
    )
    send_script_path.chmod(0o755)

    print(f"generated payload: {payload_path}")
    print(f"generated script:  {send_script_path}")


if __name__ == "__main__":
    main()
