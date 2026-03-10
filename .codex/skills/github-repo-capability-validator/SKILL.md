---
name: github-repo-capability-validator
description: Extract a GitHub repository's claimed core capabilities from README content, write per-capability technical analysis documents, and verify every claim against the actual codebase. Use when asked to analyze a public or local repository from its README first, avoid capability backfilling from code, compare README claims with implementation, or produce structured evidence-backed capability reports with confidence ratings.
---

# GitHub Repo Capability Validator

## Inputs

Collect these inputs when available:

- `repo_url`: GitHub repository URL.
- `readme_content`: README text or README file path.
- `repo_root` or checked out source tree.
- `report_output_dir`: fixed report directory in the current workspace. Default: `reports/`.
- `report_filename`: default `<repo-name>-capability-audit.md`, derived from the analyzed repository name.
- Optional `docs/`, configuration files, interface definitions, and key entrypoints.
- Optional permission to inspect GitHub pull requests with `gh` for recent implementation context.

If the repository is not checked out locally, clone it locally before Stage 3.
If cloning fails, stop and report that code verification could not be completed.

## Workflow

Execute the work in three stages and keep them separate.

Before Stage 1:

- If `repo_root` is not already available locally, clone the repository first.
- Prefer a local checkout of the default branch.
- If clone fails for any reason, stop instead of falling back to webpage-only verification.
- You may read the README from GitHub before clone only when needed to identify the repository, but do not use webpage inspection as a substitute for a local code tree.
- Create the report output directory in the current workspace if it does not already exist.
- Plan to write the final Markdown report into the current workspace, not into the analyzed repository.
- Derive the report filename from the repository name using this fixed convention: `<repo-name>-capability-audit.md`.

### Stage 1: Extract Claimed Core Capabilities From README Only

Do not inspect source code before finishing this stage.

Produce:

- One-sentence project positioning.
- `3-8` core capabilities when supported by README. Output fewer
  only if the README genuinely exposes fewer.
- README evidence for each capability.
- Boundary note for each capability: `what it is / what it is not`.

Use these extraction rules:

- Focus on the problem solved, explicitly claimed main functions,
  external-facing scenarios, unique value, and architecture-level
  traits.
- Merge overlapping abilities.
- Exclude installation steps, badges, test commands, CI/CD,
  dependency names, roadmap items, and experimental toggles unless
  the README presents them as default, central behavior.
- Treat marketing language as a claim, not a fact.

### Stage 2: Write One Technical Analysis Per Capability

Create one independent section or document per capability. Use the
fixed structure from `references/report-template.md`.

When README details are incomplete:

- infer cautiously;
- label the statement `based on README inference`;
- reduce confidence.

Prefer concise architecture and flow diagrams in Mermaid when the
repository is large enough to benefit.

### Stage 3: Verify Against Code

Return to the repository and verify each analysis using:

- directory structure;
- public interfaces;
- configuration;
- core modules;
- classes, functions, handlers, services, pipelines, prompts,
  schemas, or workflow definitions.

For each capability, explicitly report:

- code locations that support or refute it;
- which README claims are implemented;
- which are only partially implemented;
- which are not verified;
- `README claim / code reality / likely reason for mismatch` when they differ.

Never invent modules, classes, functions, or call chains. If code
evidence is weak, say `insufficient to verify`.

Optional enhancement:

- Use `gh` to inspect relevant pull requests only after default-branch code verification is complete.
- Treat PRs as supporting evidence for implementation history or README drift, not as the primary proof of current capability.
- Do not mark a capability as implemented based on PR discussion alone when current code does not support it.

## Evidence Rules

Attach evidence to every conclusion:

- `README evidence`: quote or paraphrase the relevant README section.
- `Code evidence`: file path, module, class, function, config key,
  CLI command, route, or schema.
- `External evidence` only when allowed and useful. Prefer official project sources.

Add a confidence rating to each capability: `high`, `medium`, or `low`.

Use stronger confidence only when README and code line up cleanly.

## Verification Heuristics

Use fast repository inspection first:

- local clone or existing local checkout
- `rg --files`
- `rg "<capability keyword>|<domain term>|<config key>"`
- targeted reads of README, docs, config, and entrypoints

Then optionally deepen verification with:

- `gh pr list` / `gh pr view` for capability-related implementation history
- recent merged PRs when README claims and current code appear misaligned

Validate behavior through implementation markers such as:

- API routes or CLI commands
- orchestrators or workflow engines
- adapters, plugins, registries, loaders
- model or retrieval pipelines
- code generation templates
- rules, policies, evaluators, schedulers
- tests that prove the capability is intended to work

Treat tests and docs as supporting evidence, not a replacement for implementation.
Treat PRs the same way: supporting evidence, never a replacement for implementation in the checked out code.

## Output Contract

Always deliver:

1. README-only capability extraction.
2. One full analysis per capability.
3. A final overview report with:
   - capability summary table
   - verification status per capability
   - overall README/code consistency judgment
   - key risks
   - five priority code entrypoints for deeper study
4. Write the complete report to `report_output_dir/<repo-name>-capability-audit.md` under the current workspace.

Keep the report structured, auditable, and easy to hand off to another agent.

## Constraints

Enforce these constraints:

- Do not skip local clone when analyzing a remote GitHub repository.
- Do not continue to Stage 3 if clone fails.
- Do not write the generated report into the analyzed repository by default.
- Do write the generated report into the current workspace's fixed report directory by default.
- Do use the fixed filename pattern `<repo-name>-capability-audit.md` by default.
- Do not backfill capability definitions from code during Stage 1.
- Do not treat tooling or peripheral features as core capabilities.
- Do not present README claims as facts until code verification is complete.
- Do not hide mismatches; state them explicitly.
- Do not over-claim architecture details when the repository lacks evidence.
- Call out external-service dependencies when a claimed capability
  only works with SaaS or remote systems.
- Do not use pull requests as the main evidence for a capability when the default-branch code does not confirm it.

## Resource Files

- `references/report-template.md`: fixed document skeleton,
  evidence checklist, and Mermaid suggestions.
