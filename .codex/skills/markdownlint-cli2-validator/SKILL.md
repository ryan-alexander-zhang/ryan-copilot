---
name: markdownlint-cli2-validator
description: Validate Markdown files with markdownlint-cli2, try automatic fixes first with `--fix`, then rerun lint and decide the result from the exit code. Use when asked to check Markdown formatting, explain markdownlint-cli2 failures, auto-fix lintable issues, or return the remaining lint report for `.md` files or Markdown-heavy directories.
---

# Markdownlint CLI2 Validator

## Inputs

Collect these inputs when available:

- file path, directory path, or glob to lint
- optional config file path
- whether to auto-fix before final reporting

Default to auto-fix first unless the user explicitly asks for read-only
validation.

## Workflow

Run the workflow in this order.

### 1. Confirm Tool Availability

Check whether `markdownlint-cli2` is installed:

```bash
command -v markdownlint-cli2
```

If it is missing, say that the tool is unavailable and stop. Do not
pretend validation ran.

### 2. Discover Target Markdown Files

If the user gives a directory, find Markdown files before linting.

Prefer:

```bash
rg --files <target> -g '*.md'
```

If the user already gives a precise file path or glob, use that
directly.

### 3. Try Automatic Fixes First

Unless the user disables fixing, run:

```bash
markdownlint-cli2 "<target>" --fix
```

Interpret the result carefully:

- exit code `0`: fixes applied or no issues remained after fixing
- exit code non-zero: some problems remain or are not auto-fixable

Do not stop after `--fix`. Always rerun lint once more to get the final
state.

### 4. Rerun Validation

Run the final check without `--fix`:

```bash
markdownlint-cli2 "<target>"
```

Use this final exit code as the source of truth.

### 5. Report Result

If the final exit code is `0`, report that validation passed.

If the final exit code is non-zero, return:

- that validation failed
- the final exit code
- the lint report
- a short summary of what auto-fix changed, if that is clear from the
  before/after results

When helpful, explain common rules with concrete bad/good examples, such
as:

- `MD032`: lists need blank lines around them
- `MD013`: lines are too long and usually need manual wrapping

## Output Contract

Prefer this shape:

```text
Checked: <target>
Auto-fix attempted: yes|no
Final exit code: <code>
Result: pass|fail
```

If failed, include the lint report verbatim or as a faithful plain-text
block so the user can act on it.

## Constraints

Follow these rules:

- base the final verdict on the second run without `--fix`
- do not claim success from the `--fix` run alone
- if lint fails, return the report instead of summarizing it away
- if only some issues were auto-fixed, say so
- do not invent markdownlint rules or meanings

## Examples

Lint one file:

```bash
markdownlint-cli2 "docs/guide.md" --fix
markdownlint-cli2 "docs/guide.md"
```

Lint a skill directory:

```bash
markdownlint-cli2 ".codex/skills/my-skill/**/*.md" --fix
markdownlint-cli2 ".codex/skills/my-skill/**/*.md"
```
