---
name: qstack-ship
description: "Prepare a verified branch and publish a requested pull request using the repository's release process."
---

# Ship

## Requirements

- Repository test interfaces and forge permission for a requested publication.

## Procedure

1. Resolve branch, destination base, open PR and release requirements. Identify whether the user requested readiness inspection, branch preparation, or publication. Inspect the current tree for a readiness-only request. If branch preparation is authorized, preserve unrelated work and bring the branch onto the intended base before checking it.
2. Reuse matching evidence and run required missing checks once for the final tree. Review intended changes, version and documentation requirements, and prepare the PR body with evidence.
3. Create or update the requested branch or PR through its normal forge path. Verify that the remote head matches the reviewed revision and report the PR link, checks, blockers and release notes.

## Upstream sources

- Bind checks to the exact tree, refresh release artifacts when appropriate, and publish the verified PR. [gstack/ship](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/ship/SKILL.md#L654)
