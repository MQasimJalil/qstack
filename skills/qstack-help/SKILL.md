---
name: qstack-help
description: "Help a user discover qstack skills, configure them, choose the right workflow, or recover a stalled run."
---

# Help

## Procedure

1. Identify whether the user wants installation, model setup, a skill recommendation, or diagnosis of an existing run. Read the installed catalog and host instructions for the current package before naming commands.
2. Recommend the narrowest skill that produces the requested result. Give its trigger, deliverable, and exact invocation supported by the host. Give the full-workflow command when the user wants to exercise the bundled pilot.
3. For a stalled or unreliable run, recover the latest verified checkpoint, outstanding decision, and actual artifact. Show how to resume its existing check or route the next action without reopening finished work.
4. Keep guidance read-only until the user requests a setup or execution action. State any host capability or tool installation that the chosen workflow genuinely needs.

## Upstream sources

- Intent-to-skill lookup, model setup, playbook choice, and troubleshooting grounded in real checkpoints. [pstack/poteto-help](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/poteto-help/SKILL.md#L62)
