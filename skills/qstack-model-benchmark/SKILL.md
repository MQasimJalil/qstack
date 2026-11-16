---
name: qstack-model-benchmark
description: "Compare agent models or providers on the same skill prompt and score tangible outputs with an explicit rubric."
---

# Model Benchmark

## Procedure

1. Freeze the prompt, input fixture, model IDs, tool access, budgets, and scoring rubric. Use an independent judge when model identity could influence scores.
2. Use qstack-evaluation-plan before a paid run when the comparison needs preregistration or a controlled spend. Exercise the provider interface with a no-cost fixture first where available.
3. Run each authorized arm against the same input. Save outputs, model, runtime, tool errors, output scores, and actual usage or cost when available.
4. Compare task success and operating cost separately. Distinguish timeout, error, and missing data from quality scores. Keep single-sample rankings provisional.

## Upstream sources

- Select one prompt and eligible providers, control the judge policy, and retain output and usage evidence. [gstack/benchmark-models](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/benchmark-models/SKILL.md#L173)
