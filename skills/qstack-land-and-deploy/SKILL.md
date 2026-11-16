---
name: qstack-land-and-deploy
description: "Land an approved pull request and verify its resulting deployment."
---

# Land And Deploy

## Requirements

- Forge and deploy adapters with the project's required permissions and release configuration.

## Procedure

1. Identify the PR head, base branch, deploy target, merge method and required checks. Verify readiness, approvals and CI for the pinned revision.
2. Execute the authorized merge while the observed head is current. Record the landed revision and wait for its deployment. Distinguish skipped deployment from rollout failure.
3. Verify the exact deployed revision and configured health and smoke routes. Use the canary workflow when a monitoring window applies.
4. On failure, preserve evidence and follow any authorized rollback procedure. Report the landed revision, deployment outcome and observed health.

## Upstream sources

- Exact-head PR gates, deployment verification, canary monitoring, and rollback escalation. [gstack/land-and-deploy](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/land-and-deploy/SKILL.md#L298)
