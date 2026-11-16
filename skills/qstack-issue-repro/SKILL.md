---
name: qstack-issue-repro
description: "Reproduce a triaged app issue and prepare a bounded fix when evidence supports it."
---

# Issue Repro

## Requirements

- Configured triage contract, app-control adapter, and authorized repository and thread access.

## Procedure

1. Pin the source thread and validate the triage verdict and actor. Check whether someone claimed the fix or whether an existing change already covers it.
2. Exercise the exact user path with the authorized adapter. Capture expected and observed results and environment. Verify an existing fix before creating another and record failures to reproduce.
3. Fix only an authorized, confirmed issue with a bounded demonstrated cause. Isolate the edit, replay the same path with before-and-after evidence, and run required checks.
4. Where authorized, open a draft PR linked to the issue and reply on the pinned thread. Preserve evidence and clean up the temporary environment.

## Upstream sources

- Validate the triage and ownership contracts, reproduce on the real UI, and prove the fix before draft publication. [pstack/reproduce-and-fix-issues](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md#L267)
