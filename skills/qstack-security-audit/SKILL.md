---
name: qstack-security-audit
description: "Perform a defensive source and configuration audit of an authorized application."
---

# Security Audit

## Requirements

- Read access to in-scope source, configuration, and defensive evidence.

## Procedure

1. Record the audit scope. Review architecture, trust boundaries, data exposure, authorization hooks, dependencies and deployment configuration from source and authorized read-only evidence.
2. For each actionable issue, point to file and line, name the violated invariant and explain impact and remediation. Distinguish potential weaknesses from confirmed source findings.
3. Review existing defensive tests and propose a safe regression assertion for each fix. Report coverage gaps, and limit static conclusions to what was inspected.
4. Deliver prioritized remediation with evidence, confidence, and owning component through authorized channels.

## Upstream sources

- Evidence-based defensive audit with trust boundaries, scoped findings, and coverage transparency. [gstack/cso](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/cso/SKILL.md#L16)
