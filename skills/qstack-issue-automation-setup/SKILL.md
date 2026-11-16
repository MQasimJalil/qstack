---
name: qstack-issue-automation-setup
description: "Configure and test adapters for thread-scoped issue triage and reproduction."
---

# Issue Automation Setup

## Requirements

- Authorized chat, tracker, repository, automation and app-control capabilities for the configured modes.

## Procedure

1. Record source channel, actors, tracker routes, repos, budgets and authorization for automated issue or draft PR creation. Store secrets with the integration provider.
2. Define adapter contracts for attachments, read-only tracker dedupe, thread replies, real-app reproduction and optional draft PR creation. Verify the app can be driven through a concrete feature map.
3. Test a harmless thread. Check one reply in the correct parent, correct dedupe, blocking on missing permissions, and evidence capture. Enable live handling only for the verified requested scope.

## Upstream sources

- Configure evidence, tracker and control adapters and test thread safety before enablement. [pstack/setup-benny](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/automations/benny/skills/setup-benny/SKILL.md#L117)
