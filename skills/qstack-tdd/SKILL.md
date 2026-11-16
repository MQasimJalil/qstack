---
name: qstack-tdd
description: "Fix a bug with a focused regression that fails for the right reason before the repair."
---

# Tdd

## Procedure

1. Identify the intended observable behavior, the defect, and the cheapest practical user or caller entry point that reproduces it.
2. Add the smallest focused regression using the project's existing test setup. Run it before editing production code and confirm its failure matches the defect.
3. Make the smallest production change that restores the contract. Rerun the regression and nearby relevant tests without weakening expected behavior.
4. When a durable failing test is impractical, use the nearest reproducible runtime check and report the before and after evidence and its limits.

## Upstream sources

- Smallest practical failing-before test, targeted fix, and passing-after evidence [pstack/tdd](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/tdd/SKILL.md#L13)
