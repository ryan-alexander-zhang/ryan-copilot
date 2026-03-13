---
name: refactoring-playbook
description: >-
  Refactor existing code with behavior-preserving, book-driven guidance
  focused on diagnosing code smells, choosing small safe refactoring
  steps, and improving readability, modularity, and changeability
  without rewriting from scratch. Use when Codex needs to clean up a
  function, class, module, or API; remove duplication; simplify
  conditionals; split large units; reduce coupling; add characterization
  tests before structural edits; or turn a vague maintainability concern
  into a concrete refactoring plan. Trigger on requests such as refactor
  this code, clean up this method, improve maintainability, remove code
  smells, simplify this class, restructure without changing behavior, or
  Chinese requests like 重构这段代码、消除坏味道、优化这段实现、拆分大函数、减少重复代码、去掉 switch 地狱、在不改行为的前提下整理代码.
---

# Refactoring Playbook

## Overview

Use this skill to turn "this code feels wrong" into a small, explicit,
behavior-preserving refactoring sequence. Base the first version of this
skill on the `MwumLi/book-refactoring2` repository, and keep the
structure ready for later book-derived references.

Read these reference files only when needed:

- [references/refactoring2-principles.md](references/refactoring2-principles.md)
- [references/refactoring2-smells.md](references/refactoring2-smells.md)
- [references/refactoring2-techniques.md](references/refactoring2-techniques.md)

## Working Mode

Assume the goal is structural improvement with unchanged observable
behavior unless the user explicitly asks for a bug fix or feature
change.

Separate these modes clearly:

- Refactor: preserve behavior and improve structure.
- Bug fix: intentionally change behavior to correct an error.
- Feature work: intentionally add new behavior.

If the request mixes them, state which edits are structural and which
edits change behavior. Avoid presenting feature work as refactoring.

## Refactoring Workflow

### 1. Establish the safety boundary

- Inspect tests, type checks, linters, build steps, and runtime
  contracts before editing.
- Add or strengthen characterization tests when the code lacks a
  reliable safety net.
- Keep each step small enough that tests or checks can validate it
  quickly.
- Prefer a sequence of stable micro-steps over one large rewrite.

Load [references/refactoring2-principles.md](references/refactoring2-principles.md)
when deciding whether to refactor now, how aggressive to be, or how to
balance YAGNI, testing, and performance concerns.

### 2. Diagnose the dominant smell

- Inspect the smallest useful unit first: function, method, class,
  module, or public API seam.
- Name the dominant smell or the smallest coherent smell cluster.
- Avoid chasing every imperfection in one pass.
- Prefer one clear reason for change over a grab bag of cleanup edits.

Load [references/refactoring2-smells.md](references/refactoring2-smells.md)
when the smell is unclear or when several smells overlap.

### 3. Choose the smallest useful moves

- Favor named, well-understood refactorings over ad hoc rewrites.
- Stack small moves such as rename, extract, inline, move, or split
  before introducing new abstractions.
- Use tooling support for safe renames and signature changes when the
  language and editor support it.
- Prefer deleting bad indirection to adding speculative indirection.

Load [references/refactoring2-techniques.md](references/refactoring2-techniques.md)
when selecting concrete refactorings.

### 4. Execute incrementally

- Make one meaningful structural change at a time.
- Re-run the narrowest relevant checks after each meaningful cluster of
  edits.
- Stop once the target smell is materially reduced and the code is
  easier to understand and modify.
- Do not keep polishing after the current change becomes easy.

### 5. Report the result

- State the starting smell.
- State the refactorings chosen.
- State the safety checks that were run.
- State residual risks, deferred smells, or missing tests.

## Decision Rules

- Prefer "make the next change easy" over speculative future-proofing.
- Prefer local clarity over generic frameworks that are not yet needed.
- Prefer explicit names over comments that explain obscure code.
- Prefer queries over mutable cached state when the value can be derived.
- Prefer moving behavior toward the data it depends on.
- Prefer splitting phases when different concerns happen in sequence.
- Prefer characterization tests before deep edits to legacy code.

## Smell Triage Hints

Use these shortcuts before loading the full smell reference:

- Suspect `Long Function` when a function needs comments to explain what
  blocks do.
- Suspect `Duplicated Code` when the same fix will need to be applied in
  more than one place.
- Suspect `Large Class` or `Divergent Change` when unrelated reasons
  force edits in the same class.
- Suspect `Shotgun Surgery` when one requirement change touches many
  files with small edits.
- Suspect `Feature Envy` when a function spends most of its time pulling
  data from another object.
- Suspect `Repeated Switches` when the same conditional branching logic
  appears in several places.
- Suspect `Data Clumps` or `Primitive Obsession` when the same basic
  values travel together through multiple calls.
- Suspect `Message Chains` when clients navigate deep object graphs.

## Reference Scope

Current coverage comes from the `MwumLi/book-refactoring2` repository,
primarily:

- Chapter 2 for principles and timing
- Chapter 3 for bad smells
- Chapters 4 and 2 for testing and safety expectations
- Chapters 6 through 12 for the refactoring catalog

When adding later books, keep the workflow in this file stable and add
new source-specific material under `references/`.
