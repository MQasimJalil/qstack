---
name: qstack-type-system-discipline
description: "Use a static type system to make bad states and mixed-up values difficult or impossible to express."
---

# Type System Discipline

## Procedure

1. Choose representations that admit only valid combinations. Use exhaustive variant handling where the language supports it.
2. Give overloaded primitives distinct semantic types when mixing them up is a real risk. Construct those values from checked inputs at the boundary.
3. Derive types from authoritative schemas before adding parallel definitions. Keep unknown input at the perimeter and verify new cases through the boundary.

## Upstream sources

- Represent legal variants, brand semantic primitives, parse external data once, and derive from schemas. [pstack/principle-type-system-discipline](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-type-system-discipline/SKILL.md#L9)
