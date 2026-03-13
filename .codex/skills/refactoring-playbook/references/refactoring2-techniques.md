# Refactoring 2 Techniques

## Table of Contents

- Selection rules
- Local simplification
- Encapsulation and data shaping
- Moving behavior and separating phases
- Conditional logic
- API shaping
- Inheritance refactorings
- Common technique bundles

## Selection Rules

Choose the smallest technique that reduces the current smell.

- Rename before abstracting.
- Extract before moving.
- Inline before re-extracting when indirection became useless.
- Encapsulate mutable state before spreading new behavior across it.
- Split phases before introducing new object models for mixed concerns.

Prefer sequences of simple moves over one "clever" rewrite.

## Local Simplification

### Use for local clarity first

- `Extract Function`: isolate intent-revealing chunks.
- `Inline Function`: remove wrappers that no longer help.
- `Extract Variable`: name a complex expression.
- `Inline Variable`: remove aliases that add noise.
- `Split Variable`: separate one variable with multiple jobs.
- `Substitute Algorithm`: replace convoluted logic with a clearer
  implementation.

### Reach for these when

- A reader must simulate the code to understand it.
- A comment is needed to explain a block.
- One function mixes several abstraction levels.

## Encapsulation and Data Shaping

### Use for state and data boundaries

- `Encapsulate Variable`
- `Encapsulate Record`
- `Encapsulate Collection`
- `Replace Primitive with Object`
- `Introduce Parameter Object`
- `Combine Functions into Class`
- `Combine Functions into Transform`
- `Change Reference to Value`
- `Change Value to Reference`

### Reach for these when

- Shared mutable data is hard to track.
- The same fields travel together.
- Domain concepts are trapped inside strings or numbers.
- Related calculations orbit the same data structure.

## Moving Behavior and Separating Phases

### Use for coupling and change pressure

- `Move Function`
- `Move Field`
- `Move Statements into Function`
- `Move Statements to Callers`
- `Slide Statements`
- `Split Phase`
- `Hide Delegate`
- `Remove Middle Man`
- `Extract Class`
- `Inline Class`

### Reach for these when

- Behavior lives far from the data it needs.
- One change requires edits across several files.
- Sequential concerns are entangled, such as parsing plus pricing or
  fetching plus formatting.
- Clients navigate deep object relationships.

## Conditional Logic

### Use for branches and special cases

- `Decompose Conditional`
- `Consolidate Conditional Expression`
- `Replace Nested Conditional with Guard Clauses`
- `Replace Conditional with Polymorphism`
- `Introduce Special Case`
- `Introduce Assertion`

### Reach for these when

- A branch is difficult to name.
- Nested conditions dominate the function.
- The same case split appears in several places.
- Null or empty handling spreads everywhere.

## API Shaping

### Use for public function design

- `Change Function Declaration`
- `Separate Query from Modifier`
- `Parameterize Function`
- `Remove Flag Argument`
- `Preserve Whole Object`
- `Replace Parameter with Query`
- `Replace Query with Parameter`
- `Remove Setting Method`
- `Replace Constructor with Factory Function`
- `Replace Function with Command`
- `Replace Command with Function`

### Reach for these when

- Signatures miscommunicate intent.
- Callers pass too many knobs.
- A function both returns information and mutates state.
- Construction logic needs naming or variation.

## Inheritance Refactorings

### Use only when hierarchy pressure is real

- `Pull Up Method`
- `Pull Up Field`
- `Pull Up Constructor Body`
- `Push Down Method`
- `Push Down Field`
- `Replace Type Code with Subclasses`
- `Remove Subclass`
- `Extract Superclass`
- `Collapse Hierarchy`
- `Replace Subclass with Delegate`
- `Replace Superclass with Delegate`

### Reach for these when

- Subtypes duplicate logic.
- A type code keeps driving branching.
- A hierarchy exists only for reuse, not for a stable is-a model.
- A subclass resists the inherited API.

Default to composition when inheritance makes change harder.

## Common Technique Bundles

### Long function with temporary variables

Use:

1. `Extract Variable` for hard expressions.
2. `Replace Temp with Query` when temps block extraction.
3. `Extract Function` for named chunks.
4. `Decompose Conditional` or `Split Loop` when needed.

### Large class with mixed reasons to change

Use:

1. `Extract Function` to isolate cohesive behavior.
2. `Move Function` and `Move Field` toward the relevant data.
3. `Extract Class` for the stable subset.
4. `Split Phase` if sequential concerns are mixed.

### Repeated conditionals across modules

Use:

1. `Extract Function` per branch.
2. `Replace Conditional with Polymorphism` or
   `Replace Type Code with Subclasses`.
3. `Move Function` so branching lives near the variant data.

### Data clumps and primitive obsession

Use:

1. `Introduce Parameter Object` or `Extract Class`.
2. `Replace Primitive with Object` for domain rules.
3. `Preserve Whole Object` to simplify callers.

### Shotgun surgery around one requirement

Use:

1. `Move Function` and `Move Field` to centralize the affected logic.
2. `Inline Function` or `Inline Class` if the current split is artificial.
3. Re-extract after centralization if a cleaner boundary becomes obvious.
