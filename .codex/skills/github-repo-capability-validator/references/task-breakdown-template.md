# Task Breakdown Template

Use this template to create `00-task-breakdown.md`.

## Repository Analysis Task Breakdown

- Repository:
- Analysis scope:
- Local clone path:
- Branch or ref:
- Commit:
- Report bundle path:

## Task List

| Task ID | File | Goal | Inputs | Depends On | Status |
| --- | --- | --- | --- | --- | --- |
| T00 | `00-task-breakdown.md` | Record the decomposition and execution order | README, repo metadata | none | completed |
| T01 | `01-readme-capability-extraction.md` | Extract project positioning and normalized capabilities from README only | README | T00 | pending |
| T02 | `02-entrypoints-and-main-flow.md` | Establish shared code-reading skeleton: entrypoints, orchestration, main flow, key modules | local clone | T01 | pending |
| T03+ | `NN-capability-<name>.md` or `NN-scope-<scope>.md` | Verify one capability or one scoped investigation unit against code | README extraction, shared skeleton | T01, T02 | pending |
| T99 | `99-final-consistency-summary.md` | Summarize validation status, mismatches, risks, and next reading paths | all prior tasks | all prior tasks | pending |

## Decomposition Rules

- Prefer one shared task for entrypoints and main-flow analysis before capability-specific deep dives.
- Create one capability task per normalized capability in full-audit mode.
- In scoped-audit mode, create one scoped deep-dive task for each explicitly requested investigation unit instead of pretending to cover all extracted capabilities.
- Reuse evidence from T02 instead of repeating the same code-reading in every capability file.
- Keep each task document reviewable on its own.

## Notes

- Track blockers, external dependencies, and uncertain areas here.
- Update task status as analysis progresses.
