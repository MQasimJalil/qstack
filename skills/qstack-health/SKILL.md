---
name: qstack-health
description: "Build a repeatable repository health dashboard from native project checks."
---

# Health

## Procedure

1. Discover native type, lint, tests, coverage, and complexity checks. Mark unavailable checks and distinguish tool startup errors from valid failures.
2. Run each applicable category once against the same revision. Capture commands, exit statuses, raw counts, and findings. Show the disclosed scoring rubric and measured coverage.
3. Save a timestamped history row only when sufficient comparable measurements exist. Compare matching categories and thresholds to a preceding run, with evidence links for regressions.

## Upstream sources

- Discover tools, score categories, and save comparable health history. [gstack/health](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/health/SKILL.md#L219)
