# README Capability Extraction

## Project positioning

Happy is a mobile/web companion for running Claude Code or Codex from anywhere through a local CLI wrapper and an end-to-end encrypted sync service.

## Core capability list

| Capability | README evidence | Boundary | Initial confidence |
| --- | --- | --- | --- |
| Mobile and web remote control of coding agents | Title says "Mobile and Web Client for Claude Code & Codex"; README says "Use Claude Code or Codex from anywhere" and "control your coding agent from your phone" | It is remote control and observation of a coding-agent session; it is not a hosted agent runtime replacing the local machine | high |
| CLI wrapper for Claude Code and Codex | README instructs users to run `happy` instead of `claude`, and `happy codex` instead of `codex`; "start your AI through our wrapper" | It wraps existing local agent CLIs; it is not presented as its own model SDK or first-party coding engine | high |
| End-to-end encrypted sync | README headline says "with end-to-end encryption"; feature list says "Your code never leaves your devices unencrypted" | It protects message/session transport and storage; it does not imply server-side execution secrecy beyond encrypted payload handling | medium |
| Device handoff and notifications | Feature list says "Push notifications" and "Switch devices instantly"; How it works says the session "restarts the session in remote mode" and "press any key" to switch back | It covers operational control and awareness; it is not a claim about collaborative multi-user editing or arbitrary multi-device concurrency | medium |

## Boundary notes

### 1. Mobile and web remote control

- What it is: a client experience that can send prompts, receive agent events, and manage a session from phone/web.
- What it is not: a cloud-hosted Codex/Claude execution backend.

### 2. CLI wrapper for Claude Code and Codex

- What it is: a local replacement command that inserts Happy session management, transport, and UI/protocol adaptation around existing CLIs.
- What it is not: a reimplementation of Codex or Claude through provider SDK calls.

### 3. End-to-end encrypted sync

- What it is: encrypted metadata, state, and message flow between client devices and server-backed session sync.
- What it is not: proof that every external integration in the stack is zero-knowledge; README only claims encrypted Happy transport/storage.

### 4. Device handoff and notifications

- What it is: remote mode, readiness/permission notifications, and switching between phone and computer.
- What it is not: evidence that all agent flavors implement the exact same switching semantics.

## README-only observations

- README does not mention multi-agent orchestration as a product capability.
- README does not mention `skills`, `AGENTS.md`, `SKILL.md`, or any Happy-managed skill system.
- Therefore, any conclusion about multi-agent or skills must come from Stage 3 code verification, not from README claims.
