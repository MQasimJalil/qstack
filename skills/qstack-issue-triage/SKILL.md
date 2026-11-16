---
name: qstack-issue-triage
description: "Triage an in-scope chat issue report into one evidence-backed thread verdict."
---

# Issue Triage

## Requirements

- Configured source and authorized thread access, plus a tracker adapter when linking or creating issues.

## Procedure

1. Pin the configured channel, source thread and permalink. Read the full report, approved attachments and current fixes before assigning category or owner.
2. Trace the likely cause from action to observed result. Separate confirmed evidence from hypotheses and route by cause. Search the tracker by source permalink, signature, trigger and affected area.
3. Create a tracker issue only within the configured authorization for a clearly demonstrated, unresolved, unmatched issue. Post one authorized verdict as a reply under the pinned thread and keep its identity stable across retries.

## Upstream sources

- Freeze source thread, classify after tracing cause, dedupe tracker issues, and send an authorized single verdict. [pstack/triage-issue-reports](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/automations/benny/skills/triage-issue-reports/SKILL.md#L144)
