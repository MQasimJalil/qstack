---
name: qstack-simplify-change
description: "Reduce a refactor or addition to the smallest change that meets a proven requirement."
---

# Simplify Change

## Procedure

1. Name the required behavior and identify the observed callers. Locate decisions that are repeated or controls no caller uses.
2. Remove dead code, redundant layers, stale references, and speculative validators before adding anything. Retain guards that have an actual boundary or contract.
3. Keep one source of truth for each choice and pass its result directly to callers. Verify preserved behavior and check that the final diff contains only the work the contract needs.

## Upstream sources

- Concentrate one decision at one source and minimize the diff. [pstack/principle-laziness-protocol](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-laziness-protocol/SKILL.md#L9)
- Delete dead code, speculative guards, and empty references before construction. [pstack/principle-subtract-before-you-add](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-subtract-before-you-add/SKILL.md#L13)
