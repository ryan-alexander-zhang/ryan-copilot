---
name: github-repo-capability-validator
description: "Analyze a GitHub repository or a user-scoped capability slice from a strict README-first workflow: clone locally, extract claimed core capabilities from the README, decompose the work into reviewable task documents, produce shared and per-capability or per-scope technical analyses, verify each claim against the checked out codebase, and write an evidence-backed consistency report bundle."
---

# GitHub Repo Capability Validator

## Purpose

Analyze a GitHub repository by first extracting the project's claimed core capabilities from the README, then generating task-oriented technical analysis documents, and finally validating each analysis against the actual source code.

The default mode is a full repository capability audit. However, if the user explicitly narrows the ask to a subset such as a single capability, request path, command flow, API lifecycle, or create/update/delete chain, switch into a scoped audit mode while preserving the same README-first discipline.

This skill is designed to prevent shallow README paraphrasing. It enforces a strict path:

`clone -> README claims -> capability extraction -> task breakdown -> shared main-flow analysis -> per-capability technical analysis -> code verification -> consistency report bundle`

The reports should be strong enough to help a reader reconstruct how the product works, not just restate README claims. Prefer concrete explanations of implementation mechanics, state flow, data flow, storage, and external dependency boundaries.

## Inputs

Collect these inputs when available:

- `repo_url`: GitHub repository URL.
- `readme_content`: README text or README file path.
- `repo_root` or checked out source tree.
- Optional `analysis_scope`: a user-declared subset such as one capability, one control-plane chain, one API flow, one command path, or one bounded architecture slice.
- Optional `scope_slug`: a short filesystem-safe slug derived from `analysis_scope` for report naming when scoped mode is active.
- `report_output_dir`: fixed report directory in the current workspace. Default: `reports/`.
- `report_filename`: default `<repo-name>-capability-audit.md`, or `<repo-name>-capability-audit-<scope-slug>.md` in scoped mode.
- `report_bundle_dir`: default `reports/<repo-name>-capability-audit/`, or `reports/<repo-name>-capability-audit-<scope-slug>/` in scoped mode.
- Optional `docs/`, configuration files, interface definitions, and key entrypoints.
- Optional permission to inspect GitHub pull requests with `gh` for recent implementation context.

## Safety Policy

Default to static analysis only.

- You may clone the repository locally for inspection.
- Do read README, docs, configuration, manifests, tests, and source files.
- Do not install dependencies by default.
- Do not run tests, builds, package managers, project scripts, containers, binaries, or application code by default.
- Do not execute repository code just because it would improve confidence.
- Only run repository-affecting or code-executing commands when the user explicitly asks for runtime verification or clearly authorizes execution for that turn.
- If runtime execution is not authorized, report that validation is based on static inspection only.
- If runtime execution is authorized, prefer the narrowest command set needed and call out security risk from untrusted repository code before or while requesting approval when required.

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
- Detect whether the user requested a full audit or a scoped audit.
- In full-audit mode, derive the report filename from the repository name using this fixed convention: `<repo-name>-capability-audit.md`.
- In full-audit mode, derive the report bundle directory from the repository name using this fixed convention: `<repo-name>-capability-audit/`.
- In scoped-audit mode, derive a short `scope_slug` from the user request and use `<repo-name>-capability-audit-<scope-slug>.md` and `reports/<repo-name>-capability-audit-<scope-slug>/`.
- Keep the README extraction repository-wide even in scoped mode unless the user explicitly asks to skip repository-wide README extraction.
- Create a task breakdown document before deep code verification so the work is explicitly decomposed.

### Stage 1: Extract Claimed Core Capabilities From README Only

Do not inspect source code before finishing this stage.

Produce:

- One-sentence project positioning.
- `3-8` core capabilities when supported by README. Output fewer
  only if the README genuinely exposes fewer.
- README evidence for each capability.
- Boundary note for each capability: `what it is / what it is not`.
- When `analysis_scope` is provided, also produce a short `Scoped audit target` section that maps the requested scope back to one or more README-derived capabilities without pretending the scoped target came directly from README wording if it did not.

Use these extraction rules:

- Focus on the problem solved, explicitly claimed main functions,
  external-facing scenarios, unique value, and architecture-level
  traits.
- Merge overlapping abilities.
- Exclude installation steps, badges, test commands, CI/CD,
  dependency names, roadmap items, and experimental toggles unless
  the README presents them as default, central behavior.
