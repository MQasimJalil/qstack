---
name: qstack-test-audit
description: "Find low-value tests, preserve independently useful coverage, and apply approved retirement batches."
---

# Test Audit

## Procedure

1. Set the scope, revision, and discovery budget. Use mechanical signals such as near duplicates, source-text assertions, no assertions, or export-list tests to identify candidates.
2. Read each full test, its production owner, callers, overlapping coverage, and history. Retain a test when it uniquely guards a contract. Record suppressed candidates and their stated reasons.
3. For each proposed retirement or rewrite, record the behavior, stronger proof, references searched, test-only code that could be removed, and exact validation commands. Group candidates by the owning boundary.
4. Report retire, rewrite, extend, or retain decisions and estimated production and test line changes separately. Apply only an in-scope batch with complete evidence.
5. Before removing production code, prove it is unreachable from the package entry point and run an appropriate build, typecheck, or dead-code check with it gone. Rerun owner and sibling tests and check the diff.

## Upstream sources

- Evidence cards and owner-aware batches for tests or test-only code that may be retired [gstack/test-audit](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/test-audit/SKILL.md#L197)
