---
name: qstack-release-crew
description: "Coordinate release lanes through a controller and a verified merge train."
---

# Release Crew

## Requirements

- Authorized parallel-agent and forge capabilities. Merging requires the project's approvals.

## Procedure

1. Assign authorized lanes isolated work areas, edit scopes, deliverables and stop conditions. Keep merge authority with the controller. Have lanes report the exact ready PR head, base, checks and pending decisions.
2. Validate receipts and approvals against current heads. Build an ordered train in an isolated worktree, record the base and prefix trees, and verify the combined tree.
3. Land approved candidates while heads and base match the checked sequence. Rebuild when a head or base moves. Maintain a digest for owner decisions, newly landed changes, and blockers.
4. Route confirmed flaky tests to a repair lane and preserve baseline and rerun evidence.

## Upstream sources

- Version-bound readiness records, staged trains, one controller, and a compact owner digest. [gstack/captain](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/captain/SKILL.md#L167)
