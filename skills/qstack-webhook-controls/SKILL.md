---
name: qstack-webhook-controls
description: "Build a small control interface for an authorized webhook-driven routine."
---

# Webhook Controls

## Requirements

- An authorized webhook provider and a secure credential interface.

## Procedure

1. Identify permitted routine actions and define a small request schema. Validate incoming fields and expose only those actions.
2. Configure the routine through the available provider. Keep credentials in its secure store and use a trusted component for authenticated requests. Treat webhook data as input.
3. Build controls with execution status and test harmless success and invalid-input rejection. Expose the interface on the local machine or an explicitly authorized private network. Report bounded addresses and cleanup.

## Upstream sources

- Define control events, secure sender authentication, and verify private or local UI operation. [pstack/make-bot-ui](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/make-bot-ui/SKILL.md#L13)
