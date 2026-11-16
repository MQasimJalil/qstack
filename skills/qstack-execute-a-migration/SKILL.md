---
name: qstack-execute-a-migration
description: "Keep a planned rewrite or migration converging on the verified target architecture."
---

# Execute A Migration

## Procedure

1. Name the target state and final static and runtime checks before editing. Identify intermediate steps that need to be usable and define any planned reversible breakage.
2. Choose phase boundaries that either verify a meaningful part of the target or retain a clear rollback point. Run high-signal checks for touched areas within each phase.
3. Remove temporary bridges when their phase ends. Verify the whole target through its normal entry points and report any remaining compatibility obligation explicitly.

## Upstream sources

- Converge on a clear end state with explicit verification boundaries and scoped intermediate breakage. [pstack/principle-outcome-oriented-execution](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-outcome-oriented-execution/SKILL.md#L9)
