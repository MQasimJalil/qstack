---
name: qstack-qa
description: "Test a real browser, API, CLI, or background workflow and optionally repair reproduced defects."
---

# QA

## Requirements

- Use the project's supported test tools or a browser for the selected surface. Use authorized test data for state-changing paths.

## Procedure

1. Choose report or repair mode from the request. Identify the browser, API, CLI, job, worker, or webhook under test. Record current build, environment, safe test data, and the relevant contract.
2. Select project-native checks and isolated instances where needed. Write a test charter with each entry point, expected result, practical limit, and evidence to collect. Preserve prior baselines when verifying a regression.
3. Exercise the real user path and retain the smallest reproducible steps with actual and expected results. Include screenshots, responses, logs, commands, and relevant timings that support each claim. Distinguish product findings from environment failures.
4. In report mode, rank findings and save a report with stable evidence links. In repair mode, reproduce each chosen defect, use a focused failing regression where practical, make the smallest related fix, and repeat the same check.
5. Run a final pass on repaired and critical paths. Record fixed, remaining, deferred, and untested items with a traceable baseline. Preserve evidence after cleaning up the test instances.

## Upstream sources

- Baseline and triage, cause-focused fixes, regression evidence, and final re-test [gstack/qa](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/qa/SKILL.md#L340)
- Report-only surface selection, isolation, and evidence-preserving artifact workflow [gstack/qa-only](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/qa-only/SKILL.md#L188)
