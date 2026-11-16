---
name: qstack-manage-context
description: "Keep a large investigation or multi-phase agent task inside a usable context window."
---

# Manage Context

## Procedure

1. Set limits for files, output volume, and scope per phase before a broad read. Read indexes first and retrieve only the passages needed for the current decision.
2. Use an authorized delegate for a genuinely independent bulk read when available. Otherwise process bounded slices serially and reduce them as you go.
3. Keep the source link, observation, and decision in a short handoff. Retrieve raw traces or large artifacts again only when the next check requires them.

## Upstream sources

- Cap phase scope and preserve compact evidence instead of carrying bulky raw payloads. [pstack/principle-guard-the-context-window](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-guard-the-context-window/SKILL.md#L9)
