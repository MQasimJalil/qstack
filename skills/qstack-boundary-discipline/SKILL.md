---
name: qstack-boundary-discipline
description: "Concentrate validation, narrowing, and error handling at a true system boundary."
---

# Boundary Discipline

## Procedure

1. Find where input crosses into the system. Decode and validate it there, returning a useful boundary error when it fails.
2. Pass validated domain values into internal logic. Keep framework, transport, storage, and wire representations behind the boundary.
3. Keep business decisions in testable pure functions where practical. Remove repeat validation that can only see already-validated internal values.

## Upstream sources

- Decode external representations into trusted domain types and keep framework wiring thin. [pstack/principle-boundary-discipline](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-boundary-discipline/SKILL.md#L13)
