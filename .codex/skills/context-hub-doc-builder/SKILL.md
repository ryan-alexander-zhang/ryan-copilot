---
name: context-hub-doc-builder
description: Generate private Context Hub docs and local content trees from URLs, OpenAPI or Swagger specs, and local files. Use when asked to create internal `chub` docs, infer `author/docs/<entry>/DOC.md` structure, scaffold Context Hub frontmatter, build a private registry with `chub build`, or print test CLI commands for `chub search` and `chub get`.
---

# Context Hub Doc Builder

## Overview

Turn source material into a local Context Hub content directory that can be built and consumed by `chub`.

Prefer this skill when the user wants internal docs, private registries, or repeatable `Context Hub` content from mixed inputs such as:

- product or API docs URLs
- OpenAPI or Swagger JSON/YAML
- local Markdown, text, JSON, YAML, or code files

## Inputs

Collect these inputs when available:

- `content_root`: root content directory to build, for example `my-content/`
- `author`: vendor or org slug used in `author/docs/...`
- `entry_name`: entry slug; infer from source title when absent
- `source_inputs`: one or more URLs or local file paths
- `description`: short search-friendly summary
- `language`: doc variant label
- `version`: package, SDK, API, or internal doc version
- `source_trust`: one of `official`, `maintainer`, `community`
- `tags`: comma-separated tags

Use these defaults when the user does not specify them:

- `language=text` for generic internal docs
- `language=http` for OpenAPI or Swagger API docs
- `source_trust=maintainer` for first-party internal material
- `revision=1`

If no trustworthy version can be inferred, ask for one instead of inventing it. Only use a placeholder when the user explicitly accepts that tradeoff.

## Workflow

### 1. Classify the source

Decide whether the material is:

- a general documentation URL
- an OpenAPI or Swagger spec
- a local file set
- a mixed bundle that needs one main `DOC.md` plus `references/`

For OpenAPI or Swagger sources, prefer extracting `info.title`, `info.version`, `info.description`, and server URLs from the spec.

For URLs, fetch only the relevant page content. Prefer `curl -L <url>` for raw Markdown, JSON, YAML, or HTML endpoints. For local files, read the minimum set needed to draft the main doc and references.

### 2. Decide the content layout

Follow Context Hub layout rules:

- Single doc: `author/docs/entry-name/DOC.md`
- Multi-language: `author/docs/entry-name/<language>/DOC.md`
- Multi-version: `author/docs/entry-name/<version-dir>/DOC.md`
- Combined version and language: `author/docs/entry-name/<version-dir>/<language>/DOC.md`

Use a direct `DOC.md` by default. Add language or version subdirectories only when the material clearly has multiple variants.

Keep one main `DOC.md` for the common path. Move long examples, endpoint catalogs, auth notes, or edge cases into `references/`.

### 3. Scaffold the entry

Use `scripts/scaffold_context_hub_doc.py` to create the directory, frontmatter, and starter body:

```bash
python3 scripts/scaffold_context_hub_doc.py \
  --content-root my-content \
  --author mycompany \
  --entry-name internal-api \
  --source-input ./openapi.yaml \
  --language http \
  --version 2.0.0 \
  --source-trust official \
  --tag internal \
  --tag api
```

The script:

- infers missing metadata from OpenAPI or simple source files when possible
- creates the correct `DOC.md` path
- writes required frontmatter
- creates a `references/` directory
- prints suggested `chub build`, `chub search`, and `chub get` commands

If the source already includes trustworthy metadata, preserve it. Do not overwrite a real title, version, or description with a weaker guess.

### 4. Write `DOC.md` for LLM consumption

Keep the main doc compact and operational:

- start with what the system does
- show the happy path first
- include concrete request or code examples
- note auth, prerequisites, or environment assumptions early
- move long tables or deep edge cases into `references/`

Recommended outline:

1. What this entry covers
2. Quick start or first successful call
3. Common workflows
4. Important constraints
5. Reference file map

### 5. Add references

Create `references/` files when the source is large or split across topics. Common files:

- `references/auth.md`
- `references/endpoints.md`
- `references/errors.md`
- `references/examples.md`

Mention important reference files near the end of `DOC.md` so agents know they exist.

### 6. Validate and build

Run:

```bash
chub build <content_root> --validate-only
chub build <content_root> -o <dist_dir>
```

If validation fails, fix frontmatter or directory layout first. Do not claim the registry is ready until `--validate-only` passes.

### 7. Emit test CLI commands

Always finish by printing runnable commands for the new entry. Include:

```bash
chub build <content_root> --validate-only
chub build <content_root> -o <dist_dir>
chub search "<entry_name>"
chub get <author>/<entry_name>
chub get <author>/<entry_name> --full
```

If references exist, also print:

```bash
chub get <author>/<entry_name> --file references/<file-name>.md
```

When the user wants local usage, explicitly say that `~/.chub/config.yaml` requires a manual edit, then print the exact snippet that adds the built directory as a `path` source.

Also explain this tradeoff clearly:

- If `sources` contains only the local path source, `chub search` and `chub get` will only see local content.
- Public entries such as `search openai` will no longer appear unless the `community` source remains configured.
- Prefer printing two config options: local-only and local-plus-community.

## References

- Read `references/context-hub-content-guide.md` for the required content layout and frontmatter fields.
- Read `references/context-hub-byod-guide.md` for the local registry and config workflow.