- Treat marketing language as a claim, not a fact.

### Stage 2: Write One Technical Analysis Per Capability Or Scoped Investigation Unit

Create one independent section or document per capability in full-audit mode. In scoped-audit mode, create one independent section or document per scoped investigation unit. Use the
fixed structure from `references/report-template.md`.

When README details are incomplete:

- infer cautiously;
- label the statement `based on README inference`;
- reduce confidence.

Prefer concise architecture and flow diagrams in Mermaid when the
repository is large enough to benefit.

Default to using diagrams when the evidence is strong enough to support them.

Prefer these visualization forms:

- `Mermaid flowchart` for architecture and module relationships
- `Mermaid sequenceDiagram` for request, execution, or orchestration flow
- `Mermaid stateDiagram-v2` for state or lifecycle transitions
- `Mermaid classDiagram` or entity-style diagrams for data and storage structures when helpful

If a useful diagram cannot be supported by evidence, say so instead of fabricating one.

For each capability, explicitly cover these implementation angles when evidence exists:

- what technologies or frameworks are used
- how execution or state transitions flow
- how data enters, transforms, and exits the system
- where data is stored, cached, indexed, or persisted
- what a minimal rebuild of the capability would require

The goal is not only validation. The goal is also to make the capability understandable enough that a reader could plausibly reproduce the product design from the report.

Before capability deep dives, write a task breakdown document that decomposes the work into:

- README-only extraction task
- entrypoints and main-flow task
- one task per capability in full-audit mode, or one task per scoped investigation unit in scoped-audit mode
- final consistency summary task

Prefer task decomposition by investigation stage, not only by capability name, so shared code-reading work is done once and reused.

Scoped-audit rules:

- Do not silently expand a user-scoped request back into a full implementation audit.
- Do keep Stage 1 anchored in README-level repository capabilities so the scoped deep dive still has documented grounding.
- Do make `02-entrypoints-and-main-flow.md` explicitly scoped when the user asked for a scoped flow.
- Do make the deep-dive filename and report bundle name reflect the scoped target when scoped mode is active.
- Do say clearly which adjacent subsystems are intentionally out of scope.

### Stage 3: Verify Against Code

Return to the repository and verify each analysis using:

- directory structure;
- public interfaces;
- configuration;
- core modules;
- classes, functions, handlers, services, pipelines, prompts,
  schemas, or workflow definitions.

By default, perform this stage through static code verification only.
Do not treat dependency installation, test execution, builds, or running repository programs as part of the default workflow.
Only add runtime verification when the user explicitly requests it.

For each capability, explicitly report:

- code locations that support or refute it;
- which README claims are implemented;
- which are only partially implemented;
- which are not verified;
- `README claim / code reality / likely reason for mismatch` when they differ.

When the code supports it, also verify:

- concrete technology choices
- state or lifecycle transitions
- data model and storage boundaries
- key external-service dependencies
- minimum modules required to rebuild the capability

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

Add a validation status to each capability. This is required.

Use one of:

- `Validated`
- `Partially Validated`
- `Insufficient Evidence`
- `README Claim Not Supported`
- `Implemented but Under-Documented`

Evidence grade is optional but recommended when it improves rigor.

Suggested evidence grades:

- `A`: README and code both clearly support the conclusion
- `B`: code supports it, but README is vague
- `C`: README strongly claims it, but code only partially supports it
- `D`: only README mentions it, code does not support it

When README and code differ, add a mismatch classification. This is required when a mismatch exists.

Use one of:

- `README described, code not implemented`
- `README described, code partially implemented`
- `code implemented, README under-describes it`
- `same meaning, different naming`
- `depends on external platform or service, cannot be fully verified in repo`
- `placeholder or scaffolding only`
- `roadmap mistakenly presented as present capability`

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

Runtime heuristics are opt-in only:

- If the user has not explicitly authorized execution, do not run `npm install`, `pnpm install`, `yarn`, `pip install`, `poetry install`, `cargo build`, `go test`, `pytest`, `npm test`, `make`, `docker`, project binaries, or repository scripts.
- In the default mode for this skill, tests may be read as evidence but not executed.
- When execution is authorized, keep it minimal and relevant to the claimed capability being verified.

## Output Contract

Always deliver:

