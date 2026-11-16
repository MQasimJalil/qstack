---
name: qstack-blast-radius
description: "Trace what a change might break beyond its diff and prove the fact on which its safety depends."
---

# Blast Radius

## Procedure

1. Trace the change from the diff into callers, persisted data, external contracts, dependency versions, and lifecycle timing. Cite the source path that makes each effect reachable.
2. Pick the one or two facts that must be true for the change to be safe. Localize the observable difference between a world where each fact holds and one where it fails.
3. Run the narrowest executable check against the real implementation or running app. Record the actual result and distinguish verified facts, source-backed deductions, and open assumptions.
4. Report confirmed risks with their reproduction and impact. Report the highest-risk cases you cleared and give a rerunnable check for any fact the release depends on.

## Upstream sources

- Trace behavior outside the diff and prove the dominant safety assumption against the real code. [pstack/blast-radius](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/blast-radius/SKILL.md#L31)
