---
name: qstack-decision-trail
description: "Keep an append-only evidence trail during long-running or unattended work."
---

# Decision Trail

## Procedure

1. Create or reuse a scoped TSV trail with time, phase, decision, reason, evidence and result. Start each appended run with a boundary row.
2. Record consequential decisions, pivots, blockers and verified checkpoints with resolvable evidence pointers. Keep cells single-line and escape spreadsheet formula prefixes when exporting.
3. Check this run's rows and pointers against actual work before handing off. Append corrections or superseding rows and point the reader to the relevant run range.

## Upstream sources

- Append decision rows, record a run boundary, and audit evidence without rewriting history. [pstack/show-me-your-work](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/show-me-your-work/SKILL.md#L34)
