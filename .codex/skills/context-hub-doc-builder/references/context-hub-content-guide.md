# Context Hub Content Guide Notes

Use this file when you need the required content layout or frontmatter rules.

## Required structure

- Group entries by author, then by `docs/` or `skills/`.
- For docs, the main file is `DOC.md`.
- For skills, the main file is `SKILL.md`.
- Place additional material beside the entry file, usually in `references/`.

Examples:

```text
my-content/acme/docs/widgets/DOC.md
my-content/acme/docs/widgets/references/errors.md
my-content/acme/docs/sdk/python/DOC.md
my-content/acme/docs/sdk/javascript/DOC.md
my-content/acme/docs/api/v1/DOC.md
my-content/acme/docs/api/v2/DOC.md
my-content/acme/skills/deploy/SKILL.md
```

## DOC.md frontmatter

Use YAML frontmatter with these required fields:

- `name`
- `description`
- `metadata.languages`
- `metadata.versions`
- `metadata.revision`
- `metadata.updated-on`
- `metadata.source`

Optional:

- `metadata.tags`

## Practical conventions

- Use `text` for a generic internal narrative doc with no SDK language.
- Use `http` for OpenAPI or Swagger material that documents raw API calls rather than a client SDK.
- Use a real SDK language such as `python` or `javascript` when the content is language-specific.
- Keep `revision` monotonic. Start at `1`.
- Update `updated-on` whenever you materially revise the content.
- Use `official`, `maintainer`, or `community` for `metadata.source`.

## Layout decisions

- Use a direct `DOC.md` for a single variant.
- Add a language directory only when the same entry has multiple language-specific variants.
- Add a version directory only when the material has distinct breaking versions that should be fetched separately.

## Build commands

```bash
chub build my-content --validate-only
chub build my-content -o dist
```

## Retrieval reminders

```bash
chub search "widgets"
chub get acme/widgets
chub get acme/widgets --full
chub get acme/widgets --file references/errors.md
```

