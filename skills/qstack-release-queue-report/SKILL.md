---
name: qstack-release-queue-report
description: "Inspect release queue order and version conflicts without modifying the queue."
---

# Release Queue Report

## Requirements

- Read access to the forge or a saved queue snapshot with known freshness.

## Procedure

1. Resolve the forge, base branch, base version and current head. Read live queue and PR version claims with timestamps.
2. Summarize planned order, ready revisions, each candidate's version and projected sibling conflicts. Distinguish live values from cached observations.
3. Return a single queue view, the evidence for conflicts, and the next decision the queue owner needs to make.

## Upstream sources

- Read-only view of base version, sibling PRs, slot projections and collisions. [gstack/landing-report](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/landing-report/SKILL.md#L153)
