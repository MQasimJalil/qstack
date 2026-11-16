---
name: qstack-modernize-pr
description: "Decide whether an aging pull request should be updated, reworked, or closed against the current base."
---

# Modernize Pr

## Requirements

- Repository history and read access to the PR. External mutation requires the applicable authorization.

## Procedure

1. Read the PR as a claim about behavior. Pin its observed head and base, inspect current implementation and history, and check whether another change already solved it.
2. Choose modernize, rework, or recommend closure with evidence. Modernize in isolation and verify every original effect against the refreshed base.
3. For an authorized update, use the forge's expected-head protection. Report the disposition, before-after revisions, evidence and any closure decision the owner must make.

## Upstream sources

- Classify the PR from current base evidence, preserve intent and pin any remote update. [gstack/modernize](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/modernize/SKILL.md#L174)
