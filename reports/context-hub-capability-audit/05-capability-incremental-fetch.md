# Incremental Fetch of Partial Reference Files Versus Full Bundles

## 1. Capability Definition

- Problem solved: avoid loading an entire doc directory when only a specific reference file is needed.
- User or scenario: an agent starts from a small entry point and drills into a specific advanced file or requests all companion files.
- Input: entry ID with either default mode, `--file`, or `--full`.
- Output: entry-point markdown, one or more selected files, or the full file set.

## 2. README-Side Mechanism

- README key features section says docs can include multiple reference files, with `--file` for targeted fetch and `--full` for everything.

## 3. Solution Analysis And Alternatives

- Implementation paradigm: entry directories declare a file inventory in the registry; runtime fetches use that inventory for validation and selective retrieval.
- This is a concrete directory-based progressive disclosure system, not a semantic chunking system.

## 4. Implementation Mechanics

- `build.js` computes `files` by recursively listing each entry directory.
- `get.js` derives `refFiles` by excluding `DOC.md` or `SKILL.md`.
- `--file` validates requested paths against `resolved.files`; invalid requests surface available alternatives.
- `--full` loads all files via `fetchDocFull()`.
- Default mode returns only the entry point and advertises extra files in the footer.
- MCP parity exists through `handleGet()` in `cli/src/mcp/tools.js`, including path traversal rejection.

## 5. State and Lifecycle Analysis

- Fetch mode branches:
  - default entry-point fetch
  - selected file fetch
  - full bundle fetch
- Error branches:
  - invalid file path
  - requested file not listed in registry
  - content load failure from source/cache/CDN

## 6. Data and Storage Analysis

- The file inventory is stored in each resolved version record as `files[]`.
- Full fetch concatenates or writes all files; targeted fetch preserves relative paths.
- The content remains plain markdown files rather than an indexed chunk store.

## 7. Architecture Analysis

- Incremental fetch is not a separate subsystem; it is a mode of the same retrieval pipeline driven by registry metadata.

```mermaid
flowchart TD
  Entry[Resolved entry] --> Mode{Fetch mode}
  Mode --> Default[DOC.md or SKILL.md only]
  Mode --> File[Specific file from files[]]
  Mode --> Full[All files from files[]]
  Default --> Footer[Show additionalFiles footer]
  File --> Output[Return requested content]
  Full --> Output
  Footer --> Output
```

## 8. Core Call Path

- Entry point: `cli/src/commands/get.js`
- Intermediate processing:
  - `resolveDocPath()`
  - `fetchDoc()` for one file
  - `fetchDocFull()` for many files
- Output node: stdout, JSON, or directory/file output

## 9. Key Technical Points

- `--file` and `--full` are backed by explicit file lists, not filesystem trust.
- MCP `handleGet()` adds path traversal validation absent from the CLI command path.
- Relative directory structure is preserved when writing full outputs to disk.

## 10. Code Verification

- Code locations:
  - `cli/src/commands/get.js`
  - `cli/src/lib/cache.js`
  - `cli/src/commands/build.js`
  - `cli/src/mcp/tools.js`
  - `docs/content-guide.md`
- Confirmed parts:
  - file inventory generation
  - extra-files footer
  - targeted file retrieval
  - full-bundle retrieval
  - helpful invalid-file error reporting
- Supporting tests:
  - `cli/test/e2e.test.js`
  - `cli/tests/mcp/tools.test.js`
- README claim is implemented.

## 11. Rebuildability

- Minimum modules:
  - recursive file inventory during build
  - runtime file whitelist validation
  - single-file and multi-file fetch helpers
- No hidden external service is required beyond the same content source used for normal retrieval.

## 12. Consistency Check

- README claim: fetch only what you need with `--file`, or everything with `--full`.
- Code reality: implemented directly and verified by tests.
- Gap summary: the README’s "no wasted tokens" framing is marketing language; the actual mechanism is deterministic file selection, not token-aware planning.
- Mismatch classification: `same meaning, different naming`

## 13. Conclusion

- Exists: yes
- Confidence: high
- Validation status: Validated
- Evidence grade: A
- Next code entrypoints:
  - `cli/src/commands/get.js`
  - `cli/src/commands/build.js`
  - `cli/src/mcp/tools.js`
