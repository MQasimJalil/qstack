---
name: qstack-benchmark
description: "Measure a browser or system performance change with a controlled baseline and an evidence-backed conclusion."
---

# Benchmark

## Procedure

1. Write the decision the result could change, the smallest meaningful effect, and the user workload that matters. Select a baseline and candidate revision.
2. Use an identical fixture, settings, device profile, workload, and load generator for both revisions. Warm up consistently and repeat enough to see variance. For browser changes capture navigation timing, relevant Web Vitals, and resource weight.
3. Verify both sides did comparable work successfully. Check throttling, queues, dropped requests, CPU or memory limits, cache state, and the resource that set the observed ceiling.
4. Report raw values, units, sample count, dispersion, delta, environment, and the artifact or command that reproduces them. Mark the result inconclusive when variation is larger than the effect.

## Upstream sources

- Collect comparable browser timing, Web Vitals, and resource sizes across revisions. [gstack/benchmark](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/benchmark/SKILL.md#L241)
- Check limiter, tuning, errors, completed work, repeatability, and relevance. [pstack/benchmark-checklist](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/benchmark-checklist/SKILL.md#L19)
- State the decision, target, and noise floor before interpreting a number. [pstack/principle-explain-the-number](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-explain-the-number/SKILL.md#L9)
