---
name: qstack-maintain-formal-verification
description: "Update a model, proof, or formal verification skill after the covered code changes."
---

# Maintain Formal Verification

## Requirements

- The target must have a formal verification workflow or named check. A locally available verifier or reproducible runner is needed for execution.

## Procedure

1. Inventory each property, bounds, assumptions, covered code, last sync revision, and exact command. Run the existing check once as a baseline.
2. Read changes to covered state and transitions from the sync revision, including moves and new writers. Classify each change as irrelevant, model drift, an intentional contract change, or a possible bug.
3. Update only the verification to reflect the observed code. Change a property only with evidence the promise changed. Keep or explain the bound.
4. Rerun. Replay a failure step by step against the implementation. For a passing update, inject an isolated break within scope to show sensitivity, then remove it.
5. Record each outcome, verified code revision, evidence, bounds, and remaining gaps. Keep a blocked check's previous sync revision and separate product fixes from verification maintenance.

## Upstream sources

- Reconcile each named formal check from its sync commit, distinguish drift from bugs, and reprove failure sensitivity. [pstack/maintain-formal-verification-skill](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/maintain-formal-verification-skill/SKILL.md#L26)
