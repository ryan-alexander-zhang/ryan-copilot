# Context Hub BYOD Notes

Use this file when you need the local private-registry workflow.

## Local build flow

1. Create a content directory containing `author/docs/.../DOC.md` and optional `references/`.
2. Build it into a local registry with `chub build`.
3. Point `~/.chub/config.yaml` at the build output with a `path` source.
4. Use `chub search` and `chub get` across both community and private sources.

## Example config

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1
  - name: internal
    path: /path/to/my-content/dist
```

## Example local test commands

```bash
chub build my-content -o my-content/dist
chub search "internal-api"
chub get mycompany/internal-api
```

## Collision handling

If a private ID collides with a public ID, fetch with a source prefix:

```bash
chub get internal:mycompany/internal-api
chub get community:openai/chat
```

