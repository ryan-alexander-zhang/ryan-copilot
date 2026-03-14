# Entrypoints and Main Flow Template

Use this template to create `02-entrypoints-and-main-flow.md`.

## Entrypoints and Main Flow

### 1. Scope

- Repository:
- Requested audit scope:
- Goal of this shared investigation:
- Which later capability tasks will reuse this document:

### 2. Key Entrypoints

| Entrypoint | File | Role | Why it matters |
| --- | --- | --- | --- |

### 3. Main Flow Skeleton

- Top-level execution flow
- Shared orchestration logic
- Core execution layer
- Important adapters, infra, or external-service boundaries
- High-level state or lifecycle transitions
- Where key data is created, transformed, stored, or emitted
- Add a `Mermaid sequenceDiagram` and `Mermaid flowchart` by default when evidence supports them

### 4. Architecture Notes

- Main modules and responsibilities
- Important boundaries between layers
- Cross-cutting concerns such as config, cache, telemetry, persistence, auth, or transport
- Core technology choices that shape implementation
- Add a `Mermaid stateDiagram-v2` when lifecycle stages are explicit
- Add a `Mermaid classDiagram` when shared data and storage structures are clear

### 5. Shared Evidence for Capability Tasks

- Code locations that multiple capability analyses will reference
- Important configs and manifests
- Any constraints discovered here that affect later validation
- Shared storage or state-management mechanisms

### 6. Open Questions

- Areas that still require targeted validation
- Potential mismatch hotspots
- Unknowns that block rebuild-level understanding

### 7. Recommended Next Reading Paths

- 1.
- 2.
- 3.
