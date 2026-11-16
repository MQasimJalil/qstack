---
name: qstack-design-review
description: "Audit the implemented design in a running product and verify any authorized repairs."
---

# Design Review

## Requirements

- Use a browser that can inspect layout and capture screenshots of the tested build.

## Procedure

1. Open the target build and record the baseline, key journeys, breakpoints, and comparison screenshots. Use an existing design review baseline when one matches the target and conditions.
2. Follow real user flows across screens and states. Inspect hierarchy, typography, color, spacing, layout, accessibility, interaction feedback, and cross-page consistency. Capture reproducible examples of each material finding.
3. Rank findings by user impact. Report the overall design grade and the separate grade for generic or formulaic presentation. Store category grades and stable finding IDs for future comparisons.
4. When repairs are in scope, make each fix at the source, capture the same viewport and interaction afterward, and rerun the affected flow. Track new console errors and leave deferred work visible.
5. Deliver the final design report with scope, baseline, fixes, remaining findings, and before-and-after evidence.

## Upstream sources

- Live interaction and consistency audit, scored baseline, before-and-after repairs, and regression report [gstack/design-review](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/design-review/SKILL.md#L746)
