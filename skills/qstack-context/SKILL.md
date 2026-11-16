---
name: qstack-context
description: "Save, list, or reconstruct working context so another session can resume accurately."
---

# Context

## Requirements

- Project records or an existing checkpoint. Session history is optional and must be in scope.

## Procedure

1. Resolve the project and active ref. In save mode, write an append-only checkpoint with goal, decisions, affected files, verified results, blockers, and next action.
2. In list or restore mode, identify the matching checkpoint and compare the saved revision and PR with the current worktree. Report drift that changes how to resume.
3. When the checkpoint is absent or incomplete, reconstruct from the current checkout, authorized shared history and in-scope transcripts. Label unverified claims.
4. Return a short capsule, workstream statuses, outstanding problems and one next move.

## Upstream sources

- Persist a recoverable handoff with decisions and live state. [gstack/context-save](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/context-save/SKILL.md#L274)
- Find and validate project checkpoints or recover from existing records. [gstack/context-restore](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/context-restore/SKILL.md#L145)
- Combine session history with shared records to reconstruct the current state. [pstack/recall](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/recall/SKILL.md#L24)
