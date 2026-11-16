---
name: qstack-make-operations-idempotent
description: "Design commands and state changes to converge after retries, restarts, or interrupted runs."
---

# Make Operations Idempotent

## Procedure

1. Describe the target state and the evidence that proves it. On each run read the current state, compare it to the target, and apply only the remaining difference.
2. Make unfinished artifacts recognizable after interruption. Use a verifiable marker or atomic publication when the next run must distinguish completed work from a partial write.
3. Check a normal run, an immediate repeat, and restarts after each meaningful interruption point. Add reconciliation where any run fails to converge.

## Upstream sources

- Derive actions from observed state and test convergence after every interruption boundary. [pstack/principle-make-operations-idempotent](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-make-operations-idempotent/SKILL.md#L13)
