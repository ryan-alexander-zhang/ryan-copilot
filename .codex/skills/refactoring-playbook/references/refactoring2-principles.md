# Refactoring 2 Principles

## Table of Contents

- Scope
- Core definition
- Non-negotiables
- When to refactor
- When to hold back
- Testing, CI, and safety
- YAGNI and architecture
- Performance stance

## Scope

Use this file when deciding whether to refactor, how aggressive to be,
and what safety bar to require. This reference distills the guidance in
`book-refactoring2` chapters 2 and 4.

## Core Definition

Treat refactoring as a structural change that preserves observable
behavior.

Separate two activities:

- Add behavior.
- Improve structure.

Switch hats consciously. Do not hide behavior changes inside a cleanup
diff.

## Non-Negotiables

- Preserve observable behavior unless the user explicitly requests a bug
  fix or feature change.
- Prefer many small, behavior-safe steps over one large rewrite.
- Keep the code working between steps whenever possible.
- Use names and structure to make intent easier to read.
- Reduce the future cost of change, not just today's line count.

## When to Refactor

Refactor in these situations by default:

- Before adding a feature when a small structural change will make the
  feature easier to add.
- While trying to understand confusing code.
- While fixing a nearby mess that is cheap to improve.
- During code review when a concrete structural improvement is obvious.
- Over time across many small touches when a large subsystem needs
  gradual cleanup.

Apply the "third time" rule:

- First time: implement directly.
- Second time: notice the repetition.
- Third time: refactor.

## When to Hold Back

Hold back or narrow the scope when:

- The code has no meaningful safety net and the change would be deep.
- The requested outcome is really a behavior change, not a refactor.
- The fastest safe move is to add a seam or a test first.
- The team is under delivery pressure and the cleanup is not helping the
  current change.
- The code will be deleted or replaced very soon.

Avoid "planned refactor weeks" unless everyday opportunistic refactoring
has failed and pain has clearly accumulated.

## Testing, CI, and Safety

Treat automated tests as the foundation of reliable refactoring.

- Run tests frequently.
- Add characterization tests for legacy behavior when requirements are
  unclear.
- Keep CI green so refactors integrate quickly.
- Use tooling support for rename and signature changes, but still run
  tests around non-trivial edits.
- If reflection, code generation, dynamic dispatch, or runtime wiring is
  heavy, assume tooling can miss things.

When the code lacks tests, add the smallest useful behavior checks
before making deep structural moves.

## YAGNI and Architecture

Do not add flexibility just because future variation is imaginable.

- Add abstraction when current change pressure justifies it.
- Prefer simple, current-fit design plus good refactoring ability.
- Ask whether future refactoring would be genuinely hard; only then
  consider adding flexibility early.
- Favor preparatory refactoring over speculative frameworks.

For long-running architectural changes, use gradual migration patterns
such as branch by abstraction rather than all-at-once replacement.

## Performance Stance

Do not guess at performance.

- First, write code that is clear enough to optimize safely.
- Measure actual hotspots before making performance-driven structural
  tradeoffs.
- Optimize where data shows pressure, not where intuition feels nervous.
- Accept that some refactorings may slightly change runtime
  characteristics while still preserving user-visible behavior.

The default sequence is:

1. Make the code understandable.
2. Measure.
3. Optimize hotspots.
4. Re-measure.
