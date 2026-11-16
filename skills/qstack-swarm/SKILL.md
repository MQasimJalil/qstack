---
name: qstack-swarm
description: "Partition independent work across workers or race several attempts against a fixed selection rule."
---

# Swarm

## Procedure

1. Define a verifiable done predicate. Pick coverage by disjoint slices, a same-brief race, or both. For a race specify first acceptable, rank all, or best-of before work starts.
2. Give each worker a standalone brief and a separate write target. Name the exact input revision and measurement recipe where findings depend on them.
3. Use authorized host delegation when available. Otherwise run the slices or attempts serially and retain the same contracts, while disclosing the execution mode.
4. Check each primary result against its brief before aggregation. Retry an incomplete slice once when useful, then record an uncovered gap. Apply the selection rule and provide one consolidated report with evidence.

## Upstream sources

- Partition or race with a frozen selection rule and require exact evidence from each required slice. [pstack/swarm](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/swarm/SKILL.md#L18)
