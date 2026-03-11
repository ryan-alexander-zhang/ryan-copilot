#!/usr/bin/env python3
"""
Create a Context Hub DOC.md scaffold from URLs, OpenAPI/Swagger specs, or local files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any


TRUST_LEVELS = {"official", "maintainer", "community"}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-") or "entry"


def titleize(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def looks_like_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def load_text(source: str) -> str:
    if looks_like_url(source):
        with urllib.request.urlopen(source) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    return Path(source).read_text(encoding="utf-8")


def try_parse_yaml(text: str) -> Any | None:
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    return yaml.safe_load(text)


def parse_structured_source(text: str) -> Any | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return try_parse_yaml(text)


def detect_openapi_payload(payload: Any) -> bool:
    return isinstance(payload, dict) and "info" in payload and (
        "openapi" in payload or payload.get("swagger") == "2.0"
    )


def first_sentence(text: str | None) -> str | None:
    if not text:
        return None
    collapsed = " ".join(text.strip().split())
    if not collapsed:
        return None
    match = re.match(r"(.+?[.!?])(?:\s|$)", collapsed)
    return match.group(1) if match else collapsed[:160]


def infer_from_openapi(source: str) -> dict[str, Any]:
    text = load_text(source)
    payload = parse_structured_source(text)
    if not detect_openapi_payload(payload):
        return {}

    info = payload.get("info", {})
    title = info.get("title")
    version = str(info.get("version")) if info.get("version") is not None else None
    description = first_sentence(info.get("description") or info.get("summary"))
    servers = []
    for server in payload.get("servers", []):
        url = server.get("url")
        if url:
            servers.append(url)
    tags = [slugify(item.get("name", "")) for item in payload.get("tags", []) if item.get("name")]

    return {
        "title": title,
        "entry_name": slugify(title) if title else None,
        "description": description,
        "version": version,
        "language": "http",
        "server_urls": servers,
        "tags": [tag for tag in tags if tag],
        "source_kind": "openapi",
    }


def infer_from_url(source: str) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(source)
    leaf = Path(parsed.path).name or parsed.netloc
    stem = Path(leaf).stem or parsed.netloc
    entry_name = slugify(stem)
    return {
        "entry_name": entry_name,
        "title": titleize(entry_name),
        "source_kind": "url",
    }


def infer_from_file(source: str) -> dict[str, Any]:
    path = Path(source)
    entry_name = slugify(path.stem)
    extension = path.suffix.lower()
    language = "text"
    if extension in {".py"}:
        language = "python"
    elif extension in {".js", ".mjs", ".cjs", ".ts"}:
        language = "javascript"
    elif extension in {".java"}:
        language = "java"
    elif extension in {".go"}:
        language = "go"
    return {
        "entry_name": entry_name,
        "title": titleize(entry_name),
        "language": language,
        "source_kind": "file",
    }


def infer_metadata(sources: list[str]) -> dict[str, Any]:
    merged: dict[str, Any] = {"tags": [], "server_urls": []}
    for source in sources:
        candidate: dict[str, Any] = {}
        if looks_like_url(source):
            if any(token in source.lower() for token in ("openapi", "swagger", ".json", ".yaml", ".yml")):
                candidate = infer_from_openapi(source)
                if not candidate:
                    candidate = infer_from_url(source)
            else:
                candidate = infer_from_url(source)
        else:
            path = Path(source)
            if path.suffix.lower() in {".json", ".yaml", ".yml"}:
                candidate = infer_from_openapi(source)
                if not candidate:
                    candidate = infer_from_file(source)
            else:
                candidate = infer_from_file(source)

        for key, value in candidate.items():
            if key in {"tags", "server_urls"}:
                merged.setdefault(key, [])
                for item in value:
                    if item not in merged[key]:
                        merged[key].append(item)
            elif value and not merged.get(key):
                merged[key] = value
    return merged


def render_frontmatter(args: argparse.Namespace, metadata: dict[str, Any]) -> str:
    tags = sorted({tag for tag in metadata.get("tags", []) + args.tag if tag})
    lines = [
        "---",
        f"name: {args.entry_name}",
        f'description: "{args.description}"',
        "metadata:",
        f"  languages: \"{args.language}\"",
        f"  versions: \"{args.version}\"",
        f"  revision: {args.revision}",
        f'  updated-on: "{args.updated_on}"',
        f"  source: {args.source_trust}",
    ]
    if tags:
        lines.append(f'  tags: "{",".join(tags)}"')
    lines.append("---")
    return "\n".join(lines)


def render_body(args: argparse.Namespace, metadata: dict[str, Any]) -> str:
    title = args.title
    bullet_sources = "\n".join(f"- `{item}`" for item in args.source_input)
    reference_lines = [
        "- Add `references/auth.md` for auth and permission models.",
        "- Add `references/examples.md` for longer request and response examples.",
        "- Add `references/errors.md` for error handling and troubleshooting.",
    ]
    if metadata.get("source_kind") == "openapi":
        reference_lines.insert(0, "- Add `references/endpoints.md` for endpoint and schema details.")

    server_block = ""
    if metadata.get("server_urls"):
        server_block = "\n## Known Base URLs\n\n" + "\n".join(
            f"- `{url}`" for url in metadata["server_urls"]
        )

    return f"""# {title}

