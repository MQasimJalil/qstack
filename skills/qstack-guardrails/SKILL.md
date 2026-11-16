---
name: qstack-guardrails
description: "Set, inspect, or release an edit boundary and destructive-action guard for a work session."
---

# Guardrails

## Requirements

- Enforcement requires a host with directory-scoped write controls.

## Procedure

1. Choose warning, scoped edits, both, status, or release. Canonicalize the allowed directory and target, including symlinks, before comparing them.
2. Route recursive deletion, data-destructive actions, and history rewrites through existing host controls. Identify concrete effects and preserve stronger host protections.
3. Set or release only the named session's boundary. Leave unrelated locks in place and preserve the prior state on busy or uncertain ownership.
4. Read the state back. Report whether the host enforces the boundary or the agent follows it as advisory guidance.

## Upstream sources

- Detect destructive actions across shells and data tools. [gstack/careful](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/careful/SKILL.md#L40)
- Limit writes to a selected directory. [gstack/freeze](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/freeze/SKILL.md#L34)
- Combine destructive warnings and scoped edits. [gstack/guard](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/guard/SKILL.md#L44)
- Release an edit boundary through its state owner. [gstack/unfreeze](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/unfreeze/SKILL.md#L26)