1. A task breakdown document in `report_output_dir/<bundle-name>/00-task-breakdown.md`.
2. A README-only extraction document in `report_output_dir/<bundle-name>/01-readme-capability-extraction.md`.
3. An entrypoints and main-flow document in `report_output_dir/<bundle-name>/02-entrypoints-and-main-flow.md`.
4. One capability document per capability in full-audit mode, or one scoped deep-dive document per scoped investigation unit in scoped-audit mode, in `report_output_dir/<bundle-name>/` using a stable numbered filename such as `03-capability-<name>.md` or `03-scope-<scope-slug>.md`.
5. A final overview report with:
   - capability summary table
   - verification status per capability
   - overall README/code consistency judgment
   - key risks
   - five priority code entrypoints for deeper study
6. A final summary document in `report_output_dir/<bundle-name>/99-final-consistency-summary.md`.

Where `<bundle-name>` is:

- `<repo-name>-capability-audit` in full-audit mode
- `<repo-name>-capability-audit-<scope-slug>` in scoped-audit mode

The single-file report `report_output_dir/<bundle-name>.md` is optional. Prefer the task-oriented report bundle as the default output.

Each capability analysis must include:

- confidence
- validation status
- mismatch classification when applicable
- evidence grade when useful
- implementation mechanics
- state and lifecycle analysis when applicable
- data and storage analysis when applicable
- rebuildability notes
- diagrams by default when supported by evidence

Keep the report structured, auditable, and easy to hand off to another agent.

## Constraints

Enforce these constraints:

- Do not skip local clone when analyzing a remote GitHub repository.
- Do not continue to Stage 3 if clone fails.
- Do not write the generated report into the analyzed repository by default.
- Do write the generated report into the current workspace's fixed report directory by default.
- Do use the fixed filename pattern `<repo-name>-capability-audit.md` by default.
- Do use the fixed multi-file report bundle directory `<repo-name>-capability-audit/` by default.
- Do switch to `<repo-name>-capability-audit-<scope-slug>.md` and `<repo-name>-capability-audit-<scope-slug>/` when the user explicitly requested a scoped audit.
- Do create `00-task-breakdown.md` before deep verification work.
- Do decompose work into reviewable task documents with smaller scope.
- Do not backfill capability definitions from code during Stage 1.
- Do not let scoped mode rename a repository-wide README extraction into a fake scoped README.
- Do make scoped deep-dive filenames, summary text, and bundle names visibly reflect the declared scope.
- Do not treat tooling or peripheral features as core capabilities.
- Do not present README claims as facts until code verification is complete.
- Do not hide mismatches; state them explicitly.
- Do not over-claim architecture details when the repository lacks evidence.
- Call out external-service dependencies when a claimed capability
  only works with SaaS or remote systems.
- Do not use pull requests as the main evidence for a capability when the default-branch code does not confirm it.
- Do prefer concrete implementation explanation over abstract summary when the code supports it.
- Do distinguish clearly between proven implementation, cautious inference, and unknowns.
- Do default to non-executing static inspection and say so in the report when no runtime authorization was provided.
- Do not install dependencies, run tests, build artifacts, or execute repository code unless the user explicitly requested runtime verification.
- Do attempt visual explanation by default when the repository structure supports it.
- Do not invent diagrams that cannot be justified from README and code evidence.

For large repositories, prioritize analysis in this order:

1. README-described main flows
2. entrypoint modules
3. orchestration layer
4. core engine or execution layer
5. infra or adapter layer
6. tests that prove behavior

If the repository cannot be fully analyzed, explicitly state why.
Common reasons include:

- README too vague
- missing source code for a key capability
- capability depends on a hosted service not present in the repo
- code layout too fragmented to verify efficiently
- examples exist but the production path is unclear

In those cases, still provide:

- best-effort capability extraction
- partial evidence
- uncertainty notes
- recommended next files to inspect

If the repository is intentionally only partially analyzed because the user declared a narrow scope, explicitly state that this was a user-requested scope boundary, not a failure of the skill.

## Resource Files

- `references/report-template.md`: fixed document skeleton,
  evidence checklist, and Mermaid suggestions.
- `references/task-breakdown-template.md`: template for decomposing the analysis into reviewable tasks.
- `references/entrypoints-main-flow-template.md`: template for the shared entrypoint and main-flow investigation.