## What This Covers

{args.description}

## Source Material

{bullet_sources}

## Quick Start

Replace this section with the shortest path to a successful first use. Prefer one request, one command, or one code sample that works end to end.

## Common Workflows

- Add the top 3-5 workflows the agent will need most often.
- Put the happy path first.
- Keep branchy edge cases in `references/`.
{server_block}

## Constraints

- Document auth, required headers, environment variables, and role assumptions.
- Call out rate limits, pagination, idempotency, or file-size limits if they matter.

## Reference Files

{chr(10).join(reference_lines)}
"""


def print_commands(args: argparse.Namespace, doc_dir: Path) -> None:
    content_root = Path(args.content_root)
    dist_dir = Path(args.output_dir) if args.output_dir else content_root / "dist"
    doc_id = f"{args.author}/{args.entry_name}"
    print("\nSuggested CLI commands:\n")
    print(f"chub build {content_root} --validate-only")
    print(f"chub build {content_root} -o {dist_dir}")
    print(f'chub search "{args.entry_name}"')
    print(f"chub get {doc_id}")
    print(f"chub get {doc_id} --full")
    print(f"chub get {doc_id} --file references/examples.md")
    print("\nManual config step:\n")
    print("Edit ~/.chub/config.yaml manually.")
    print("If you keep only the local source, chub search/get will only see local entries.")
    print("That means public lookups such as `chub search \"openai\"` may stop returning community results.")
    print("Keep the community source as well if you want both public and local content.\n")
    print("Option 1: local only\n")
    print("sources:")
    print(f'  - name: {args.author}')
    print(f"    path: {dist_dir}")
    print("\nOption 2: local plus community\n")
    print("sources:")
    print('  - name: community')
    print("    url: https://cdn.aichub.org/v1")
    print(f'  - name: {args.author}')
    print(f"    path: {dist_dir}")
    print(f"\nCreated DOC.md: {doc_dir / 'DOC.md'}")


def build_doc_dir(args: argparse.Namespace) -> Path:
    base = Path(args.content_root) / args.author / "docs" / args.entry_name
    if args.version_dir:
        base = base / args.version_dir
    if args.language_dir:
        base = base / args.language
    return base


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a Context Hub DOC.md entry and print test CLI commands."
    )
    parser.add_argument("--content-root", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--entry-name")
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--language")
    parser.add_argument("--version")
    parser.add_argument("--revision", type=int, default=1)
    parser.add_argument("--updated-on", dest="updated_on", default=str(date.today()))
    parser.add_argument("--source-trust", choices=sorted(TRUST_LEVELS), default="maintainer")
    parser.add_argument("--source-input", action="append", default=[], required=True)
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--output-dir")
    parser.add_argument("--version-dir", help="Optional directory name such as v1 or v2.")
    parser.add_argument(
        "--language-dir",
        action="store_true",
        help="Create a language subdirectory like author/docs/entry/python/DOC.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = infer_metadata(args.source_input)

    args.entry_name = args.entry_name or metadata.get("entry_name")
    if not args.entry_name:
        print("error: could not infer entry name; pass --entry-name", file=sys.stderr)
        return 1
    args.entry_name = slugify(args.entry_name)

    args.title = args.title or metadata.get("title") or titleize(args.entry_name)
    args.description = args.description or metadata.get("description")
    if not args.description:
        print("error: could not infer description; pass --description", file=sys.stderr)
        return 1

    args.language = args.language or metadata.get("language") or "text"
    args.version = args.version or metadata.get("version")
    if not args.version:
        print("error: could not infer version; pass --version", file=sys.stderr)
        return 1

    doc_dir = build_doc_dir(args)
    references_dir = doc_dir / "references"
    references_dir.mkdir(parents=True, exist_ok=True)

    frontmatter = render_frontmatter(args, metadata)
    body = render_body(args, metadata)
    doc_path = doc_dir / "DOC.md"
    doc_path.write_text(frontmatter + "\n\n" + body, encoding="utf-8")

    print_commands(args, doc_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
