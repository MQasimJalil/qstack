---
name: qstack-isolate-shared-state
description: "Resolve competing writers by isolating state before adding structural serialization."
---

# Isolate Shared State

## Procedure

1. Inventory each mutable file, branch, key, or object and the writers that can reach it at the same time.
2. Give independent facts a designated writer and separate output location. Combine them at the read or reporting boundary.
3. For an invariant that requires one canonical writable object, use a single writer, atomic compare-and-swap, a lock, or a genuinely sequential phase. Exercise overlapping operations to prove the mechanism.

## Upstream sources

- Separate independent writes and enforce real shared ownership structurally. [pstack/principle-separate-before-serializing-shared-state](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md#L13)
