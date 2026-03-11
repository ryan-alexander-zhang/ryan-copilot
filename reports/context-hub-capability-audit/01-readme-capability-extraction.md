# README Capability Extraction

## Project Positioning

Context Hub is an agent-oriented CLI and content system that provides curated, versioned documentation plus lightweight memory and feedback loops so coding agents can retrieve better context and improve over time.

## Core Capability List

| Capability | README evidence | Boundary | Initial confidence |
| --- | --- | --- | --- |
| Search and discovery of available content | README quick start and commands table state `chub search [query]` can find available docs and skills, including examples like `chub search openai` and `chub search "stripe payments"`. | What it is: discovery over the available content catalog. What it is not: open-web search or arbitrary internet retrieval. | high |
| Retrieval of curated, versioned, language-specific content | README says Context Hub gives agents "curated, versioned docs" and shows `chub get openai/chat --lang py` and `--lang js` for variant-specific retrieval. | What it is: fetching packaged content variants by stable ID and language. What it is not: generating docs from source code on demand or crawling vendor sites live. | high |
| Incremental fetch of partial reference files versus full bundles | README key features section claims docs can have multiple reference files and `--file` fetches specific references while `--full` fetches everything. | What it is: selective retrieval within a document bundle. What it is not: semantic summarization or automatic token budgeting beyond the file selection model described. | medium |
| Local persistent annotations that reappear on future fetches | README says agents can `chub annotate`, that annotations are local notes, persist across sessions, and appear automatically on later `chub get`. | What it is: local, agent-specific memory attached to content IDs. What it is not: shared team knowledge sync or maintainer-visible edits to the source docs. | high |
| Feedback submission to improve shared content over time | README states `chub feedback <id> <up|down>` sends votes to maintainers and describes a loop where authors improve docs based on feedback. | What it is: outbound quality signals tied to content usage. What it is not: in-repo direct editing, automatic doc rewriting, or guaranteed closed-loop maintainer actions. | medium |

## Capability Notes

### 1. Search and discovery of available content

- README evidence: Quick start and commands table present `search` as the first discovery command and explicitly say it can search docs and skills.
- Boundary note: limited to the repository-backed or service-backed catalog exposed by Chub, not arbitrary knowledge retrieval.

### 2. Retrieval of curated, versioned, language-specific content

- README evidence: opening paragraph says "curated, versioned docs"; content types section emphasizes language-specific variants; quick start uses `get`.
- Boundary note: retrieval assumes content already exists in Context Hub's format and catalog.

### 3. Incremental fetch of partial reference files versus full bundles

- README evidence: "Docs can have multiple reference files beyond the main entry point" plus `--file` and `--full`.
- Boundary note: README does not yet specify how reference files are indexed or linked, so the implementation details remain an inference target for Stage 3.

### 4. Local persistent annotations that reappear on future fetches

- README evidence: annotation examples plus the explicit statement that annotations persist across sessions and appear automatically on future fetches.
- Boundary note: these notes are described as local, so shared synchronization should not be assumed.

### 5. Feedback submission to improve shared content over time

- README evidence: command table documents `feedback`; multiple sections say feedback flows to doc authors and maintainers.
- Boundary note: the README claims an improvement loop, but whether the repository contains only the client side or also server-side handling remains unknown.

## Stage 1 Outcome

- Normalized capability count: 5
- README-only confidence: moderate overall
- Known weak areas before verification:
  - Whether "skills" are first-class searchable content today or a partially implemented extension.
  - Whether feedback transport and maintainer workflows are fully implemented in this repository.
  - Whether incremental fetch is a thin file-selection feature or a richer bundle/index mechanism.
