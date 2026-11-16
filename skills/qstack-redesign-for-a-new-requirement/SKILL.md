---
name: qstack-redesign-for-a-new-requirement
description: "Integrate a new requirement by reconsidering the existing design and its invariants."
---

# Redesign For A New Requirement

## Procedure

1. Read affected files, examples, and decisions. List the old assumptions and the new requirement that changes them.
2. Sketch the shape you would choose if the requirement were present from the beginning. Reuse useful existing boundaries and change the ones that would force special-case coordination.
3. Apply the redesign incrementally across types, callers, docs, and examples. Verify the original obligations that remain and the new observable behavior.

## Upstream sources

- Re-derive the design with the new requirement in mind, then propagate the result coherently. [pstack/principle-redesign-from-first-principles](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-redesign-from-first-principles/SKILL.md#L11)
