# Refactoring 2 Smells

## Table of Contents

- Naming and local clarity
- Data and state
- Change pressure and coupling
- Control flow
- Class and hierarchy design
- Comments and cleanup

## Naming and Local Clarity

### Mysterious Name

Look for:

- Names that force readers to inspect implementation to understand use.
- Names that describe mechanics instead of intent.

Start with:

- `Change Function Declaration`
- `Rename Variable`
- `Rename Field`

### Duplicated Code

Look for:

- Same logic in more than one place.
- Similar blocks that differ only by ordering, constants, or data access.

Start with:

- `Extract Function`
- `Move Statements`
- `Pull Up Method`
- `Parameterize Function`

### Long Function

Look for:

- Commented blocks inside one function.
- Mixed levels of abstraction.
- Large conditionals or loops that hide intent.

Start with:

- `Extract Function`
- `Replace Temp with Query`
- `Split Loop`
- `Decompose Conditional`
- `Replace Conditional with Polymorphism`

### Long Parameter List

Look for:

- Functions that require many loosely related arguments.
- The same argument cluster repeated across calls.
- Boolean flags that change behavior.

Start with:

- `Introduce Parameter Object`
- `Preserve Whole Object`
- `Remove Flag Argument`
- `Replace Parameter with Query`

## Data and State

### Global Data

Look for:

- State writable from many places.
- Hidden cross-module coupling around shared values.

Start with:

- `Encapsulate Variable`
- `Move Function`
- `Move Field`

### Mutable Data

Look for:

- Variables updated for several unrelated purposes.
- Derived values cached and manually kept in sync.
- Query code mixed with mutation code.

Start with:

- `Encapsulate Variable`
- `Split Variable`
- `Separate Query from Modifier`
- `Remove Setting Method`
- `Replace Derived Variable with Query`

### Data Clumps

Look for:

- Same small field group traveling together.
- Repeated parameter clusters.

Start with:

- `Extract Class`
- `Introduce Parameter Object`
- `Preserve Whole Object`

### Primitive Obsession

Look for:

- Strings or numbers representing rich domain concepts.
- Repeated validation or formatting around basic values.

Start with:

- `Replace Primitive with Object`
- `Extract Class`
- `Introduce Parameter Object`
- `Replace Type Code with Subclasses`

### Temporary Field

Look for:

- Fields only used in narrow scenarios.
- Objects that seem partially initialized most of the time.

Start with:

- `Extract Class`
- `Move Function`
- `Introduce Special Case`

### Data Class

Look for:

- Classes that mostly expose getters and setters.
- Behavior living in clients instead of near the data.

Start with:

- `Encapsulate Record`
- `Remove Setting Method`
- `Move Function`
- `Extract Function`

## Change Pressure and Coupling

### Divergent Change

Look for:

- One module changing for several unrelated reasons.
- Database, domain, formatting, and transport logic mixed together.

Start with:

- `Split Phase`
- `Extract Class`
- `Move Function`
- `Extract Function`

### Shotgun Surgery

Look for:

- One requirement causing many small edits across files.
- Shared logic scattered across modules.

Start with:

- `Move Function`
- `Move Field`
- `Combine Functions into Class`
- `Combine Functions into Transform`
- `Inline Function`
- `Inline Class`

### Feature Envy

Look for:

- A function spending most of its time asking another object for data.
- Repeated foreign getter chains inside one method.

Start with:

- `Extract Function`
- `Move Function`

### Message Chains

Look for:

- Calls like `a.b().c().d()`.
- Clients navigating internal object structure directly.

Start with:

- `Hide Delegate`
- `Extract Function`
- `Move Function`

### Middle Man

Look for:

- A class that forwards too many calls without adding value.

Start with:

- `Remove Middle Man`
- `Inline Function`
- `Replace Superclass with Delegate`
- `Replace Subclass with Delegate`

### Insider Trading

Look for:

- Two modules that know too much about each other's internals.
- Cross-object field shuffling and intimate private knowledge.

Start with:

- `Move Function`
- `Move Field`
- `Hide Delegate`
- `Replace Subclass with Delegate`
- `Replace Superclass with Delegate`

## Control Flow

### Repeated Switches

Look for:

- Same branching logic repeated in several locations.
- New cases requiring edits in many files.

Start with:

- `Extract Function`
- `Replace Conditional with Polymorphism`
- `Replace Type Code with Subclasses`

### Loops

Look for:

- One loop doing several conceptually separate tasks.
- Loops that hide filter/map/aggregate intent.

Start with:

- `Split Loop`
- `Replace Loop with Pipeline`
- `Extract Function`

## Class and Hierarchy Design

### Lazy Element

Look for:

- A class or function adding no real abstraction.
- Thin wrappers whose name adds no insight.

Start with:

- `Inline Function`
- `Inline Class`
- `Collapse Hierarchy`

### Speculative Generality

Look for:

- Hooks, options, or abstractions added for imagined futures.
- Parameters or subclasses with no current pressure.

Start with:

- `Change Function Declaration`
- `Inline Function`
- `Inline Class`
- `Collapse Hierarchy`
- `Remove Dead Code`

### Large Class

Look for:

- Too many fields or too many unrelated methods.
- Clients using only separate subsets of one class.

Start with:

- `Extract Class`
- `Extract Superclass`
- `Replace Type Code with Subclasses`
- `Extract Function`

### Alternative Classes with Different Interfaces

Look for:

- Similar concepts that cannot be substituted because names or shapes
  differ.

Start with:

- `Change Function Declaration`
- `Move Function`
- `Extract Superclass`

### Refused Bequest

Look for:

- Subclasses ignoring or actively resisting inherited API.
- Inheritance used only for implementation reuse.

Start with:

- `Push Down Method`
- `Push Down Field`
- `Replace Subclass with Delegate`
- `Replace Superclass with Delegate`

## Comments and Cleanup

### Comments

Look for:

- Comments explaining what code should already make obvious.
- Comments apologizing for confusing structure.

Start with:

- `Extract Function`
- `Change Function Declaration`
- `Introduce Assertion`

Keep comments that explain intent, constraints, or why a tradeoff
exists. Remove comments that only compensate for muddy code.
