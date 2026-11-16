---
name: qstack-canary
description: "Watch a newly deployed application for persistent production regressions."
---

# Canary

## Requirements

- Read access to the deployed application and a browser or health-check interface.

## Procedure

1. Identify the deployment, approved read-only routes, comparison baselines and observation window. Timestamp the first observation.
2. Check page state, relevant console failures, critical resources and latency or layout signals. Capture comparable screenshots in each round.
3. Use persistent deviations across consecutive rounds as regression evidence. Record immediate outages as observed. Without a baseline, label the report as a health check.
4. Return routes, timestamps, differences and evidence. Route investigation or remediation as a separate operation.

## Upstream sources

- Bounded post-deployment rounds with screenshots and baseline comparisons. [gstack/canary](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/canary/SKILL.md#L225)
