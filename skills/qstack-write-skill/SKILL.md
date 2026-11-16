---
name: qstack-write-skill
description: "Create, revise, or trim an agent skill with evidence that its instructions improve real use."
---

# Write Skill

## Procedure

1. Find the target skill and its consumers. Capture current size and behavior for representative tasks before editing. Identify the exact failure or missing capability.
2. Fix a tool or validation layer when it can enforce the behavior naturally. Add or change prose for judgment, routing, and context the execution environment cannot derive.
3. Put each instruction at the lowest level that reaches the agent on time. Keep the discovery description narrow, the main workflow short, and detailed material in references selected by the task.
4. For a major trim, inventory commands and dependencies and run representative before, after, and no-skill cases. Check that retained examples and tool references still work.
5. Record what changed, the size difference, and evidence of improvement or a dated measurement plan.

## Upstream sources

- Tool-first edit ladder, instruction-level budgets, drift checks, and baseline comparisons [gstack/write-skill](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/write-skill/SKILL.md#L125)
