---
name: qstack-fix-root-causes
description: "Find the earliest code decision that produces a defect and verify the fix on the original surface."
---

# Fix Root Causes

## Procedure

1. Reproduce the symptom and inspect actual state at each preceding step. Add focused instrumentation when the first wrong decision is unclear.
2. Decide whether the triggering state is valid. For a valid state, fix the consumer that mishandles it. For an invalid state, fix the producer or the invariant it violates.
3. Use the same diagnosis to find other in-scope instances. Replay the original reproduction on the same surface and retain the deciding observation for review.

## Upstream sources

- Reproduce, trace legitimate versus impossible state, instrument uncertainty, and fix all in-scope instances. [pstack/principle-fix-root-causes](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-fix-root-causes/SKILL.md#L13)
