---
name: qstack-evaluation-plan
description: "Preregister and run a controlled evaluation with a measurable outcome, baseline, and budget."
---

# Evaluation Plan

## Requirements

- Data and an evaluation harness. Paid work requires the applicable budget and authorization.

## Procedure

1. Define arms, baseline, dataset split, metrics, thresholds, sample size, stop rules, budget and result-to-action mapping before collecting priced evidence.
2. Run a zero-cost dry run on development rows to confirm schema, prompts, logs, outputs and budget instrumentation. Keep held-out examples out of development and calibrate model judges against human labels.
3. Run a small authorized capped pilot to estimate full cost and error rates. Run the approved remaining arms under frozen conditions.
4. Report side-by-side measurements, sample sizes, costs, uncertainty and the preregistered decision. Treat a changed experiment as a new run.

## Upstream sources

- Preregister metrics, decision rules, controls, data split, and staged spend. [gstack/eval-plan](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/eval-plan/SKILL.md#L130)
