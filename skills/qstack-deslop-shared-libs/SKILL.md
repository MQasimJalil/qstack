---
name: qstack-deslop-shared-libs
description: "Audit recent work for shared-code opportunities with proven callers and net savings."
---

# Deslop Shared Libs

## Procedure

1. Pin the reviewed revision or overlay. Inspect recent first-party changes and work already in progress. Exclude generated and vendor copies when counting potential callers.
2. Require at least two verified caller locations. Compare contracts, errors, side effects, dependencies, and deployment boundaries. Check existing libraries before proposing another shared helper.
3. For each viable idea, name the helper, destination, callers, migration order, compatibility tests, and shared failure path. Estimate removed and added lines for implementation and total change separately, including tests and integration.
4. Recheck source at the recorded revision and rank ideas by reliability gain, net savings, and adoption risk. Return a short, read-only report with source links and the ideas already covered by active work.

## Upstream sources

- Two real callers, contract compatibility, cost accounting, and a read-only ranked report [gstack/deslop-shared-libs](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/deslop-shared-libs/SKILL.md#L151)
